# -*- coding: utf-8 -*-
# © 2017 Giacomo Grasso
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    #
    @api.model
    def create(self, vals):
        """at creation, create if required a bank statement line"""

        item = super(AccountMove, self).create(vals)
        if item.journal_id.autom_stat_line and not item.statement_line_id:
            bank_statements = self.env['account.bank.statement'].search([
                ('journal_id', '=', item.journal_id.id),
                ('state', '=', 'open'),
            ])
            if not bank_statements:
                raise UserError(_("There is no open bank statement for this journal. "
                                  "It is therefore not possible to create a bank statement line."
                                  "Please create one or edit the journal configuration."))
            # different methods are applied to link the statement line to the correct statement
            # 1) take the statement with the date of the move date
            daily_statement = bank_statements.filtered(lambda r: r.date == item.date)
            if daily_statement:
                statement_id = daily_statement[0]

            # TODO: 2) take the statement in which range (most recent or oldest line) this date can be included

            # 3) elsewhere select the most recent statement
            else:
                statement_id = bank_statements.sorted(key=lambda r: r.date)[0]

            # for each bank line in the move we create a statement line
            line = item.line_ids.filtered(
                lambda r: r.account_id.id == item.journal_id.default_debit_account_id.id)
            if len(line) != 1:
                raise UserError(_("There should be at least and only one bank line per move if you want "
                                  "to have automatic bank statement line."))

            # TODO: consider multi-currency application
            # the bank statement line is created
            name = "[{}] {}".format(item.name, line.name)
            amount = line.debit - line.credit
            new_line_data = ({
                'partner_id': line.partner_id.id,
                'name': name,
                'statement_id': statement_id.id,
                'amount': amount,
                'date': item.date,
            })
            new_line = self.env['account.bank.statement.line'].create(new_line_data)
            statement_id.update({'line_ids': [(4, new_line.id)]})

            # we finally link the account move to the statement line, which in turns appears reconciled
            item.statement_line_id = new_line.id

            # moreover, we link the move line to the statement id
            line.statement_id = statement_id.id

        return item

    @api.onchange('statement_line_id')
    def onchange_statement_line(self):
        """
        Account moves for bank/cash journals are sometimes done out of the bank reconciliation or payment
        systems. Therefore it may be needed to reconcile such moves with bank statement lines.

        We create a specific editable tree view with bank moves WITHOUT a link to a bank statement line.
        Once this field is manually set, we link the specific bank line to the bank statement.

        """
        if self.statement_line_id:
            move_lines = self.line_ids.filtered(
                lambda r: r.account_id.id == self.journal_id.default_debit_account_id.id)
            for line in move_lines:
                line.statement_id = self.statement_line_id.statement_id
