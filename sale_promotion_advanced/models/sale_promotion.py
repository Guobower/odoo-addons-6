# coding=utf-8

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SalePromotion(models.Model):
    _inherit = 'sale.promotion'

    @api.constrains('item_ids')
    def checking_rule_line_type(self):
        """
        Constrains verify that all promotion rule lines are applied to the same type,
        either product, product category or kit.
        """
        for rec in self:
            types = [x.applied_on for x in rec.item_ids]
            if len(set(types)) > 1:
                raise UserError(_("All rule lines shall be applied to the same type, "
                                  "either product or product category"))

            prods = [x.product_tmpl_id.id for x in rec.item_ids]
            if len(set(prods)) > 1:
                raise UserError(_("There shall be only one rule for each product"))

            categ = [x.categ_id.id for x in rec.item_ids]
            if len(set(categ)) > 1:
                raise UserError(_("There shall be only one rule for each product"))
        return True


class SalePromotionRule(models.Model):
    _inherit = 'sale.promotion.rule'

    applied_on = fields.Selection(
        selection_add=[('kit', 'Kit')],)
    kit_line_ids = fields.One2many(
        comodel_name='sale.promotion.kit.line', string="Kit lines",
        inverse_name='kit_promo_id', help="Lines to which the promotion is applied")
    main_discount = fields.Float(
        string="Main discount",
        help="This main discount is applied to all the product to which the "
             "rule is applied, i.e. single product, category or kit.")

    @api.onchange('applied_on')
    def onchange_applied_on(self):
        # while changing the rule application, the configuration is reset
        self.update({
            'categ_id': False,
            'product_tmpl_id': False,
            'categ_id': [(5, 0, 0)]}
        )

    @api.multi
    def return_products(self):
        """This method returns a list of tuples, with product
        and required quantity for each promotion rule."""
        self.ensure_one()
        prod_list = []
        if self.applied_on == 'product':
            prod_list.append((self.product_tmpl_id, self.min_quantity))

        if self.applied_on == 'kit':
            for kit_line in self.kit_line_ids:
                prod_list.append((kit_line.product_id, kit_line.qty_required))

        return prod_list


class SalePromotionApplication(models.Model):
    _name = 'sale.promotion.kit.line'

    kit_promo_id = fields.Many2one(comodel_name='sale.promotion.rule', string="Promotion")
    product_id = fields.Many2one(comodel_name='product.product', string="Product")
    qty_required = fields.Float(string="Qty required")


class SalePromotionCase(models.Model):
    _name = 'sale.promotion.case'

    def _default_name(self):
        obj_sequence = self.env['ir.sequence']
        return obj_sequence.next_by_code('promotion.case.sequence')

    name = fields.Char(string='Name', default=_default_name,
                       required=True)
    date = fields.Date(string="Date")
    date_maturity = fields.Date(string="Date Maturity")
    order_id = fields.Many2one(comodel_name='sale.order', string="Order")
    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner")
    promotion_id = fields.Many2one(comodel_name='sale.promotion', string="Promotion")
    order_line_ids = fields.Many2many(
        comodel_name='sale.order.line',
        relation='so_line_promotion_rel',
        column1='order_line_id',
        column2='promotion_id',
        string="Order lines",
        help="Each promotion can be related to multiple order lines")

    @api.multi
    def unlink(self):
        """When deleting a promotion case we also update the amount of
        promotion quantity on each order line, and we delete all the
        new promotion lines added."""
        for promo_case in self:
            promotion = promo_case.promotion_id
            if not promo_case.order_line_ids:
                raise UserError(_("There are no order lines connected"))

            prod_list = []
            for rule in promotion.item_ids:
                prod_list += rule.return_products()

            # update the sale order lines on which the promotion has been computed
            for prod in prod_list:
                so_lines = promo_case.order_line_ids.filtered(
                    lambda l: (l.product_id.id == prod[0].id and not l.is_promotion_line))
                available = prod[1]
                for line in so_lines:
                    if available <= line.promo_qty:
                        line.promo_qty -= available
                        available = 0
                    else:
                        available -= line.promo_qty
                        line.promo_qty = 0

            # delete all the promotion lines created for that promotion
            promo_lines = promo_case.order_line_ids.filtered(
                lambda l: l.is_promotion_line)
            for promo in promo_lines:
                promo.unlink()
        return super(SalePromotionCase, self).unlink()
