# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
import tempfile
import binascii
import xlrd
import io
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import date, datetime,timedelta
from odoo.exceptions import Warning
from odoo import models, fields, exceptions, api, _
from odoo.exceptions import UserError, ValidationError
import pytz

import logging

_logger = logging.getLogger(__name__)

try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class Wrkentry(models.Model):
    _inherit = 'hr.work.entry'


    invoice_name = fields.Char('Invocie Name')
    project_code = fields.Char('Search ID')
    badge_id = fields.Char('Badge ID')




class gen_inv(models.TransientModel):
    _name = "gen.invoice"

    file = fields.Binary('File')
    account_opt = fields.Selection(
        [('default', 'Configuration product/Property'), ('custom', 'Excel/CSV')],
        string='Option', required=True, default='default')

    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select', default='csv')
    sample_option = fields.Selection([('csv', 'CSV'), ('xls', 'XLS')], string='Sample Type', default='csv')
    down_samp_file = fields.Boolean(string='Download Sample Files')

    def make_invoice(self, values):
        invoice_obj = self.env['hr.work.entry']

        invoice_search = invoice_obj.search([
                    ('name', '=', values.get('name')),
                    ('badge_id', '=', values.get('badge_id')),
                ])

        if invoice_search:
            if invoice_search.employee_id.badge_id == values.get('badge_id'):
                if invoice_search.project_id.project_code == values.get('project_code'):
                    if invoice_search.state == 'draft':
                        return invoice_search
                    else:
                        raise Warning(_('Work entry "%s" is not in Draft state.') % invoice_search.name)


                else:
                    raise Warning(_('Project search is different for "%s" .\n Please define same.') % values.get('project_code'))
            else:
                raise Warning(_('Employee badge is different for "%s" .\n Please define same.') % values.get('badge_id'))
        else:
            partner_id = self.find_partner(values.get('badge_id'))
            project_id = self.find_project(values.get('project_code'))
            im_date_start = self.find_invoice_date(values.get('from'))
            im_date_stop = self.find_invoice_date(values.get('to'))
            wrk_entry_type= self.find_work_entry_type(values.get('work_entry_type'))

            # work_entry = self.env['hr.work.entry.type'].browse(values.get('work_entry_type'))


            inv_id = invoice_obj.create({
                'employee_id': partner_id.id,
                'project_id': project_id.id,
                'name': values.get('name'),
                # 'work_entry_type_id': work_entry.id,
                'contract_id':partner_id.contract_id.id,

                'work_entry_type_id': wrk_entry_type.id,
                'date_start': im_date_start,
                'date_stop': im_date_stop,
                'duration': values.get('duration'),
                # 'state': values.get('state')
            })

            return inv_id


    def find_project(self, name):
        currency_obj = self.env['project.project']
        project_search = currency_obj.search([('project_code', '=', name)])
        if project_search:
            return project_search
        else:
            raise Warning(_(' "%s" project are not available.') % name)


    def find_partner(self, name):
        partner_obj = self.env['hr.employee']
        partner_search = partner_obj.search([('barcode', '=', name)])
        if partner_search:
            return partner_search[0]
        else:
            raise Warning(_(' "%s" Employee are not available.') % name)
            # partner_id = partner_obj.create({
            #     'badge_id': name})
            # return partner_id
    def find_work_entry_type(self, name):
        work_entry = self.env['hr.work.entry.type']
        type_search = work_entry.search([('name', '=', name)])
        if type_search:
            return type_search
        else:
            raise Warning(_(' "%s" Work Entry Type are not available.') % name)

    def new_find_invoice_date(self, date):
        DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
            # "%Y-%m-%d"
        i_date = datetime.strptime(date, DATETIME_FORMAT).strftime('%Y-%m-%d %H:%M:%S')
        return i_date
    def find_invoice_date(self, date):
        fmt = "%Y-%m-%d %H:%M:%S"
        # Current time in UTC
        now_utc = datetime.strptime(date, fmt)
        # Convert to current user time zone
        user_tz = self.env.user.tz or pytz.utc
        now_timezone = now_utc.astimezone(pytz.timezone(self.env.user.tz))
        UTC_OFFSET_TIMEDELTA = datetime.strptime(
            now_timezone.strftime(fmt), fmt)-datetime.strptime(now_utc.strftime(fmt), fmt)
        local_datetime = datetime.strptime(date, fmt)
        result_utc_datetime = local_datetime - UTC_OFFSET_TIMEDELTA
        return result_utc_datetime.strftime(fmt)

    def import_csv(self):
        """Load Inventory data from the CSV file."""
        if self.import_option == 'csv':
            keys = ['name', 'work_entry_type', 'badge_id', 'project_code', 'from','to','duration']

            try:
                csv_data = base64.b64decode(self.file)
                data_file = io.StringIO(csv_data.decode("utf-8"))
                data_file.seek(0)
                file_reader = []
                csv_reader = csv.reader(data_file, delimiter=',')

                file_reader.extend(csv_reader)
            except Exception:
                raise exceptions.Warning(_("Please select an CSV/XLS file or You have selected invalid file"))
            values = {}
            invoice_ids = []
            for i in range(len(file_reader)):
                field = list(map(str, file_reader[i]))
                if len(field) > 7:
                    raise Warning(_('Your File has extra column please refer sample file'))
                elif len(field) < 7:
                    raise Warning(_('Your File has less column please refer sample file'))

                values = dict(zip(keys, field))
                if values:
                    if i == 0:
                        continue
                    else:
                        values.update({
                                       'option': self.import_option,
                                       })
                        res = self.make_invoice(values)
                        # res.compute_taxes()
                        invoice_ids.append(res)


        else:
            try:
                fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
                fp.write(binascii.a2b_base64(self.file))
                fp.seek(0)
                values = {}
                invoice_ids = []
                workbook = xlrd.open_workbook(fp.name)
                sheet = workbook.sheet_by_index(0)
            except Exception:
                raise exceptions.Warning(_("Please select an CSV/XLS file or You have selected invalid file"))

            for row_no in range(sheet.nrows):
                val = {}
                if row_no <= 0:
                    fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
                else:
                    line = list(
                        map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value),
                            sheet.row(row_no)))
                    if self.account_opt == 'default':
                        if len(line) == 7:
                            a1 = float(line[4])
                            a1_as_datetime = datetime(*xlrd.xldate_as_tuple(a1, workbook.datemode))
                            date_from = a1_as_datetime.strftime('%Y-%m-%d %H:%M:%S')
                            a2 = float(line[5])
                            a2_as_datetime = datetime(*xlrd.xldate_as_tuple(a2, workbook.datemode))
                            date_end= a2_as_datetime.strftime('%Y-%m-%d %H:%M:%S')

                            values.update({'name': line[0],
                                           'work_entry_type': line[1],
                                           'badge_id': line[2],
                                           'project_code': line[3],
                                           'from': date_from,
                                           'to': date_end,
                                           'duration': float(line[6]),
                                           # 'state': line[7],
                                           })
                        elif len(line) > 7:
                            raise Warning(_('Your File has extra column please refer sample file'))
                        else:
                            raise Warning(_('Your File has less column please refer sample file'))

                    res = self.make_invoice(values)
                    # res.compute_taxes()
                    invoice_ids.append(res)


        return res

    def download_auto(self):

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=gen.invoice&id=%s' % (self.id),
            'target': 'new',
        }
