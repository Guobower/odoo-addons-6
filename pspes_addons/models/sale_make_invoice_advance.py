# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        res = super(SaleAdvancePaymentInv, self)._create_invoice(self, order, so_line, amount)

        sale_orders = self.mapped('invoice_line_ids.sale_line_ids.order_id')
        officer_id = sale_orders[0] if sale_orders else False
        res.officer_id = officer_id.id

        return res