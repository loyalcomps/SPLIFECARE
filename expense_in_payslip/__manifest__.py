# -*- coding: utf-8 -*-
{
    'name': "expense_in_payslip",

    'summary': """
        Expense in payslip""",

    'description': """
    Expense in payslip
    
    1.write salary rule for employee 
               
        result=0
        s=0
        if payslip.hr_expense_sheet_ids:
            for expense in payslip.hr_expense_sheet_ids:
                for payslips in expense.expense_line_ids:
                    s+=payslips.total_amount
           
        result =s
    """,

    'author': "Loyal IT Solutions PVT LTD",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_expense','hr_payroll'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/hr_expense.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
