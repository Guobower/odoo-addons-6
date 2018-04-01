# -*- coding: utf-8 -*-
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    invoicing_plan_id = fields.Many2one(
        'sale.invoicing.plan', string='Invoicing Plan')
