# -*- coding: utf-8 -*-
# from odoo import http


# class IncidentReport(http.Controller):
#     @http.route('/incident_report/incident_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/incident_report/incident_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('incident_report.listing', {
#             'root': '/incident_report/incident_report',
#             'objects': http.request.env['incident_report.incident_report'].search([]),
#         })

#     @http.route('/incident_report/incident_report/objects/<model("incident_report.incident_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('incident_report.object', {
#             'object': obj
#         })
