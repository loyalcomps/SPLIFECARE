# -*- coding: utf-8 -*-
{
    'name': "invoice_homenursing",

    'summary': """
        Sale order creation with timesheet
        """,

    'description': """
         Sale order creation with timesheet
        (qty as total no of shift)
    """,

    'author': "Loyal It solutions PVT LTD",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','caretaker_timesheet'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizard/sale_order_wizard_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
