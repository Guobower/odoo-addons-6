# coding: utf-8
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'PSPES project',
    'version': '10.0.1.0.0',
    'category': 'Sale',
    'summary': 'PSPES project',
    'author': "Giacomo Grasso",
    'license': 'AGPL-3',
    'depends': [
        'base',
        'knowledge',
        'sale',
        'sale_timesheet',
        'sales_team',
        'account',
        ],
    'data': [
        'views/product_product.xml',
        'views/installation.xml',
        'views/ir_attachment.xml',
        'views/project_task.xml',
        'views/res_partner.xml',
        'views/rsa_sheet.xml',
        'views/sale_order.xml',
        'views/account_invoice.xml',
    ],
    'installable': True,
}
