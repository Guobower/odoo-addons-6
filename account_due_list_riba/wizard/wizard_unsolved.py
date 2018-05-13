# -*- coding: utf-8 -*-

from odoo import fields, models, _, api
from odoo.exceptions import UserError


class RibaUnsolved(models.TransientModel):
    _inherit = "riba.unsolved"

    def create_move(self):
        """Once the unsolved/unpaid move has been created, we edit
        reconciliations in order to open again the original invoice"""
        res = super(RibaUnsolved, self).create_move()
        to_be_settled = self.env['account.move.line']
        move = self.env['account.move'].browse(res['res_id'])

        # new unpaid line
        unpaid_acc = self._get_overdue_effects_account_id()
        unpaid_line = move.line_ids.filtered(lambda r: r.account_id.id == unpaid_acc)
        to_be_settled |= unpaid_line

        # we get the unpaid line and its offset line
        effects_acc = self._get_effects_account_id()
        effects_line = move.line_ids.filtered(lambda r: r.account_id.id == effects_acc)
        offset_line = effects_line.full_reconcile_id.reconciled_line_ids.filtered(
            lambda r: r.id != effects_line.id)
        if not offset_line:
            raise UserError(_("The acceptance/advance account in configuration has been changed,"
                              " it is not possible to reopen the invoice. Please register the"
                              " operation manually or edit the configuration. "))

        # from the offset line we get the original invoice line
        other_line = offset_line[0].move_id.line_ids.filtered(
            lambda r: r.id != offset_line.id)
        invoice_line = other_line[0].full_reconcile_id.reconciled_line_ids.filtered(
            lambda r: r.id != other_line.id)[0]
        to_be_settled |= other_line

        # we now change the reconciliation
        invoice_line.remove_move_reconcile()
        invoice_line.update({'distinta_line_ids': [(5, )]})
        to_be_settled.reconcile()

        return move

