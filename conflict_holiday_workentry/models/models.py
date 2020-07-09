# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from datetime import date, timedelta


class workentry_Conflict(models.Model):
    _inherit = 'hr.work.entry'


    def allsundays(self,years):
        sunndays =[]
        year = int(years)
        d = date(year, 1, 1)  # January 1st
        d += timedelta(days=6 - d.weekday())  # First Sunday
        while d.year == year:
            yield d
            d += timedelta(days=7)
            sunndays.append(str(d.strftime('%Y-%m-%d')))
        # yield sunndays





    # def action_approve_leave(self):
    #     res=super(workentry_Conflict, self).action_approve_leave()
    #
    #     if self.employee_id:
    #         if self.employee_id.user_id:
    #             user_id = self.employee_id.user_id.id
    #         else:
    #             user_id = self.time_sheet_ids._default_user()
    #     else:
    #         user_id = self.time_sheet_ids._default_user()
    #     so_order = {
    #         # 'partner_id': self.partner_id.id,
    #         'employee_id': self.employee_id.id,
    #         # 'task_id': self.project_task.id,
    #         'user_id': user_id,
    #         'date_start': self.date_start,
    #         'date_stop': self.date_stop,
    #         # 'project_id': self.project_id.id,
    #         # 'total_attendance': self.total_work_attendance,
    #         # 'so_line':1
    #
    #     }
    #
    #     so = self.env['account.analytic.line'].create(so_order)
    #
    #     return
    #
    #     return res

    @api.model_create_multi
    def create(self, vals_list):
        year_list =[]

        work_entries = super(workentry_Conflict, self).create(vals_list)


        global_leave = self.env['resource.calendar.leaves'].search([('resource_id', '=', False)])

        global_leave_list =[datetime.strptime(str(leave.date_from), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d') for leave in global_leave]


        start_year = datetime.strptime(str(vals_list[0]['date_start']), '%Y-%m-%d %H:%M:%S').strftime('%Y')
        start_date = datetime.strptime(str(vals_list[0]['date_start']), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        end_year = datetime.strptime(str(vals_list[0]['date_stop']), '%Y-%m-%d %H:%M:%S').strftime('%Y')
        end_date = datetime.strptime(str(vals_list[0]['date_stop']), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

        for s in self.allsundays(start_year):
            year_list.append(str(s.strftime('%Y-%m-%d')))
            print(s)

        # y = [d for d in self.allsundays(start_year)]

        complete_year_list = year_list + global_leave_list

        if start_date in complete_year_list:
            work_entries.write({'state': 'conflict'})
        elif end_date in complete_year_list:
            work_entries.write({'state': 'conflict'})
            # vals_list[0]['state'] = 'conflict'

        return work_entries

    # def write(self, vals):
    #     work = super(workentry_Conflict, self).write(vals)
    #
    #     global_leave = self.env['resource.calendar.leaves'].search([('resource_id', '=', False)])
    #
    #     global_leave_list = [datetime.strptime(str(leave.date_from), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d') for leave
    #                          in global_leave]
    #
    #     start_year = datetime.strptime(str(self.date_start), '%Y-%m-%d %H:%M:%S').strftime('%Y')
    #     start_date = datetime.strptime(str(self.date_start), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
    #     end_year = datetime.strptime(str(self.date_stop), '%Y-%m-%d %H:%M:%S').strftime('%Y')
    #     end_date = datetime.strptime(str(self.date_stop), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
    #
    #     year_list = [d for d in self.allsundays(start_year)]
    #
    #     if start_date or end_date in year_list or global_leave_list:
    #         work.write({'state': 'conflict'})
    #         # vals_list[0]['state'] = 'conflict'
    #
    #     return work
    #


