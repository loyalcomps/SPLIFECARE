# -*- coding: utf-8 -*-
# from odoo import http


# class CaretakerSaleOrder(http.Controller):
#     @http.route('/invoice_homenursing/invoice_homenursing/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_homenursing/invoice_homenursing/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_homenursing.listing', {
#             'root': '/invoice_homenursing/invoice_homenursing',
#             'objects': http.request.env['invoice_homenursing.invoice_homenursing'].search([]),
#         })

#     @http.route('/invoice_homenursing/invoice_homenursing/objects/<model("invoice_homenursing.invoice_homenursing"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_homenursing.object', {
#             'object': obj
#         })
