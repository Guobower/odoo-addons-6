# -*- coding: utf-8 -*-
# © 2017 Giacomo Grasso
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields, api, _


class AccountJournal(models.Model):
    _inherit = "account.journal"

    autom_stat_line = fields.Boolean(
        string='Automatic statement line',
        help="If flagged, when an account move with this journal is created, Odoo searches for an open "
             "bank statement and created a statement lines reconciled with this move.")
