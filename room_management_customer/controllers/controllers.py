# -*- coding: utf-8 -*-
# from odoo import http


# class RoomManagementCustomer(http.Controller):
#     @http.route('/room_management_customer/room_management_customer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/room_management_customer/room_management_customer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('room_management_customer.listing', {
#             'root': '/room_management_customer/room_management_customer',
#             'objects': http.request.env['room_management_customer.room_management_customer'].search([]),
#         })

#     @http.route('/room_management_customer/room_management_customer/objects/<model("room_management_customer.room_management_customer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('room_management_customer.object', {
#             'object': obj
#         })
