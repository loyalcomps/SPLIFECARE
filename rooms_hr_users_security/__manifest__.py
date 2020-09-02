# -*- coding: utf-8 -*-
{
    'name': "rooms_hr_users_security",

    'summary': """
        Hr user and Room user security
        """,

    'description': """
        Hide create button (list,form,kanban) in employee,contract,mytime off,caretaker timeoff,
        Hide menu in time off(Every one,Managers,Reporting,configurations),
        Hide menu in payroll(Payment advice,Employee,Payslip,Reporting,Configuration),
        hide room menu

    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','room_chart_management','hr',
                'l10n_in_hr_payroll','hr_holidays','hr_payroll','caretaker_timesheet',
                'hr_contract','hr_timesheet','timesheet_grid'],

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
