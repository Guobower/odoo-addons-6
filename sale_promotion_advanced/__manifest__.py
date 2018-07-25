# -*- coding: utf-8 -*-
{
    'name': "Sale Promotion Advanced",

    'summary': """
        Sale promotion advanced,
        depending on sale_promotion by Cybro.""",

    'description': """
        Sale promotion advanced,
        depending on sale_promotion by Cybro.
    """,

    'author': "Levelprime SRL",
    'website': "http://www.levelprime.com",

    'category': 'Sales Management',
    'version': '10.0.1.0',

    'depends': ['base',
                'account',
                'sale_promotion',
                ],

    'data': [
        'data/data.xml',
        'views/sale_order.xml',
        'views/sale_promotion.xml',
        'wizard/promotion_wizard.xml',
    ],
    'application': False,
    'installable': True,
}
