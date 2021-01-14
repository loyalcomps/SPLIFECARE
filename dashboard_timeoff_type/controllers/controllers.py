# -*- coding: utf-8 -*-
# from odoo import http


# class DashboardTimeoffType(http.Controller):
#     @http.route('/dashboard_timeoff_type/dashboard_timeoff_type/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dashboard_timeoff_type/dashboard_timeoff_type/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dashboard_timeoff_type.listing', {
#             'root': '/dashboard_timeoff_type/dashboard_timeoff_type',
#             'objects': http.request.env['dashboard_timeoff_type.dashboard_timeoff_type'].search([]),
#         })

#     @http.route('/dashboard_timeoff_type/dashboard_timeoff_type/objects/<model("dashboard_timeoff_type.dashboard_timeoff_type"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dashboard_timeoff_type.object', {
#             'object': obj
#         })
