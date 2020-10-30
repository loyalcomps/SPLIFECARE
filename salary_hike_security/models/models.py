# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class salary_hike_security(models.Model):
#     _name = 'salary_hike_security.salary_hike_security'
#     _description = 'salary_hike_security.salary_hike_security'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
