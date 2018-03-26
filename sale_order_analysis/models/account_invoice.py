# coding: utf-8
#   @author Giacomo Grasso <giacomo.grasso.82@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    """
    When an invoice is edited, the related sale orders indicators are updated
    """
    sale_analysis = fields.Boolean(string="Analysis", compute="_compute_total_residual", store=True)

    @api.multi  # >> attenzione, originale è @api.one
    @api.depends(
        # 'state', 'currency_id', 'invoice_line_ids.price_subtotal',
        # 'move_id.line_ids.amount_residual',
        # 'move_id.line_ids.currency_id'
        'residual'
        )
    def _compute_total_residual(self):
        sale_orders = self.mapped('invoice_line_ids.sale_line_ids.order_id')
        for order in sale_orders:
            amount_paid, amount_unpaid = order._get_order_paid_amount()

            order.write({
                'order_amount_paid': amount_paid,
                'order_amount_to_pay': order.amount_total - amount_paid,
            })

            # order.order_amount_paid = amount_paid
            # order.order_amount_to_pay = order.amount_total - amount_paid

