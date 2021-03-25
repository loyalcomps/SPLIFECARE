import datetime
from odoo.exceptions import UserError
from datetime import datetime, date
import time
from odoo import api, models, _
from odoo.exceptions import UserError
from xlsxwriter.utility import xl_range, xl_rowcol_to_cell


class GST_statementXls(models.AbstractModel):
    _name = 'report.splife_gst_report.action_gst_report_xls'
    _inherit = 'report.report_xlsx.abstract'

    def get_sale(self, data):

        lines = []

        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        company_id = data['form']['company_id']

        sl = 0

        query = '''

             select dd.id,
                (dd.employee_name) as employee_name,
				dd.code as code,
                (dd.basic_salary) as basic_salary,
				(dd.working_days) as working_days,
				dd.travel_expense as travel_expense,
				(dd.basic_salary+dd.travel_expense) as total,
                (dd.less_tds) as less_tds,
                dd.other_deduction as other_deduction,
				dd.advance as advance,
                dd.net_amount as net_amount

                from

            ((select hre.id as id,
			  hre.name as employee_name,
			  hre.barcode as code,
              sum(case when hrpl.code ~~* 'TDS%%' then hrpl.total else 0 end) as less_tds,
              sum(case when hrpl.code='NET' then hrpl.total else 0 end) as net_amount

                        from hr_payslip_line as hrpl
                left join hr_payslip as hrp on hrp.id=hrpl.slip_id
                left join hr_employee as hre on hre.id=hrp.employee_id
                left join hr_department as hp on hp.id=hre.department_id
                left join hr_job as hrj on hrj.id=hre.job_id
                where to_char(date_trunc('day',hrp.date_from),'YYYY-MM-DD')::date between %s and %s
              and hrp.company_id=%s 
              and hrp.state in ('verify','done')

                group by hre.id) as a

                left join
                (select 
				sum(case when ht.code='DB100' then (hw.no_of_shift*2) else hw.no_of_shift end) as working_days,
				 h.employee_id as employee_id from hr_payslip as h
                left join hr_payslip_worked_days as hw on h.id=hw.payslip_id
				 left join hr_work_entry_type as ht on ht.id=hw.work_entry_type_id
                where to_char(date_trunc('day',h.date_from),'YYYY-MM-DD')::date between %s and %s
                 and h.company_id=%s
                 and h.state in ('verify','done')
                group by h.employee_id)as b on a.id=b.employee_id

             left join
             (select hl.employee_id as em_id,
             sum(case when hc.code='BASIC' then hl.total else 0 end) as basic_salary,     
             sum(case when hl.code !~~* 'TDS%%' and hc.code<>'ADV' and hc.name='Deduction' then hl.total else 0 end) as other_deduction,
             sum(case when hc.code='TRAVEL' then hl.total else 0 end) as travel_expense,
			 sum(case when hc.code='ADV' then hl.total else 0 end) as advance

			  from hr_payslip_line as hl
              left join hr_payslip as hp on hp.id=hl.slip_id
              left join hr_salary_rule_category as hc on hc.id=hl.category_id
              where to_char(date_trunc('day',hp.date_from),'YYYY-MM-DD')::date between %s and %s
              and hp.company_id=%s
                 and hp.state in ('verify','done')

              group by hl.employee_id
             )as c on a.id=c.em_id

            )dd   
              '''
        self.env.cr.execute(query, (
            date_from, date_to, company_id,
            date_from, date_to, company_id,
            date_from, date_to, company_id,
        ))
        for row in self.env.cr.dictfetchall():
            sl += 1

            employee_name = row['employee_name'] if row['employee_name'] else " "
            code = row['code'] if row['code'] else " "
            basic_salary = row['basic_salary'] if row['basic_salary'] else 0.0
            working_days = row['working_days'] if row['working_days'] else 0.0
            travel_expense = row['travel_expense'] if row['travel_expense'] else 0.0
            total = row['total'] if row['total'] else 0.0
            # sale_new_date = datetime.strptime(str(saledate), '%Y-%m-%d').date().strftime('%d-%m-%Y')
            less_tds = row['less_tds'] if row['less_tds'] else 0.0
            other_deduction = row['other_deduction'] if row['other_deduction'] else 0.0
            net_amount = row['net_amount'] if row['net_amount'] else 0.0
            advance = row['advance'] if row['advance'] else 0.0

            res = {
                'sl_no': sl,
                'code': code if code else " ",
                'employee_name': employee_name if employee_name else " ",
                'basic_salary': basic_salary if basic_salary else 0.0,
                'working_days': working_days if working_days else 0.0,
                'travel_expense': travel_expense if travel_expense else 0.0,
                'total': total if total else 0.0,
                'less_tds': less_tds if less_tds else 0.0,
                'other_deduction': other_deduction if other_deduction else 0.0,
                'advance': advance if advance else 0.0,
                'net_amount': net_amount if net_amount else 0.0,

            }

            lines.append(res)
        if lines:
            return lines
        else:
            return []




    def generate_xlsx_report(self, workbook, data, lines):

        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        sheet = workbook.add_worksheet(_('Caregiver Salary Statement Report'))
        sheet.set_landscape()
        sheet.set_default_row(25)
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)

        company = self.env['res.company'].browse(data['form']['company_id'])

        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        company_id = data['form']['company_id']
        if company.street:
            res = company.street
        else:
            res = ""
        if company.street2:
            res2 = company.street2
        else:
            res2 = ""

        date_start = data['form']['date_from']
        date_end = data['form']['date_to']

        if date_start:
            date_object_date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
        if date_end:
            date_object_date_end = datetime.strptime(date_end, '%Y-%m-%d').date()

        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 14})
        font_size_8_center = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'font_size': 14, 'align': 'center'})
        font_size_8_right = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'font_size': 14, 'align': 'right'})
        font_size_8_left = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'font_size': 14, 'align': 'left'})

        formattotal = workbook.add_format(
            {'bg_color': 'e2e8e8', 'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True,
             'align': 'right', 'bold': True})

        blue_mark2 = workbook.add_format(
            {'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 14, 'bold': True,
             'color': 'ffffff', 'bg_color': '7b0b5b', 'align': 'center'})
        font_size_8blod = workbook.add_format(
            {'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 14, 'bold': True, })

        blue_mark3 = workbook.add_format(
            {'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 18, 'bold': True,
             'color': 'ffffff', 'bg_color': '7b0b5b', 'align': 'center'})

        title_style = workbook.add_format({'font_size': 14, 'bold': True,
                                           'bg_color': '#87bdd1', 'color': 'ffffff',
                                            'align': 'center','valign': 'vcenter','border':1})
        account_style = workbook.add_format({'font_size': 14, 'bold': True,
                                             'bg_color': '929393', 'color': 'ffffff',
                                             'bottom': 1, 'align': 'left'})

        sheet.set_column(1, 1, 50)
        sheet.set_column(2, 2, 25)
        sheet.set_column(3, 3, 25)
        sheet.set_column(4, 4, 25)
        sheet.set_column(5, 5, 25)
        sheet.set_column(6, 6, 25)
        sheet.set_column(7, 7, 25)
        sheet.set_column(8, 8, 25)
        sheet.set_column(9, 9, 25)
        sheet.set_column(10, 10, 25)
        sheet.set_column(11, 11, 25)
        sheet.set_column(12, 12, 25)
        sheet.set_column(13, 13, 20)
        sheet.set_column(14, 14, 20)
        sheet.set_column(15, 15, 20)
        sheet.set_column(16, 16, 20)
        sheet.set_column(17, 17, 20)
        sheet.set_column(18, 18, 20)
        sheet.set_column(19, 19, 20)
        sheet.set_column(20, 20, 20)
        sheet.set_column(21, 21, 30)
        sheet.set_column(22, 22, 20)
        sheet.set_column(23, 23, 20)
        sheet.set_column(24, 24, 20)

        date_start = data['form']['date_from']
        date_end = data['form']['date_to']

        if date_end:
            date_month = datetime.strptime(date_end, '%Y-%m-%d').date().strftime('%B')
            date_year = datetime.strptime(date_end, '%Y-%m-%d').date().strftime('%Y')
        else:
            date_month = ""
            date_year = ""

        sheet.merge_range('A1:K1', company.name, blue_mark3)
        # sheet.merge_range('A2:P2', res+" ," + res2, blue_mark2)
        sheet.merge_range('A2:K2', "PAYMENT SCHEDULE OF RE FEE + TRAVEL EXPENSE TO CARE GIVERS FROM " + date_object_date_start.strftime(
                '%d-%m-%Y') + " to " + date_object_date_end.strftime('%d-%m-%Y'), blue_mark2)

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))

        if date_start and date_end:

            sheet.merge_range('A5:K5', "Date : " + date_object_date_start.strftime(
                '%d-%m-%Y') + " to " + date_object_date_end.strftime('%d-%m-%Y'), font_size_8blod)
        elif date_start:
            sheet.merge_range('A5:K5', "Date : " + date_object_date_start.strftime('%d-%m-%Y'),
                              font_size_8blod)

        sheet.merge_range('A6:A7', "SL.NO.", title_style)

        sheet.merge_range('B6:B7', "Date", title_style)
        sheet.merge_range('C6:C7', "Transaction Type", title_style)
        sheet.merge_range('D6:D7', "Consignee/Buyer", title_style)
        sheet.merge_range('E6:E7', "Voucher Type", title_style)
        sheet.merge_range('F6:F7', "Voucher No.", title_style)
        sheet.merge_range('G6:G7', "TOTAL", title_style)
        sheet.merge_range('H6:J6', "Registration Fee @18%", title_style)
        # sheet.merge_range('I6:I7', "SALARY FOR THE MONTH", title_style)
        sheet.write_string('H7', "CGST @ 9%", title_style)
        sheet.write_string('I7', "SGST @ 9%", title_style)
        sheet.write_string('J7', "Round Off", title_style)

        sheet.merge_range('K6:K7', "Gross Total", title_style)
        # sheet.write('K6', "SALARY PAYABLE", title_style)

        linw_row = 7
        line_column = 0

        for line in self.get_sale(data):
            sheet.write(linw_row, line_column, line['sl_no'], font_size_8_center)
            sheet.write(linw_row, line_column + 1, line['employee_name'], font_size_8_left)

            sheet.write(linw_row, line_column + 2, line['code'], font_size_8_left)
            sheet.write(linw_row, line_column + 3, line['working_days'], font_size_8_center)
            sheet.write(linw_row, line_column + 4, '{0:.2f}'.format(float(line['basic_salary'])), font_size_8_right)
            sheet.write(linw_row, line_column + 5, '{0:.2f}'.format(float(line['travel_expense'])), font_size_8_right)

            sheet.write(linw_row, line_column + 6, '{0:.2f}'.format(float(line['total'])), font_size_8_right)
            sheet.write(linw_row, line_column + 7, '{0:.2f}'.format(float(line['less_tds'])), font_size_8_right)
            sheet.write(linw_row, line_column + 8, '{0:.2f}'.format(float(line['advance'])),
                        font_size_8_right)
            sheet.write(linw_row, line_column + 9, '{0:.2f}'.format(float(line['other_deduction'])), font_size_8_right)
            sheet.write(linw_row, line_column + 10, '{0:.2f}'.format(float(line['net_amount'])), font_size_8_right)



            linw_row = linw_row + 1
            line_column = 0

        line_column = 0

        sheet.merge_range(linw_row, 0, linw_row, 3, "TOTAL", font_size_8_left)

        total_cell_range3 = xl_range(7, 3, linw_row - 1, 3)
        total_cell_range = xl_range(7, 4, linw_row - 1, 4)
        total_cell_range5 = xl_range(7, 5, linw_row - 1, 5)
        total_cell_range6 = xl_range(7, 6, linw_row - 1, 6)
        total_cell_range7 = xl_range(7, 7, linw_row - 1, 7)
        total_cell_range8 = xl_range(7, 8, linw_row - 1, 8)
        total_cell_range9 = xl_range(7, 9, linw_row - 1, 9)
        total_cell_range10 = xl_range(7, 10, linw_row - 1, 10)

        sheet.write_formula(linw_row, 3, '=SUM(' + total_cell_range3 + ')', font_size_8_right)
        sheet.write_formula(linw_row, 4, '=SUM(' + total_cell_range + ')', font_size_8_right)
        sheet.write_formula(linw_row, 5, '=SUM(' + total_cell_range5 + ')', font_size_8_right)
        sheet.write_formula(linw_row, 6, '=SUM(' + total_cell_range6 + ')', font_size_8_right)
        sheet.write_formula(linw_row, 7, '=SUM(' + total_cell_range7 + ')', font_size_8_right)
        sheet.write_formula(linw_row, 8, '=SUM(' + total_cell_range8 + ')', font_size_8_right)
        sheet.write_formula(linw_row, 9, '=SUM(' + total_cell_range9 + ')', font_size_8_right)
        sheet.write_formula(linw_row, 10, '=SUM(' + total_cell_range9 + ')', font_size_8_right)





