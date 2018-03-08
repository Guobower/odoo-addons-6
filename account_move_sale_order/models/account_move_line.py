# coding: utf-8
# author Giacom Grassso <giacomo.grasso.82@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    """Adding on each move line the link to one sale order"""

    sale_order_id = fields.Float(
        string='Sale Order', comodel_name='sale.order')

    @api.model
    def create(self, vals):
        invoice = self.env['account.invoice'].browse(vals['invoice_id'])
        order_list = self.env['sale.order'].search([('invoice_ids', 'in', [invoice.id])])
        # name = "%s%s%s" % (location, vals['code'], vals['pavilion'])
        # vals['name'] = name

        return super(AccountMoveLine, self).create(vals)