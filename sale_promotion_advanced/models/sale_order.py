# coding=utf-8

from dateutil import parser
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    promotion_ids = fields.Many2many(
        comodel_name='sale.promotion.case',
        relation='so_line_promotion_rel',
        column1='promotion_id',
        column2='order_line_id',
        string="Promotions",
        help="Each order line is linked to a specific promotion application, "
             "called promotion 'case', with unique number.")
    promo_qty = fields.Float(
        string="Prom.",
        help="Number of products already included in some promotions.")
    show_promo_details = fields.Boolean(related='order_id.show_promo_details')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    promotion_case_ids = fields.One2many(
        comodel_name='sale.promotion.case', string="Promotions",
        inverse_name="order_id")
    show_promo_details = fields.Boolean('Show promo details')

    @api.multi
    def button_dump_sale_promotion(self):
        """This method creates a wizard for promotion management."""
        for order in self:
            if not order.sale_promotion_id:
                raise UserError(_('Please Select a Promotion Rule.'))

            date_order = parser.parse(order.date_order).strftime('%Y-%m-%d')
            # for each promotion line we create a promotion wizard
            wizard_obj = self.env['promotion.wizard']
            wizard = wizard_obj.create({
                'order_id': order.id,
                'promotion_id': order.sale_promotion_id.id,
            })

            # for each promotion rule, we add data to the wizard
            for rule in order.sale_promotion_id.item_ids:
                apply_lines = []
                promo_lines = []
                if (rule.date_start and rule.date_start >= date_order or
                        rule.date_end and rule.date_end <= date_order):
                    continue

                # compiling the list of products to which apply the promotion
                prod_list = rule.return_products()
                for prod in prod_list:
                    apply_lines.append((0, 0, {
                        'product_id': prod[0].id,
                        'required': prod[1],
                    }))

                # add promoted products that shall be added to the the SO
                for rule_line in rule.promotion_rule_lines:
                    promo_lines.append((0, 0, {
                        'product_id': rule_line.product_id.id,
                        'promoted': rule_line.quantity,
                    }))

                # we copy the main discount to the wizard
                wizard.main_discount = rule.main_discount

                # once we have all required products, we update the wizard
                wizard.update({
                    'apply_line_ids': apply_lines,
                    'promo_line_ids': promo_lines,
                })

                # updating wizard promotion lines with available products
                for line in order.order_line:
                    if line.is_promotion_line:
                        continue
                    prod_line = wizard.apply_line_ids.filtered(
                        lambda l: l.product_id.id == line.product_id.id)
                    if prod_line:
                        line_available = line.product_uom_qty - line.promo_qty
                        prod_line[0].update({
                            'so_line_ids': [(4, line.id)],
                            'available': prod_line.available + line_available,
                        })
                # check if promo is available
                wizard.available = True
                for check in wizard.apply_line_ids:
                    if check.required > check.available:
                        wizard.available = False

            view_id = self.env.ref('sale_promotion_advanced.promotion_wizard_form')
            return {'type': 'ir.actions.act_window',
                    'res_model': 'promotion.wizard',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'target': 'new',
                    'res_id': wizard.id,
                    'view_id': view_id.id,
                    }
