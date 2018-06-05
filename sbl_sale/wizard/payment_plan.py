# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime
from odoo import tools


class PaymentPlanAnalysis(models.TransientModel):
    _name = "sale.order.payment.plan.analysis"

    date_to = fields.Date(string='Date to')
    payment_plan_selection = fields.Selection([
        ('normal', 'Payment Order Aging'),
        ('intervals', 'Payment Order Relative Day Intervals')],
        default='normal', string='Payment Analysis Selection',
        required=True)
    date_from = fields.Date(string='Reference Date', default=lambda r: fields.Date.today())
    intervals = fields.Integer(default=7, string='Days From Reference')
    line_analysis_ids = fields.One2many('sale.order.payment.plan.analysis.details', 'line_analysis_id')
    include_invoices = fields.Boolean('Include invoices')

    @api.multi
    def analysis_upload(self):
        # Select the right context depending by wizard selection
        groupby_context = 'days' if self.payment_plan_selection == 'intervals' else 'date_due:month'

        # importing sale orders
        orders = self.env['sale.order'].search([
            ('state', 'in', ['sale']),
            ('payment_plan_residual', '>', 0),
        ])
        payment_details = []
        for order in orders:
            for payment_plan in order.payment_plan_ids.filtered(lambda r: r.residual > 0.00):

                if self.date_from and payment_plan.date < self.date_from:
                    date_due = self.date_from
                elif self.date_to and payment_plan.date > self.date_to:
                    date_due = self.date_to
                else:
                    date_due = payment_plan.date

                # if report is needed based on date intervals
                date_from = datetime.strptime(self.date_from, tools.DEFAULT_SERVER_DATE_FORMAT)
                date_due2 = datetime.strptime(payment_plan.date, tools.DEFAULT_SERVER_DATE_FORMAT)
                days_diff = (date_due2 - date_from).days
                days = int(days_diff / self.intervals) * self.intervals

                payment_details.append((0, 0, {
                    'name': order.name,
                    'amount': payment_plan.amount,
                    'residual': payment_plan.residual,
                    'type': 'order',
                    'user_id': order.user_id.id,
                    'partner_id': order.partner_id.id,
                    'create_date': order.create_date,
                    'confirmation_date': order.confirmation_date,
                    'payment_term_id': order.payment_term_id.id,
                    'status': order.state,
                    'date_due': date_due,
                    'days': days,
                }))

        # import deadlines from invoices
        if self.include_invoices:
            move_lines = self.env['account.move.line'].search([
                ('account_id.internal_type', 'in', ['receivable']),
                ('invoice_id', '!=', False),
                ('amount_residual', '>', 0),
            ])
            for ml in move_lines:

                if self.date_from and ml.date_maturity < self.date_from:
                    date_due = self.date_from
                elif self.date_to and ml.date_maturity > self.date_to:
                    date_due = self.date_to
                else:
                    date_due = ml.date_maturity

                # if report is needed based on date intervals
                date_from = datetime.strptime(self.date_from, tools.DEFAULT_SERVER_DATE_FORMAT)
                date_due2 = datetime.strptime(ml.date_maturity, tools.DEFAULT_SERVER_DATE_FORMAT)
                days_diff = (date_due2 - date_from).days
                days = int(days_diff / self.intervals) * self.intervals
                invoice = ml.invoice_id
                payment_details.append((0, 0, {
                    'name': invoice.number,
                    'amount': ml.balance,
                    'residual': ml.amount_residual,
                    'type': 'invoice',
                    'user_id': invoice.user_id.id,
                    'partner_id': invoice.partner_id.id,
                    'create_date': order.create_date,
                    'confirmation_date': invoice.date_invoice,
                    'payment_term_id': invoice.payment_term_id.id,
                    'status': invoice.state,
                    'date_due': date_due,
                    'days': days,
                }))

        # update the wizard with payment lines
        self.update({'line_analysis_ids': payment_details})

        return {
            'name': _('Payment Analysis'),
            'views': [
                (self.env.ref('sbl_sale.payment_plan_analysis_pivot').id, 'pivot'),
            ],
            'type': 'ir.actions.act_window',
            'view_mode': 'pivot',
            'res_model': 'sale.order.payment.plan.analysis.details',
            'domain': [('line_analysis_id', '=', self.id)],
            'flags': {
                'action_buttons': False,
                'sidebar': False,
            },
            'context': {
                'pivot_column_groupby': [groupby_context],
            }
        }


class PaymentPlanAnalysisDetails(models.TransientModel):
    _name = "sale.order.payment.plan.analysis.details"
    _order = "days"

    line_analysis_id = fields.Many2one('sale.order.payment.plan.analysis', ondelete='cascade')

    type = fields.Selection([
        ('order', 'Order'),
        ('invoice', 'Invoice'),
        ], string='Type', store=True)
    user_id = fields.Many2one('res.users', string='Salesman', store=True)
    partner_id = fields.Many2one('res.partner', string='Customer', store=True)
    payment_plan_id = fields.Many2one('sale.order.payment.plan', ondelete='cascade', string="Payment", store=True)

    create_date = fields.Datetime(string='Creation Date', store=True)
    status = fields.Char(string='Status', store=True)
    confirmation_date = fields.Datetime(string='Confirmation Date', store=True)
    payment_term_id = fields.Many2one('account.payment.term', string='Order Payment Terms', store=True)

    name = fields.Char(string='Name', store=True)
    amount = fields.Monetary('Amount', store=True)
    residual = fields.Monetary('Residual', store=True)
    date_due = fields.Date(string='Due date', store=True)
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    days = fields.Integer(string='Days', store=True)
