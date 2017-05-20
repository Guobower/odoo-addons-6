# -*- coding: utf-8 -*-
##############################################################################
#
#        MISSING OPEN POINTS IN TESTS
#        - MISSING FINAL BALANCE FINANCIAL FORECASTS!!
#        - SUDO () FOR USER in SETUP
#
##############################################################################

from odoo.addons.account.tests.account_test_users import AccountTestUsers
from datetime import date, timedelta

import logging
_logger = logging.getLogger(__name__)


class TestFinance(AccountTestUsers):

    def setUp(self):
        super(TestFinance, self).setUp()

        # setup accounting data
        self.today = date.today().strftime('%Y-%m-%d')
        self.account_model = self.env['account.account']
        self.move_model = self.env['account.move']
        self.move_line_model = self.env['account.move.line']
        self.journal_model = self.env['account.journal']
        self.bank_stat_model = self.env['account.bank.statement']
        self.forecast_model = self.env['financial.forecast']
        self.template_model = self.env['financial.forecast.template']
        self.company = self.env.ref('base.main_company')

        self.miscellaneous_journal = self.env['account.journal'].search(
            [('type', '=', 'general')])[0]
        self.miscellaneous_journal.update_posted = True  # ???

        # creating unique financial planning account
        account_user_type = self.env.ref('account.data_account_type_receivable')

        self.credit_account = self.account_model.create({
            'code': '1234567',
            'name': 'Testing financial management',
            'financial_planning': True,
            'reconcile': True,
            'user_type_id': account_user_type.id,
        })

        # creating financial managemnt journal and bank statement
        self.journal = self.journal_model.create({
            'name': 'Financial planning journal',
            'type': 'bank',
            'code': 'FINPL',
            'financial_planning': True,
        })

        self.bank_stat = self.bank_stat_model.create({
            'name': 'Virtual bank',
            'journal_id': self.journal.id,
            'date': self.today,
            'balance_start': 1000,
        })

        # create financial forecast
        self.forecast = self.forecast_model.create({
            'name': 'Monthly test forecast',
            'date_start': (date.today() - timedelta(days=5)).strftime('%Y-%m-%d'),
            'date_end': (date.today() + timedelta(days=5)).strftime('%Y-%m-%d'),
            'initial_balance': 2000,
            'company_id': self.company.id,
        })

    def test_account_move_financial(self):
        # create account move
        self.move = self.move_model.create({
            'journal_id': self.miscellaneous_journal.id,
            'date': self.today,
            'ref': 'Test financial account move',
            })

        # create credit move line
        credit_line = self.move_line_model.with_context(
            check_move_validity=False).create({
                'move_id': self.move.id,
                'account_id': self.credit_account.id,
                'name': 'Test credit line',
                'credit': 200,
                'date_maturity': self.today,
            })

        # create credit move line
        debit_line = self.move_line_model.create({
            'move_id': self.move.id,
            'account_id': self.credit_account.id,
            'name': 'Test debit line',
            'debit': 200,
            'date_maturity': self.today,
            })

        self.move.post()
        self.assertEqual(
            self.forecast.receivables,
            200)

        self.assertEqual(
            self.forecast.payables,
            -200)

    """
    def test_financial_recurrent_costs(self):
        # create forecast template and lines
        self.forecast_template = self.template_model.create({
            'name': 'Generic month',
            'bank_statement_id': self.bank_stat.id,
            'company_id': self.company.id,
        })
    """
