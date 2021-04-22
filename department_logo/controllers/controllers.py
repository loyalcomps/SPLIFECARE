# -*- coding: utf-8 -*-
# from odoo import http


# class DepartmentLogo(http.Controller):
#     @http.route('/department_logo/department_logo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/department_logo/department_logo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('department_logo.listing', {
#             'root': '/department_logo/department_logo',
#             'objects': http.request.env['department_logo.department_logo'].search([]),
#         })

#     @http.route('/department_logo/department_logo/objects/<model("department_logo.department_logo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('department_logo.object', {
#             'object': obj
#         })
