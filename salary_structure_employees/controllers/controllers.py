# -*- coding: utf-8 -*-
# from odoo import http


# class SalaryStructureEmployees(http.Controller):
#     @http.route('/salary_structure_employees/salary_structure_employees/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/salary_structure_employees/salary_structure_employees/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('salary_structure_employees.listing', {
#             'root': '/salary_structure_employees/salary_structure_employees',
#             'objects': http.request.env['salary_structure_employees.salary_structure_employees'].search([]),
#         })

#     @http.route('/salary_structure_employees/salary_structure_employees/objects/<model("salary_structure_employees.salary_structure_employees"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('salary_structure_employees.object', {
#             'object': obj
#         })
