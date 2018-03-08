# -*- coding: utf-8 -*-


{
    'name': "Open sale order report",
    'summary': """Sale order report with open due dates""",
    'description': """
        Sale order report with open due dates and amounts
    """,
    'version': '10.0.1.0',
    'depends': [
        'sale',
        'account_accountant',
        'sale_order_invoiced_amount',
    ],
    'data': [
        'wizard/report_wizard.xml',
        'reports/sale_order_report.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}
