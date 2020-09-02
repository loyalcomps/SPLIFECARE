# -*- coding: utf-8 -*-
# from odoo import http


# class RoomsHrUsersSecurity(http.Controller):
#     @http.route('/rooms_hr_users_security/rooms_hr_users_security/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rooms_hr_users_security/rooms_hr_users_security/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rooms_hr_users_security.listing', {
#             'root': '/rooms_hr_users_security/rooms_hr_users_security',
#             'objects': http.request.env['rooms_hr_users_security.rooms_hr_users_security'].search([]),
#         })

#     @http.route('/rooms_hr_users_security/rooms_hr_users_security/objects/<model("rooms_hr_users_security.rooms_hr_users_security"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rooms_hr_users_security.object', {
#             'object': obj
#         })
