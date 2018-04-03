# coding: utf-8
#   @author Giacomo Grasso <giacomo.grasso.82@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    # links among contacts
    officer_id = fields.Many2one(
        string="Admin./Rappr.",
        comodel_name="res.partner",
        domain=[('officer', "!=", False)])