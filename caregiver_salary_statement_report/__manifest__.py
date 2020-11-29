# -*- coding: utf-8 -*-
{
    'name': "caregiver_salary_statement_report",

    'summary': """
        caregiver_salary_statement_report""",

    'description': """
    salary rule category for travel expense with code 'TRAVEL'
    salary rule category for advance with code 'ADV'

    """,

    'author': "LOYAL IT SOLUTIONS PVT LTD",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
      'depends': ['base','sale','hr_payroll','report_xlsx',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
