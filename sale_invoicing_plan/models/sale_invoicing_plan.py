# -*- coding: utf-8 -*-
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp


class SaleInvoicingPlan(models.Model):

    _name = 'sale.invoicing.plan'
    _description = 'Invoicing Plan'

    name = fields.Char(string='Name')
    line_ids = fields.One2many(
        'sale.invoicing.plan.line', 'plan_id', string='Plan Lines', copy=True)


class SaleInvoicingPlanLine(models.Model):

    _name = 'sale.invoicing.plan.line'
    _description = 'Invoicing Plan Line'

    amount_type = fields.Selection(
        (('percentage', 'Percentage'),
            ('fixed', 'Fixed Amount')),
        string='Type',
        required=True,
        default='percentage')
    amount = fields.Float(
        string='Amount',
        digits=dp.get_precision('Payment Term'))
    days = fields.Integer(string='Number of Days', required=True, default=0)
    plan_id = fields.Many2one('sale.invoicing.plan', string='Invoicing Plan')
    product_id = fields.Many2one('product.product', string='Product')
