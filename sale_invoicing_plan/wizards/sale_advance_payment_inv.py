# -*- coding: utf-8 -*-
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):

    _inherit = 'sale.advance.payment.inv'

    advance_payment_method = fields.Selection(
        selection_add=[('invoicing_plan', 'Invoicing Plan')])

    @api.multi
    def create_invoicing_plan(self):
        if self.advance_payment_method == 'invoicing_plan':
            orders = self.env['sale.order'].browse(
                self._context.get('active_ids', []))
            for order in orders:
                if order.invoicing_plan_id:
                    for plan_line in order.invoicing_plan_id.line_ids:
                        if plan_line.amount_type == 'percentage':
                            self.amount = order.amount_untaxed * plan_line.amount / 100
                        elif plan_line.amount_type == 'fixed':
                            self.amount = plan_line.amount
                        self.with_context({'plan_line': plan_line})._create_invoice(
                            order, False, self.amount)


    """
    @api.multi
    def create_invoices(self):
        if self.advance_payment_method == 'invoicing_plan':
                orders = self.env['sale.order'].browse(
                    self._context.get('active_ids', []))
                for order in orders:
                    if order.invoicing_plan_id:
                        for plan_line in order.invoicing_plan_id.line_ids:
                            if plan_line.amount_type == 'percentage':
                                self.amount = order.amount_untaxed * plan_line.amount / 100
                            elif plan_line.amount_type == 'fixed':
                                self.amount = plan_line.amount
                            self.with_context({'plan_line': plan_line})._create_invoice(
                                order, False, self.amount)
                        # set order lines to invoiced. This is needed since
                        # we don't use the action_invoice_create method
                        for order_line in order.order_line:
                            order_line.qty_invoiced = order_line.product_uom_qty
                    else:
                        raise UserError(_("Please select an invoicing plan"))
                if self._context.get('open_invoices', False):
                    return orders.action_view_invoice()
                return {'type': 'ir.actions.act_window_close'}
        else:
            return super(SaleAdvancePaymentInv, self).create_invoices()

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        inv_obj = self.env['account.invoice']
        ir_property_obj = self.env['ir.property']

        if self.advance_payment_method == 'invoicing_plan':
            account_id = False
            if self._context.get('plan_line').product_id.id:
                account_id = self.product_id.property_account_income_id.id
            if not account_id:
                prop = ir_property_obj.get('property_account_income_categ_id', 'product.category')
                prop_id = prop and prop.id or False
                account_id = order.fiscal_position_id.map_account(prop_id)
            if not account_id:
                raise UserError(
                    _('There is no income account defined for this product: "%s". You may have to install a chart of account from Accounting app, settings menu.') % \
                        (self.product_id.name,))

            if self.amount <= 0.00:
                raise UserError(_('The value of the down payment amount must be positive.'))
            if self.advance_payment_method == 'percentage':
                amount = order.amount_untaxed * self.amount / 100
                name = _("Down payment of %s%%") % (self.amount,)
            else:
                amount = self.amount
                name = _('Down Payment')

            date_order = datetime.strptime(order.date_order, "%Y-%m-%d %H:%M:%S")
            date_invoice = date_order + timedelta(
                days=self._context.get('plan_line').days)

            invoice = inv_obj.create({
                'name': order.client_order_ref or order.name,
                'date_invoice': datetime.strftime(
                    date_invoice, "%Y-%m-%d %H:%M:%S"),
                'origin': order.name,
                'type': 'out_invoice',
                'reference': False,
                'account_id': order.partner_id.property_account_receivable_id.id,
                'partner_id': order.partner_invoice_id.id,
                'invoice_line_ids': [(0, 0, {
                    'name': name,
                    'origin': order.name,
                    'account_id': account_id,
                    'price_unit': amount,
                    'quantity': 1.0,
                    'discount': 0.0,
                    'uom_id': self.product_id.uom_id.id,
                    'product_id': self.product_id.id,
                    'invoice_line_tax_ids': [(6, 0, [x.id for x in self.product_id.taxes_id])],
                    'account_analytic_id': order.project_id.id or False,
                })],
                'currency_id': order.pricelist_id.currency_id.id,
                'payment_term_id': order.payment_term_id.id,
                'fiscal_position_id': order.fiscal_position_id.id or order.partner_id.property_account_position_id.id,
                'team_id': order.team_id.id,
                # 'bank_account_id': order.bank_account_id.id
            })
            if invoice:
                # order.unlink_ace()
                invoice.compute_taxes()
                return invoice
        else:
            return super(SaleAdvancePaymentInv, self)._create_invoice(
                order, so_line, amount)
    """
