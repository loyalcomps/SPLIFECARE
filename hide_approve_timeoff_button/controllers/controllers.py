# -*- coding: utf-8 -*-
# from odoo import http


# class HideApproveTimeoffButton(http.Controller):
#     @http.route('/hide_approve_timeoff_button/hide_approve_timeoff_button/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hide_approve_timeoff_button/hide_approve_timeoff_button/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hide_approve_timeoff_button.listing', {
#             'root': '/hide_approve_timeoff_button/hide_approve_timeoff_button',
#             'objects': http.request.env['hide_approve_timeoff_button.hide_approve_timeoff_button'].search([]),
#         })

#     @http.route('/hide_approve_timeoff_button/hide_approve_timeoff_button/objects/<model("hide_approve_timeoff_button.hide_approve_timeoff_button"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hide_approve_timeoff_button.object', {
#             'object': obj
#         })
