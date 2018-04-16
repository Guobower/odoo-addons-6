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
        """at creation, setting the sequence and creating an activity"""

        item = super(AccountMove, self).create(vals)
        if item.journal_id.autom_stat_line and not item.statement_line_id:
            bank_statement = self.env['account.bank.statement'].search([
                ('journal_id', '=', item.journal_id.id),
                ('state', '=', 'open'),
            ])
            if not bank_statement:
                raise UserError(_("There is no open bank statement for this journal. "
                                  "It is therefore not possible to create a bank statement line"))


        return item