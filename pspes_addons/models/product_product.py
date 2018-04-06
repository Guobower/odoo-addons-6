# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    create_task = fields.Boolean('Create activity')
