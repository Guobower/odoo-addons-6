# coding: utf-8
# @author Giacom Grasso <giacomo.grasso.82@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class RsaSheet(models.Model):
    _name = "rsa.sheet"

    # integrating partner information
    name = fields.Char("Nome")
    date_exec = fields.Char("Execution date")
    date_end = fields.Char("Expiry date")
    task_id = fields.Many2one(comodel_name='project.task', string='Task')
    description = fields.Text("Description")
    installation_id = fields.Many2one(comodel_name='installation.main', string='Intallation')
    condominium_id = fields.Many2one('res.partner', domain=[('condominium', '=', '1')])
    officer_id = fields.Many2one(related='condominium_id.officer_id')
