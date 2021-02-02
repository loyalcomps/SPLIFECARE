# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, _
import datetime
from datetime import datetime
from odoo.exceptions import UserError, ValidationError


#
# class HrExpense(models.Model):
#     _inherit = "hr.expense"
#
#     payment_mode = fields.Selection(selection_add=[('payslip_account', 'Payslip (to reimburse)')])
# MONTH_LIST = [('1', 'Jan'), ('2', 'Feb'), ('3', 'Mar'), ('4', 'Apr'), ('5', 'May'), ('6', 'Jun'), ('7', 'Jul'),
#               ('8', 'Aug'), ('9', 'Sep'), ('10', 'Oct'), ('11', 'Nov'), ('12', 'Dec')]

class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    expense_in_payslip = fields.Boolean(
        string="Expense In Next Payslip", states={'done': [('readonly', True)], 'post': [('readonly', True)]},store=True)
    expense_payslip_id = fields.Many2one('hr.payslip', string="Payslip", readonly=True,store=True)
    active_payslip_id = fields.Boolean(
        string="Expense In Payslip",store=True)

    date_start = fields.Date('Date From', default=fields.Date.context_today)

    date_stop = fields.Date('Date To', default=fields.Date.context_today)

    # month = fields.Selection(MONTH_LIST, string='Month',
    #                          default=MONTH_LIST[int(datetime.now().strftime('%m')) - 1])
    #
    # year = fields.Selection([(str(num), str(num)) for num in range((datetime.now().year), 1900, -1)],
    #                                   string='Year', default=str(datetime.now().year))



    def expense_report_in_next_payslip(self):
        self.write({'expense_in_payslip': True})
        for record in self:
            record.message_post(
                body=_("Your expense (%s) will be added to your next payslip.") % (record.name),
                partner_ids=record.employee_id.user_id.partner_id.ids,
                subtype_id=self.env.ref('mail.mt_note').id,
                email_layout_xmlid='mail.mail_notification_light')
            if record.expense_line_ids:
                for expense in record.expense_line_ids:
                    if record.date_start > expense.date or expense.date>record.date_stop:
                        raise UserError(_("Cannot create an Expense Report"))

    def reset_expense_sheets(self):
        res = super().reset_expense_sheets()
        self.sudo().write({'expense_in_payslip': False})
        return res
