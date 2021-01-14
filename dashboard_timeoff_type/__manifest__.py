# -*- coding: utf-8 -*-
{
    'name': "dashboard_timeoff_type",

    'summary': """
         Available Time off Type In Dashboard""",

    'description': """
       Available time of type field when 'Include Time Off Type' mark as True
    """,

    'author': "Loyal IT Solutions PVT LTD",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_holidays'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        'views/templates.xml',
        'views/views.xml',
    ],
    'qweb':  ['static/src/xml/pos.xml'],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
