# coding: utf-8
# @author Giacom Grasso <giacomo.grasso.82@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    task_id = fields.Many2one(
        string="Task",
        comodel_name="project.task")
    installation_id = fields.Many2one(
        string="Installation",
        comodel_name="installation.main")
    condominium_id = fields.Many2one(
        string="Condominium",
        related="installation_id.condominium_id")
    officer_id = fields.Many2one(
        string="Admin./Rappr.",
        comodel_name="res.partner",
        domain=[('officer', "!=", False)])
