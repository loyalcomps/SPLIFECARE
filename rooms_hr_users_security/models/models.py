# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rooms_hr_users_security(models.Model):
#     _name = 'rooms_hr_users_security.rooms_hr_users_security'
#     _description = 'rooms_hr_users_security.rooms_hr_users_security'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
