# coding: utf-8
# @author Giacom Grasso <giacomo.grasso.82@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = "project.task"

    installation_id = fields.Many2one(
        string="Installation",
        comodel_name="installation.main")
    officer_id = fields.Many2one(
        string="Admin./Rappr.",
        comodel_name="res.partner",
        domain=[('officer', "!=", False)])

    pspes_doc_ids = fields.One2many(
        string="Documents",
        comodel_name="ir.attachment",
        inverse_name="pspes_task_id",)

    rsa_ids = fields.One2many(
        string="RSA",
        comodel_name="rsa.sheet",
        inverse_name="task_id",)