# -*- coding: utf-8 -*-
# from odoo import http


# class SplifeGoodsPrint(http.Controller):
#     @http.route('/splife_goods_print/splife_goods_print/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/splife_goods_print/splife_goods_print/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('splife_goods_print.listing', {
#             'root': '/splife_goods_print/splife_goods_print',
#             'objects': http.request.env['splife_goods_print.splife_goods_print'].search([]),
#         })

#     @http.route('/splife_goods_print/splife_goods_print/objects/<model("splife_goods_print.splife_goods_print"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('splife_goods_print.object', {
#             'object': obj
#         })
