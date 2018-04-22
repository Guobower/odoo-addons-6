# -*- coding: utf-8 -*-
# © 2017 Giacomo Grasso - Agile Business Group
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Invoice and order bank accounts',
    'version': '10.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Adding client and company bank account on invoices and sale order',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_accountant'],
    'data': [
        'views/account_invoice.xml',
    ],
    'installable': True,
}
