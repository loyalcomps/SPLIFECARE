# -*- coding: utf-8 -*-
# from odoo import http


# class RecruitmentSecurity(http.Controller):
#     @http.route('/recruitment_security/recruitment_security/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/recruitment_security/recruitment_security/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('recruitment_security.listing', {
#             'root': '/recruitment_security/recruitment_security',
#             'objects': http.request.env['recruitment_security.recruitment_security'].search([]),
#         })

#     @http.route('/recruitment_security/recruitment_security/objects/<model("recruitment_security.recruitment_security"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('recruitment_security.object', {
#             'object': obj
#         })
