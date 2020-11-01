# -*- coding: utf-8 -*-

from odoo import models, fields, api



class Incident_report_form(models.Model):
    _name = 'incident.report'
    _description = 'Incident Report'

    order_line = fields.One2many('incident.report.line', 'order_id', string='Incident Report Form')
    customer_name = fields.Many2one('res.partner',string='Customer Name',store=True)

class Incident_report_form_line(models.Model):
    _name = 'incident.report.line'

    order_id = fields.Many2one('incident.report', string='Incident Report', ondelete='cascade')
    entering_date = fields.Date(string='Date', store=True, default=fields.Date.context_today)
    activity_log = fields.Char(string="Activity",store=True)
    customer_name = fields.Many2one('res.partner', string='Customer Name', store=True,related='order_id.customer_name')

class Res_partner(models.Model):
    _inherit = 'res.partner'


    def incident_report_window(self, context=None):
        dom = self.env['incident.report'].search(

            [('customer_name', '=', self.id)]).ids

        domain = [('id', 'in', dom)]

        form_view_id = self.env.ref('incident_report.incident_report_line_setup_form').id

        view_id = self.env.ref('incident_report.incident_report_form_line_tree').id
        # recruitment_questions_line_tree
        return {
            'name': 'Incident Report Form',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'incident.report',
            'views': [[view_id, 'tree'], [form_view_id, 'form']],
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'domain': domain,
            'context':{
            # 'default_model': 'incident.report',
            #     'search_default_customer_name': self.id,
                'default_customer_name': self.id

        }
        }

