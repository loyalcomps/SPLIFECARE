# -*- coding: utf-8 -*-
# from odoo import http


# class AvoidUndefinedSlots(http.Controller):
#     @http.route('/avoid_undefined_slots/avoid_undefined_slots/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/avoid_undefined_slots/avoid_undefined_slots/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('avoid_undefined_slots.listing', {
#             'root': '/avoid_undefined_slots/avoid_undefined_slots',
#             'objects': http.request.env['avoid_undefined_slots.avoid_undefined_slots'].search([]),
#         })

#     @http.route('/avoid_undefined_slots/avoid_undefined_slots/objects/<model("avoid_undefined_slots.avoid_undefined_slots"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('avoid_undefined_slots.object', {
#             'object': obj
#         })
