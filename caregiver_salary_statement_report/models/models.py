# -*- coding: utf-8 -*-

from odoo import models, fields, api

class caregiver_salary_statementsales(models.TransientModel):
    _name = "caregiver.salary.statement"
    _description = "Caregiver Salary Statement Report"


    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    date_from = fields.Date(string='Start Date',required=True,default=fields.Date.today,)
    date_to = fields.Date(string='End Date',required=True,default=fields.Date.today,)


    def export_xls(self):


        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'hr.payslip'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]

        return self.env.ref('caregiver_salary_statement_report.caregiver_statement_xls').report_action(self, data=datas)
