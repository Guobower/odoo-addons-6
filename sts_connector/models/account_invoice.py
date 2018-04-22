# -*- coding: utf-8 -*-
# © 2017 Giacomo Grasso
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    create_dictionary = fields.Char(
        string='Dictionary',
        compute="compute_dictionary")
    sent_to_sts = fields.Boolean(string="Sent to STS")

    @api.depends('invoice_line_ids')
    def compute_dictionary(self):
        for invoice in self:
            dict = {}
            for line in invoice.invoice_line_ids:
                key = line.product_id.default_code
                if dict.get(key, False):
                    dict[key] += line.price_subtotal
                else:
                    dict[key] = line.price_subtotal
            output = ""
            for k, v in dict.iteritems():
                output += "chiave " + str(k) + " \n"
                output += "valore " + str(v) + "\n"
        invoice.create_dictionary = output