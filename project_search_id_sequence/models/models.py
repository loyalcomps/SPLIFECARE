# -*- coding: utf-8 -*-

from odoo import models, fields, api
import re


# str.isdigit

class Project(models.Model):
    _inherit = 'project.project'

    # project_code = fields.Char("Search ID")



    @api.model
    def create(self, vals):

        res = super(Project, self).create(vals)

        number_val = self.env['ir.sequence'].next_by_code('project.search.sequence')

        res['project_code'] = number_val
        return res

    def unlink(self):
        sequence = self.project_code
        next_sequence = self.env['ir.sequence'].next_by_code('project.search.sequence')
        # increment_value = self.env['ir.sequence'].search([('code','=','project.search.sequence'),('company_id','=',self.company_id.id)]).number_next_actual

        line1 = sequence
        temp1 = re.findall(r'\d+', line1)  # through regular expression
        res1 = list(map(int, temp1))
        number1 = res1[-1]
        line2 = next_sequence
        temp2 = re.findall(r'\d+', line2)  # through regular expression
        res2 = list(map(int, temp2))
        number2 = res2[-1]
        if number2-number1==1:

            self.env['ir.sequence'].search(
            [('code', '=', 'project.search.sequence'), ('company_id', '=', self.company_id.id)]).update({

            'number_next_actual':number1
        })
        super(Project, self).unlink()