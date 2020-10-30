# -*- coding: utf-8 -*-
# from odoo import http


# class SalaryHikeSecurity(http.Controller):
#     @http.route('/salary_hike_security/salary_hike_security/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/salary_hike_security/salary_hike_security/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('salary_hike_security.listing', {
#             'root': '/salary_hike_security/salary_hike_security',
#             'objects': http.request.env['salary_hike_security.salary_hike_security'].search([]),
#         })

#     @http.route('/salary_hike_security/salary_hike_security/objects/<model("salary_hike_security.salary_hike_security"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('salary_hike_security.object', {
#             'object': obj
#         })
