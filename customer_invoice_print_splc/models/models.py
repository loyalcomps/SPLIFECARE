# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class customer_invoice_print_splc(models.Model):
#     _name = 'customer_invoice_print_splc.customer_invoice_print_splc'
#     _description = 'customer_invoice_print_splc.customer_invoice_print_splc'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
