# -*- coding: utf-8 -*-
# © 2017 Giacomo Grasso
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
{
    'name': 'Automatic bank statement line',
    'version': '10.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Creates statement line at bank account move creation',
    'author': 'giacomo.grasso.82@gmail.com',
    'website': '',
    'license': 'AGPL-3',
    'depends': [
        'account'],
    'data': [
        'views/account_journal.xml',
        'views/account_move.xml',
    ],
    'installable': True,
}
