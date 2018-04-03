# coding: utf-8
# @author Giacom Grasso <giacomo.grasso.82@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    # integrating partner information
    condominium = fields.Boolean("Condominio")
    officer = fields.Boolean("Admin./Rappr.")
    legal_repr = fields.Boolean("Rapp. Legale")

    # links among contacts
    officer_id = fields.Many2one(
        string="Admin./Rappr.",
        comodel_name="res.partner",
        domain=[('officer', "!=", False)])
    condominium_ids = fields.One2many(
        string="Condomini",
        comodel_name="res.partner",
        inverse_name="officer_id",
        domain=[('condominium', "!=", False)])

    # condominium properties
    n_apart = fields.Integer("Appartamenti")
    add_notes = fields.Text("Note condominio")

