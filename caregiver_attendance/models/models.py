# -*- coding: utf-8 -*-

from odoo import models, fields, api


class caregiver_attendance(models.Model):
    _inherit = 'hr.work.entry'

    s_id = fields.Char()

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, '%s' % (field.x_studio_cg_id)))
        return res