# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectSearchIdSequence(http.Controller):
#     @http.route('/project_search_id_sequence/project_search_id_sequence/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_search_id_sequence/project_search_id_sequence/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_search_id_sequence.listing', {
#             'root': '/project_search_id_sequence/project_search_id_sequence',
#             'objects': http.request.env['project_search_id_sequence.project_search_id_sequence'].search([]),
#         })

#     @http.route('/project_search_id_sequence/project_search_id_sequence/objects/<model("project_search_id_sequence.project_search_id_sequence"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_search_id_sequence.object', {
#             'object': obj
#         })
