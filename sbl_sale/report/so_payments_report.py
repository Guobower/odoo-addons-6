# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models
from datetime import date


class CashFlowReport(models.Model):
    _name = "sale.order.payment.report"
    _description = "SO payments"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    sale_order_id = fields.Many2one('sale.order', 'Sale Order', readonly=True)
    date = fields.Date('Due date', readonly=True)
    currency_id = fields.Many2one("res.currency", "Currency", readonly=True)
    payment_term_id = fields.Many2one('account.payment.term', 'Payment Terms', readonly=True)
    amount = fields.Monetary('Amount', readonly=True)
    residual = fields.Monetary('Residual Amount', readonly=True)
    reconciled = fields.Boolean('Payment Reconciled', readonly=True)

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self._get_main_query()

    def _select(self):
        date_from = self._context.get('date_from', False)
        date_to = self._context.get('date_to', False)

        if date_from or date_to:
            domain = "CASE"
            domain += "WHEN sopp.date < '{}' THEN '{}'".format(
                date_from, date_from) if date_from else ""
            domain += "WHEN sopp.date > '{}' THEN '{}'".format(
                date_to, date_to) if date_to else ""
            domain += "ELSE sopp.date END as date,"
        else:
            domain = "sopp.date as date,"

        select_str = """
            WITH currency_rate as ({})
            SELECT min(sopp.id) as id,
                so.name as order,
                sopp.sale_order_id as sale_order,
                {}
                sopp.payment_term_id as pay_term,
                sopp.residual as residual,
                sopp.amount as amount,
                sopp.reconciled as reconciled
        """.format(self.env['res.currency']._select_companies_rates(), domain)
        return select_str

    def _from(self):
        from_str = """
            sale_order_payment_plan sopp
            LEFT JOIN sale_order so ON (sopp.sale_order_id = so.id)

        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                sopp.id,
                sopp.date,
                sopp.payment_term_id,
                sopp.amount,
                sopp.residual,
                sopp.reconciled,
                sopp.sale_order_id,
                so.name
        """
        return group_by_str

    def _get_main_query(self):
        # self._table = sale_report
        main_query = """
            CREATE or REPLACE VIEW {} as (
            {}
            FROM  {}
            {}
            )

            """.format(self._table, self._select(),
                        self._from(), self._group_by())
        print main_query
        self.env.cr.execute(main_query)
