# -*- coding: utf-8 -*-
# from odoo import http


# class LocationPublicHolidays(http.Controller):
#     @http.route('/location_public_holidays/location_public_holidays/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/location_public_holidays/location_public_holidays/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('location_public_holidays.listing', {
#             'root': '/location_public_holidays/location_public_holidays',
#             'objects': http.request.env['location_public_holidays.location_public_holidays'].search([]),
#         })

#     @http.route('/location_public_holidays/location_public_holidays/objects/<model("location_public_holidays.location_public_holidays"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('location_public_holidays.object', {
#             'object': obj
#         })
