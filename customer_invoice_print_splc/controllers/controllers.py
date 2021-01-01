# -*- coding: utf-8 -*-
# from odoo import http


# class CustomerInvoicePrintSplc(http.Controller):
#     @http.route('/customer_invoice_print_splc/customer_invoice_print_splc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer_invoice_print_splc/customer_invoice_print_splc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer_invoice_print_splc.listing', {
#             'root': '/customer_invoice_print_splc/customer_invoice_print_splc',
#             'objects': http.request.env['customer_invoice_print_splc.customer_invoice_print_splc'].search([]),
#         })

#     @http.route('/customer_invoice_print_splc/customer_invoice_print_splc/objects/<model("customer_invoice_print_splc.customer_invoice_print_splc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer_invoice_print_splc.object', {
#             'object': obj
#         })
