# -*- coding: utf-8 -*-
from odoo import models, fields, api

class res_partner(models.Model):
    _inherit = "res.partner"

    room_number = fields.Many2one("room.room",string='Room Number')


class Room_room(models.Model):
    _inherit = 'room.room'

    living_type= fields.Many2one('room.type', string="Living Type")
    occupant_name = fields.Many2one('res.partner', string="Partner")
    occupant_names = fields.Many2many('res.partner', string="Occupant Name ")
    entering_date = fields.Date(string='Order Date', store=True, default=fields.Date.context_today)


class Room_chart_management(models.Model):
    _inherit = 'room.chart'

    occupant_names = fields.Many2many('res.partner', string="Occupant Name ")



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
                            'room_number': change.chart_room.id,

                        }
                    )
            if change.chart_room:
                room_id = change.chart_room.id
                customer_group = self.env['room.room'].browse(room_id).write(
                    {
                        # 'status': change.chart_status,
                        'living_type' :self.living_type,
                        'occupant_names': [(6, 0, self.occupant_names.ids)],
                        'occupant_name' :self.occupant_name,
                        'entering_date':self.entering_date,
                    }
                )
                # change.chart_room.status = change.chart_status
        return res


    def action_vacant(self):
        res = super(Room_chart_management, self).action_vacant()
        self.current_status = 'vacant'

        for change in self.order_line:
            if self.occupant_name:
                partners = self.occupant_names.ids
                partner_id = self.occupant_name.id
                for j in partners:
                    partner_group = self.env['res.partner'].browse(j).write(
                    {
                        'room_number': False,

                    }
                )
            if change.chart_room:
                room_id = change.chart_room.id
                customer_group = self.env['room.room'].browse(room_id).write(
                    {
                        # 'status': change.chart_status,
                        'living_type': False,
                        'occupant_names': False,
                        'occupant_name': False,
                        'entering_date': False,
                    }
                )
                # change.chart_room.status = change.chart_status
        return res



