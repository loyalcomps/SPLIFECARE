# -*- coding: utf-8 -*-
# from odoo import http


# class IncidentReportSecurity(http.Controller):
#     @http.route('/incident_report_security/incident_report_security/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/incident_report_security/incident_report_security/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('incident_report_security.listing', {
#             'root': '/incident_report_security/incident_report_security',
#             'objects': http.request.env['incident_report_security.incident_report_security'].search([]),
#         })

#     @http.route('/incident_report_security/incident_report_security/objects/<model("incident_report_security.incident_report_security"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('incident_report_security.object', {
#             'object': obj
#         })
