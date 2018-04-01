# -*- coding: utf-8 -*-
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Invoicing Plan',
    'summary': """
        Invoicing Plan on Sale Orders""",
    'version': '9.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Odoo Community Association (OCA)',
    'website': 'http://abstract.it',
    'depends': [
        'account', 'sale',
    ],
    'data': [
        'wizards/sale_advance_payment_inv.xml',
        'views/sale_order.xml',
        'security/sale_invoicing_plan.xml',
        'views/sale_invoicing_plan.xml',
    ],
    'demo': [
    ],
}
