# -*- coding: utf-8 -*-
{
    'name': "splife_goods_print",

    'summary': """
       splife_goods_print""",

    'description': """
        splife_goods_print
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/hsn_security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/hsn_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
