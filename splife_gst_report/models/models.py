# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Gst_report(models.TransientModel):
    _name = "gst.report.wizard"
    _description = "GST Report"


    # operating_unit= fields.Many2one('operating.unit', string='Branch',
    #                              default=lambda self: self.env.user.default_operating_unit_id)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    target_move = fields.Boolean(default=False)



    def export_xls(self):

        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'account.move'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]

        return self.env.ref('splife_gst_report.gst_report_xls').report_action(self, data=datas)
