# -*- coding: utf-8 -*-
{
    'name': "salary_hike_security",

    'summary': """
       user wise salary hike """,

    'description': """
        user wise security for salary hike 
    """,

    'author': "Loyal It solutions PVT.LTD",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','employee_salary_hike_form'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
