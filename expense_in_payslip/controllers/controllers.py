# -*- coding: utf-8 -*-
# from odoo import http


# class ExpenseInPayslip(http.Controller):
#     @http.route('/expense_in_payslip/expense_in_payslip/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/expense_in_payslip/expense_in_payslip/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('expense_in_payslip.listing', {
#             'root': '/expense_in_payslip/expense_in_payslip',
#             'objects': http.request.env['expense_in_payslip.expense_in_payslip'].search([]),
#         })

#     @http.route('/expense_in_payslip/expense_in_payslip/objects/<model("expense_in_payslip.expense_in_payslip"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('expense_in_payslip.object', {
#             'object': obj
#         })
