# coding=utf-8

from odoo import models, fields, api, _


class PromotionWizard(models.TransientModel):
    _name = 'promotion.wizard'

    order_id = fields.Many2one(comodel_name='sale.order', string="Order")
    available = fields.Boolean(string='Available', default=False)
    promotion_id = fields.Many2one(comodel_name='sale.promotion', string="Promotion")
    promo_line_ids = fields.One2many(comodel_name='promotion.wizard.line', inverse_name='wizard_id')
    apply_line_ids = fields.One2many(comodel_name='promotion.wizard.application', inverse_name='wizard_id')
    main_discount = fields.Float(string="Main discount")

    @api.multi
    def confirm_offer(self):
        self.ensure_one()
        # we create a promotion case
        order = self.order_id
        promo_case = self.env['sale.promotion.case'].create({
            'date': fields.Date.today(),
            'order_id': order.id,
            'partner_id': order.partner_id.id,
            'promotion_id': self.promotion_id.id,
        })
        promo_lines = []
        for line in self.promo_line_ids:
            promo_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.product_id.name,
                'price_unit': line.product_id.list_price,
                'product_uom_qty': line.promoted,
                'discount': 100.0,
                'product_uom': line.product_id.uom_id.id,
                'tax_id': [],
                'is_promotion_line': True,
                'promotion_ids': [(4, promo_case.id)],
            }))

        order.update({'order_line': promo_lines})

        # now we 1) update qty in order line that can be used in new offers
        # TODO: and 2) apply main discount the same quantities (lines shall be split)

        for apply_line in self.apply_line_ids:
            qty_required = apply_line.required
            for so_line in apply_line.so_line_ids:
                available = so_line.product_uom_qty - so_line.promo_qty
                qty = min(available, qty_required)
                so_line.promo_qty += qty
                qty_required -= qty

                so_line.update({'promotion_ids': [(4, promo_case.id)]})


class PromotionWizardLine(models.TransientModel):
    _name = 'promotion.wizard.line'

    # TODO: check dynamic domain on wizard line
    def _get_product_domain(self):
        allowed_prods = self.mapped('wizard_id.promotion_id.item_ids.promotion_rule_lines.id')
        return [('id', 'in', allowed_prods)]

    product_id = fields.Many2one(
        comodel_name='product.product', string="Product",
        # domain=_get_product_domain
    )
    wizard_id = fields.Many2one(comodel_name='promotion.wizard')
    promoted = fields.Float(string="Promoted")


class PromotionWizardApplication(models.TransientModel):
    _name = 'promotion.wizard.application'

    wizard_id = fields.Many2one(comodel_name='promotion.wizard')
    so_line_ids = fields.Many2many(comodel_name='sale.order.line', string='Lines')
    product_id = fields.Many2one('product.product', string="Product")
    required = fields.Float(string="Required")
    available = fields.Float(string="Available")
