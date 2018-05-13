# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    riba_line_state = fields.Char(
        string='State', compute='_compute_riba_state')

    payment_term_id = fields.Many2one('account.payment.term',
                                      related='invoice_id.payment_term_id',
                                      string='Payment Terms', store=True)
    riba_line_state = fields.Char(
        string='State',
        compute='_compute_riba_state',
        store=True)

    @api.depends('distinta_line_ids.riba_line_id.state')
    def _compute_riba_state(self):
        for line in self:
            if line.distinta_line_ids:
                states = line.mapped('distinta_line_ids.riba_line_id.state')
                line.riba_line_state = states[0]



