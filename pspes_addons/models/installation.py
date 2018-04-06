# coding: utf-8
# @author Giacom Grasso <giacomo.grasso.82@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class InstallationMain(models.Model):
    _name = "installation.main"

    # integrating partner information
    name = fields.Char("Nome")
    inst_type = fields.Char("Type")
    description = fields.Text("Description")
    condominium_id = fields.Many2one('res.partner', domain=[('condominium', '=', '1')])
    officer_id = fields.Many2one(related='condominium_id.officer_id')
