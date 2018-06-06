# coding=utf-8

from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo import tools


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_plan_id = fields.Many2one(
        comodel_name='account.payment.term', string='Payment plan')
    payment_plan_ids = fields.One2many(
        'sale.order.payment.plan', 'sale_order_id',
        string='Payment Plan', ondelete='cascade')
    payment_plan_amount = fields.Monetary(
        string='Payment Plan Amount', compute='_compute_payment_plan_amount')
    payment_plan_residual = fields.Monetary(
        string='Payment Plan Residual', compute='_compute_payment_plan_residual')
    payment_plan_amount_total = fields.Monetary(
        related='amount_total', readonly=True)

    @api.multi
    def write(self, vals):
        sale = super(SaleOrder, self).write(vals)

        # in case of missing payment plan, we create one line
        # which is always compulsory for reporting issue
        if not self.payment_plan_ids and self.payment_plan_id:
            self.compute_payment_deadlines()
        elif not self.payment_plan_ids and not self.payment_plan_id:
            date = datetime.strptime(self.date_order, tools.DEFAULT_SERVER_DATETIME_FORMAT).date()
            self.update({'payment_plan_ids':
                             [(0, 0, {
                                 'date': date,
                                 'date_real': date,
                                 'amount': self.amount_total,
                                 'residual': self.amount_total,
                                 'payment_term_id': self.payment_term_id.id,
                             })]
                         })

        # payment plan shall be recomputed
        if any([i in ['payment_plan_ids', 'amount_untaxed'] for i in vals]):
            self._compute_payment_plan_reconcile()

        # payment plan shall be recomputed
        if self.payment_plan_ids:
            if (self.payment_plan_amount != self.amount_total and
                    self.env.context.get('payment_plan_validation', True)):
                raise UserError(_('Payment plan amount {} differ from '
                                        'Sale Order total amount {}'.format(
                                            self.payment_plan_amount, self.amount_total)))

        # in case of changes to the SO we recompute the reconciliation
        if any([i in ['payment_plan_ids', 'amount_untaxed'] for i in vals]):
            self._compute_payment_plan_reconcile()

        return sale

    @api.multi
    def compute_payment_deadlines(self):
        for order in self.with_context(uncheck=True):
            if not order.payment_plan_id:
                raise UserError(_("Please select a payment plan."))
            # remove existing payment terms
            terms_list = [(5, 0, {})]

            # creating new payment terms
            due_list = order.payment_plan_id.compute(
                order.amount_total, order.date_order)[0]

            for term in due_list:
                terms_list.append((0, 0, {
                    'date': term[0],
                    'date_real': term[0],
                    'amount': term[1],
                    'residual': term[1],
                    'payment_term_id': order.payment_term_id.id,
                    }))
            order.update({'payment_plan_ids': terms_list})

            # compute again the residual of each line
            order._compute_payment_plan_reconcile()

    @api.depends('payment_plan_ids.amount')
    def _compute_payment_plan_amount(self):
        for record in self:
            amount_total = 0.0
            if record.payment_plan_ids:
                for payment in record.payment_plan_ids:
                    amount_total += payment.amount
            record.payment_plan_amount = amount_total

    @api.depends('payment_plan_ids.residual')
    def _compute_payment_plan_residual(self):
        for record in self:
            residual_total = 0.0
            if record.payment_plan_ids:
                for payment in record.payment_plan_ids:
                    residual_total += payment.residual
            record.payment_plan_residual = residual_total

    def _compute_payment_plan_reconcile(self):
        for record in self:
            if record.payment_plan_ids:
                # we interested in emitted invoices and customer refund which are open and paid, for those
                # we calculate all the amount emitted that has to be reconciled over the payment plan
                total_residual = sum(record.invoice_ids.\
                                     filtered(lambda r: r.state in ['open', 'paid'] and r.type in ['out_invoice','out_refund']).\
                                     mapped(lambda r: r.amount_total if r.type == 'out_invoice' else -r.amount_total))
                # Loop over the payment plan sorted by date and update the residual
                for payment_plan in record.payment_plan_ids.sorted(key=lambda r: r.date):
                    if total_residual >= payment_plan.amount:
                        payment_plan.update({'residual': 0.0, 'reconciled': True})
                        total_residual -= payment_plan.amount
                    else:
                        payment_plan.update({'residual': payment_plan.amount - total_residual, 'reconciled': False})
                        total_residual = 0
