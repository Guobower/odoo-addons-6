from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class ReportWizard(models.TransientModel):
    _name = 'report.sale_order_open_amounts'

    initial_date = fields.Date("Initial Date", required=True)
    final_date = fields.Date("Final Date", required=True)

    @api.multi
    def print_report(self):
        self.ensure_one()
        data = {
            'initial_date': self.initial_date,
            'final_date': self.final_date,
        }
        return self.env['report'].get_action(
            self.env['sale.order'].search([]),
            "sale_order_due_amount.sale_order_open_amounts",
            data=data
        )


class SOOpenAmountsReport(models.AbstractModel):
    _name = 'report.sale_order_due_amount.sale_order_open_amounts'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('sale_order_due_amount.sale_order_open_amounts')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'orders': self.get_orders(data)
        }

        return report_obj.render('sale_order_due_amount.sale_order_open_amounts', docargs)

    def get_orders(self, data):
        domain = [
            ('date_from', '>=', data['initial_date']),
            ('date_to', '<=', data['final_date']),
            ('order_amount_to_invoice', '>', 0),
        ]
        orders = self.env['sale.order'].search(domain)
        """
        orders = {}
        for item in items:
            key = (item.id, item.name)
            if key not in orders:
                orders[key] = []
            else:
                orders[key].append(item)
        # print orders
        """
        return orders
