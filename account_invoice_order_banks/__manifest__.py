# -*- coding: utf-8 -*-
#  © 2017 Giacomo Grasso - giacomo.grasso.82@gmail.com
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Invoice and order bank accounts',
    'version': '10.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Adding client and company bank account on invoices and sale order',
    'author': 'Giacomo Grasso - giacomo.grasso.82@gmail.com',
    'website': '',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_accountant',
        'sale'],
    'data': [
        'views/account_invoice.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',

        'report/account_invoice.xml',
        'report/sale_order.xml',
    ],
    'installable': True,
}
