# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class incident_report_security(models.Model):
#     _name = 'incident_report_security.incident_report_security'
#     _description = 'incident_report_security.incident_report_security'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
