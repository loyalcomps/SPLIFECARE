# -*- coding: utf-8 -*-
# from odoo import http


# class CustomerRoomUpdation(http.Controller):
#     @http.route('/customer_room_updation/customer_room_updation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer_room_updation/customer_room_updation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer_room_updation.listing', {
#             'root': '/customer_room_updation/customer_room_updation',
#             'objects': http.request.env['customer_room_updation.customer_room_updation'].search([]),
#         })

#     @http.route('/customer_room_updation/customer_room_updation/objects/<model("customer_room_updation.customer_room_updation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer_room_updation.object', {
#             'object': obj
#         })
