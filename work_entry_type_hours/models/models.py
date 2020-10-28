# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime,timedelta
import pytz



class Hrwork_entry_type(models.Model):
    _inherit = 'hr.work.entry.type'

    date_start = fields.Datetime(string='From')
    date_stop = fields.Datetime(string='To')

    start_time = fields.Float(string='Time From',default=0.0)
    end_time = fields.Float(string='Working Hours',default=0.0)


class Hr_work_entry(models.Model):
    _inherit = 'hr.work.entry'

    @api.onchange('work_entry_type_id')
    def work_entry_time(self):

        for order in self:
            fmt = "%Y-%m-%d %H:%M:%S"
            if order.work_entry_type_id:
                if order.date_start!= False or order.date_stop != False:
                    # start =datetime.strptime(str(order.date_start), fmt).strftime('%m')
                    # end =datetime.strptime(str(order.date_stop), fmt).strftime('%m')
                    # today= datetime.now().strftime('%m')
                    # if start== today:
                    #     s=order.date_start.date()
                    # else:
                    s=order.date_stop.date()

                    if s != datetime.now().date():

                        date_value = datetime.now(),

                        order.date_start = (order.date_stop.replace(hour=0, minute=0, second=0,
                                                                   microsecond=0)) + timedelta(
                            hours=order.work_entry_type_id.start_time)
                        now_utc = datetime.strptime(str(order.date_stop), fmt)
                        # Convert to current user time zone
                        user_tz = self.env.user.tz or pytz.utc
                        now_timezone = now_utc.astimezone(pytz.timezone(self.env.user.tz))
                        UTC_OFFSET_TIMEDELTA = datetime.strptime(
                            str(now_timezone.strftime(fmt)), fmt) - datetime.strptime(str(now_utc.strftime(fmt)), fmt)
                        local_datetime = datetime.strptime(str(order.date_start), fmt)
                        result_utc_datetime = local_datetime - UTC_OFFSET_TIMEDELTA
                        order.date_start = (order.date_stop.replace(hour=0, minute=0, second=0,
                                                                   microsecond=0)) + timedelta(
                            hours=order.work_entry_type_id.start_time) - UTC_OFFSET_TIMEDELTA

                        a= str(order.work_entry_type_id.end_time).split('.')

                        t_hour = int(a[0])
                        t_min = int(a[1])

                        time_difference = ((order.date_start.replace(hour=0, minute=0, second=0,
                                                                   microsecond=0)) + timedelta(
                            hours=order.work_entry_type_id.end_time)) - (
                                                      (order.date_start.replace(hour=0, minute=0, second=0,
                                                                              microsecond=0)) + timedelta(
                                                  hours=order.work_entry_type_id.start_time))
                        order.date_stop = order.date_start +timedelta(
                        hours=t_hour,minutes=t_min)

                    else:

                        date_value = datetime.now(),

                        order.date_start = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)) + timedelta(
                            hours=order.work_entry_type_id.start_time)
                        now_utc = datetime.strptime(str(order.date_start), fmt)
                        # Convert to current user time zone
                        user_tz = self.env.user.tz or pytz.utc
                        now_timezone = now_utc.astimezone(pytz.timezone(self.env.user.tz))
                        UTC_OFFSET_TIMEDELTA = datetime.strptime(
                            str(now_timezone.strftime(fmt)), fmt) - datetime.strptime(str(now_utc.strftime(fmt)), fmt)
                        local_datetime = datetime.strptime(str(order.date_start), fmt)
                        result_utc_datetime = local_datetime - UTC_OFFSET_TIMEDELTA
                        order.date_start = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)) + timedelta(
                            hours=order.work_entry_type_id.start_time) - UTC_OFFSET_TIMEDELTA

                        a = str(order.work_entry_type_id.end_time).split('.')

                        t_hour = int(a[0])
                        t_min = int(a[1])

                        time_difference = ((datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)) + timedelta(
                            hours=order.work_entry_type_id.end_time)) - ((datetime.now().replace(hour=0, minute=0, second=0,
                                                                                                 microsecond=0)) + timedelta(
                            hours=order.work_entry_type_id.start_time))
                        order.date_stop = order.date_start + timedelta(
                        hours=t_hour,minutes=t_min)
                else:

                    date_value = datetime.now(),

                    order.date_start = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)) + timedelta(
                        hours=order.work_entry_type_id.start_time)
                    now_utc = datetime.strptime(str(order.date_start), fmt)
                    # Convert to current user time zone
                    user_tz = self.env.user.tz or pytz.utc
                    now_timezone = now_utc.astimezone(pytz.timezone(self.env.user.tz))
                    UTC_OFFSET_TIMEDELTA = datetime.strptime(
                        str(now_timezone.strftime(fmt)), fmt) - datetime.strptime(str(now_utc.strftime(fmt)), fmt)
                    local_datetime = datetime.strptime(str(order.date_start), fmt)
                    result_utc_datetime = local_datetime - UTC_OFFSET_TIMEDELTA
                    order.date_start = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)) + timedelta(
                        hours=order.work_entry_type_id.start_time) - UTC_OFFSET_TIMEDELTA

                    a = str(order.work_entry_type_id.end_time).split('.')

                    t_hour = int(a[0])
                    t_min = int(a[1])

                    time_difference = ((datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)) + timedelta(
                        hours=order.work_entry_type_id.end_time)) - ((datetime.now().replace(hour=0, minute=0, second=0,
                                                                                             microsecond=0)) + timedelta(
                        hours=order.work_entry_type_id.start_time))
                    order.date_stop = order.date_start + timedelta(
                        hours=t_hour,minutes=t_min)
                # if self.env['ir.ui.view'].search([('type','!=','gantt')]):


