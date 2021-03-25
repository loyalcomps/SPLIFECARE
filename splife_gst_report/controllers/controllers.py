# -*- coding: utf-8 -*-
# from odoo import http


# class SplifeGstReport(http.Controller):
#     @http.route('/splife_gst_report/splife_gst_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/splife_gst_report/splife_gst_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('splife_gst_report.listing', {
#             'root': '/splife_gst_report/splife_gst_report',
#             'objects': http.request.env['splife_gst_report.splife_gst_report'].search([]),
#         })

#     @http.route('/splife_gst_report/splife_gst_report/objects/<model("splife_gst_report.splife_gst_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('splife_gst_report.object', {
#             'object': obj
#         })
