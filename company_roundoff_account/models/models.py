# -*- coding: utf-8 -*-

from odoo import models, fields, api



class ResCompany(models.Model):
    _inherit = "res.company"

    roundoff_account_id = fields.Many2one('account.account',string="Round Off Account")