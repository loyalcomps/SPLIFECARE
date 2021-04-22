# -*- coding: utf-8 -*-
# from odoo import http


# class HideRoundedtotal(http.Controller):
#     @http.route('/hide_roundedtotal/hide_roundedtotal/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hide_roundedtotal/hide_roundedtotal/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hide_roundedtotal.listing', {
#             'root': '/hide_roundedtotal/hide_roundedtotal',
#             'objects': http.request.env['hide_roundedtotal.hide_roundedtotal'].search([]),
#         })

#     @http.route('/hide_roundedtotal/hide_roundedtotal/objects/<model("hide_roundedtotal.hide_roundedtotal"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hide_roundedtotal.object', {
#             'object': obj
#         })
