# coding: utf-8
# @author Giacom Grasso <giacomo.grasso.82@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class RsaSheet(models.Model):
    _name = "rsa.sheet"

    # integrating partner information
    name = fields.Char("Nome", required=True)
    date_exec = fields.Date("Execution date", required=True)
    date_end = fields.Date("Expiry date", required=True)
    task_id = fields.Many2one(comodel_name='project.task', string='Task', required=True)
    description = fields.Text("Description")
    installation_id = fields.Many2one(comodel_name='installation.main', string='Intallation', required=True)
    condominium_id = fields.Many2one('res.partner', domain=[('condominium', '=', '1')], required=True)
    officer_id = fields.Many2one(related='condominium_id.officer_id')

    # questions
    question_01 = fields.Char("Quest. 01", copy=True)
    question_02 = fields.Boolean("Quest 02", copy=True)
