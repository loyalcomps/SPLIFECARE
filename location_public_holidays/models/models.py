# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Work_location(models.Model):
    _name = 'work.location'
    _description = 'Locations'

    name = fields.Char(string="Locations")

class Res_user(models.Model):
    _inherit = 'res.users'

    location_name = fields.Many2many('work.location',string="Locations")


class Hr_employee(models.Model):
    _inherit = 'hr.employee'

    location_name = fields.Many2one('work.location',string="Locations")

# class Public_holidays(models.Model):
#     _inherit = 'x_public_holidays'
#
#     location_name = fields.Many2many('work.location',string="Locations")