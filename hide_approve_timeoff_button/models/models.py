# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Approve_Conflict(models.Model):
    _inherit = 'hr.work.entry'

    hide_approve_timeoff = fields.Boolean(default=False)

    def action_approve_leave(self):
        res = super(Approve_Conflict, self).action_approve_leave()
        for i in self:
            i.hide_approve_timeoff = True
        return res