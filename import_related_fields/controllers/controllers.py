# -*- coding: utf-8 -*-
# from odoo import http

from odoo import http
from odoo.http import request
# from odoo.addons.web.controllers.main import content_disposition
from odoo.http import Controller, request, route, content_disposition
import base64
import os, os.path
import csv
from os import listdir
import sys


class Download_xls(http.Controller):

    @http.route('/web/binary/download_document', type='http', auth="public")
    def download_document(self, model, id, **kw):

        Model = request.env[model]
        res = Model.browse(int(id))

        if res.sample_option == 'xls' and res.account_opt == 'default':

            invoice_xls = request.env['ir.attachment'].search([('name', '=', 'work_entry.xls')])
            filecontent = invoice_xls.datas
            filename = 'Work Entry.xls'
            filecontent = base64.b64decode(filecontent)

        elif res.sample_option == 'xls' and res.account_opt == 'custom':

            invoice_xls = request.env['ir.attachment'].search([('name', '=', 'sample_work_entry.xls')])
            filecontent = invoice_xls.datas
            filename = 'Sample Work Entry.xls'
            filecontent = base64.b64decode(filecontent)

        elif res.sample_option == 'csv' and res.account_opt == 'default':

            invoice_xls = request.env['ir.attachment'].search([('name', '=', 'work_entry.csv')])
            filecontent = invoice_xls.datas
            filename = 'Work Entry.csv'
            filecontent = base64.b64decode(filecontent)

        elif res.sample_option == 'csv' and res.account_opt == 'custom':

            invoice_xls = request.env['ir.attachment'].search([('name', '=', 'sample_work_entry.csv')])
            filecontent = invoice_xls.datas
            filename = 'Sample Work Entry.csv'
            filecontent = base64.b64decode(filecontent)

        return request.make_response(filecontent,
                                     [('Content-Type', 'application/octet-stream'),
                                      ('Content-Disposition', content_disposition(filename))])