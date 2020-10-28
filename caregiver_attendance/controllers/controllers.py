# -*- coding: utf-8 -*-
# from odoo import http


# class CaregiverAttendance(http.Controller):
#     @http.route('/caregiver_attendance/caregiver_attendance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/caregiver_attendance/caregiver_attendance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('caregiver_attendance.listing', {
#             'root': '/caregiver_attendance/caregiver_attendance',
#             'objects': http.request.env['caregiver_attendance.caregiver_attendance'].search([]),
#         })

#     @http.route('/caregiver_attendance/caregiver_attendance/objects/<model("caregiver_attendance.caregiver_attendance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('caregiver_attendance.object', {
#             'object': obj
#         })
