# -*- coding: utf-8 -*-
{
    'name': "customer_invoice_print_splc",

    'summary': """
        Invoice print""",

    'description': """
        Invoice print
    """,

    'author': "Loyal It solutions PVT LTD",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','department_logo'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/layout.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
