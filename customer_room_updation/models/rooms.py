# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Roomchartmanagement(models.Model):
    _inherit = 'room.chart'

    check_out_date = fields.Date(string='Check Out Date',store=True, default=fields.Date.context_today)