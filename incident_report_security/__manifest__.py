# -*- coding: utf-8 -*-
{
    'name': "incident_report_security",

    'summary': """
        user security for incident report""",

    'description': """
      user security for incident report
      """,

     'author': "Loyal IT Solutions Pvt. Ltd.",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','incident_report'],

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
