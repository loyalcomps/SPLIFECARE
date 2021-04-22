# -*- coding: utf-8 -*-
# from odoo import http


# class CompanyRoundoffAccount(http.Controller):
#     @http.route('/company_roundoff_account/company_roundoff_account/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/company_roundoff_account/company_roundoff_account/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('company_roundoff_account.listing', {
#             'root': '/company_roundoff_account/company_roundoff_account',
#             'objects': http.request.env['company_roundoff_account.company_roundoff_account'].search([]),
#         })

#     @http.route('/company_roundoff_account/company_roundoff_account/objects/<model("company_roundoff_account.company_roundoff_account"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('company_roundoff_account.object', {
#             'object': obj
#         })
