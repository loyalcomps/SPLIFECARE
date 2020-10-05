# -*- coding: utf-8 -*-
# from odoo import http


# class RoomChartUpdation(http.Controller):
#     @http.route('/room_chart_updation/room_chart_updation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/room_chart_updation/room_chart_updation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('room_chart_updation.listing', {
#             'root': '/room_chart_updation/room_chart_updation',
#             'objects': http.request.env['room_chart_updation.room_chart_updation'].search([]),
#         })

#     @http.route('/room_chart_updation/room_chart_updation/objects/<model("room_chart_updation.room_chart_updation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('room_chart_updation.object', {
#             'object': obj
#         })
