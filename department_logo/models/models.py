# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Department(models.Model):
    _inherit = 'hr.department'

    logo = fields.Binary(string="Department Logo")

class AccountMove(models.Model):
    _inherit = 'account.move'

    department_id = fields.Many2one(comodel_name="hr.department", string="Department")


