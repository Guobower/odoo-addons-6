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
        'sale',
        'account',
        ],
    'data': [
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/account_invoice.xml',
    ],
    'installable': True,
}
