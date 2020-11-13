# -*- coding: utf-8 -*-
# from odoo import http


# class DepartmentPayslipBatch(http.Controller):
#     @http.route('/department_payslip_batch/department_payslip_batch/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/department_payslip_batch/department_payslip_batch/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('department_payslip_batch.listing', {
#             'root': '/department_payslip_batch/department_payslip_batch',
#             'objects': http.request.env['department_payslip_batch.department_payslip_batch'].search([]),
#         })

#     @http.route('/department_payslip_batch/department_payslip_batch/objects/<model("department_payslip_batch.department_payslip_batch"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('department_payslip_batch.object', {
#             'object': obj
#         })
