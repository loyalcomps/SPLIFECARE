# -*- coding: utf-8 -*-
from odoo import models, fields, api


class res_partner(models.Model):
    _inherit = "res.partner"

    living_type= fields.Many2one('room.type', string="Living Type")
    entering_date = fields.Date(string='Date', store=True)
    status = fields.Selection([
        ('check_in', 'Check In'),
        ('check_out', 'Check Out'),
    ],store=True, )



class Room_chart_management(models.Model):
    _inherit = 'room.chart'


    def action_confirm(self):

        res = super(Room_chart_management, self).action_confirm()
        self.current_status='occupy'


        for change in self.order_line:
            if self.occupant_names:
                partners = self.occupant_names.ids
                partner_id = self.occupant_name.id
                for j in partners:
                    partner_group = self.env['res.partner'].browse(j).write(
                        {
                            'living_type': self.living_type,
                            'x_studio_date_of_admission': self.entering_date,
                            'status':'check_in'

                        }
                    )

        return res


    def action_vacant(self):
        res = super(Room_chart_management, self).action_vacant()
        self.current_status = 'vacant'

        for change in self.order_line:
            if self.occupant_names:
                partners = self.occupant_names.ids
                partner_id = self.occupant_name.id
                for j in partners:
                    partner_group = self.env['res.partner'].browse(j).write(
                    {
                        'living_type': False,
                        'entering_date': self.check_out_date,
                        'status': 'check_out'

                    }
                )

        return res





