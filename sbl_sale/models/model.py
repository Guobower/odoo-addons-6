# coding=utf-8

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


class SaleOrderPaymentPlan(models.Model):
    _name = 'sale.order.payment.plan'
    _description = 'Sale Order Payment Plan'
    _order = 'id, sequence'

    sequence = fields.Integer(string='Sequence', default=10)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')

    date = fields.Date(string='Due date', required=True)
    date_real = fields.Date(string='Real date', required=True)
    currency_id = fields.Many2one(
        "res.currency", string="Currency", readonly=True,
        required=True, default=lambda self: self.env.user.company_id.currency_id)
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms')
    amount = fields.Monetary(string='Amount', required=True, track_visibility='always')
    residual = fields.Monetary(string='Residual Amount', default=lambda self: self.amount)
    reconciled = fields.Boolean(string='Payment Reconciled')

    @api.constrains('date_real')
    def check_dates(self):
        """ Real date can not be smaller than the due date"""
        for rec in self:
            if rec.date_real < rec.date:
                raise Warning(_("Real date can not be smaller than due date"))



