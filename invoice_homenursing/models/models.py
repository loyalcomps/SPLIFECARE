# -*- coding: utf-8 -*-
from odoo import models, fields, api,_



class ProductTemplate(models.Model):
    _inherit = "product.template"

    timesheet_product = fields.Boolean(string='Is a Caretaker', default=False,store=True)

class AnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    allow_billable = fields.Boolean(string="Billable",default=False,store=True)


    # def action_timesheet_make_billable(self):
    #     return {
    #         "name": _("Create Sales Order"),
    #         "type": 'ir.actions.act_window',
    #         "res_model": 'project.timesheet.create.sale.order',
    #         "views": [[False, "form"]],
    #         "target": 'new',
    #         "context": {
    #             'active_id': self.id,
    #             'active_model': 'account.analytic.line',
    #             'form_view_initial_mode': 'edit',
    #         },
    #     }
