# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Project(models.Model):
    _inherit = 'project.project'

    # project_code = fields.Char("Search ID")



    @api.model
    def create(self, vals):

        res = super(Project, self).create(vals)

        number_val = self.env['ir.sequence'].next_by_code('project.search.sequence')

        res['project_code'] = number_val
        return res