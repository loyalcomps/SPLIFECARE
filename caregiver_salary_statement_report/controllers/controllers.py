# -*- coding: utf-8 -*-
# from odoo import http


# class CaregiverSalaryStatement(http.Controller):
#     @http.route('/caregiver_salary_statement_report/caregiver_salary_statement_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/caregiver_salary_statement_report/caregiver_salary_statement_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('caregiver_salary_statement_report.listing', {
#             'root': '/caregiver_salary_statement_report/caregiver_salary_statement_report',
#             'objects': http.request.env['caregiver_salary_statement_report.caregiver_salary_statement_report'].search([]),
#         })

#     @http.route('/caregiver_salary_statement_report/caregiver_salary_statement_report/objects/<model("caregiver_salary_statement_report.caregiver_salary_statement_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('caregiver_salary_statement_report.object', {
#             'object': obj
#         })
