# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    hr_expense_sheet_ids = fields.One2many(
        'hr.expense.sheet', 'expense_payslip_id', string='Expenses',
        help="Expenses to reimburse to employee.",
        states={'draft': [('readonly', False)], 'verify': [('readonly', False)]})
    hr_expenses_count = fields.Integer(compute='_compute_payslip_expenses_count',store=True)

    @api.depends('hr_expense_sheet_ids.expense_line_ids', 'hr_expense_sheet_ids.expense_payslip_id')
    def _compute_payslip_expenses_count(self):
        for payslip in self:
            payslip.hr_expenses_count = len(payslip.mapped('hr_expense_sheet_ids.expense_line_ids'))

    # @api.onchange('input_line_ids')
    # def _onchange_input_line_ids(self):
    #     expense_type = self.env.ref('expense_in_payslip.payslip_expense_input_type', raise_if_not_found=False)
    #     if not self.input_line_ids.filtered(lambda line: line.input_type_id == expense_type):
    #         self.hr_expense_sheet_ids.write({'expense_payslip_id': False})

    @api.onchange('employee_id', 'struct_id', 'contract_id', 'date_from', 'date_to')
    def _onchange_employee(self):
        res = super()._onchange_employee()
        if self.state == 'draft':
            self.hr_expense_sheet_ids = self.env['hr.expense.sheet'].search([
                ('employee_id', '=', self.employee_id.id),
                ('state', '=', 'approve'),
                ('payment_mode', '=', 'own_account'),
                ('expense_in_payslip', '=', True),
                ('date_start', '>=', self.date_from),
                ('date_stop', '<=', self.date_to),
                ('active_payslip_id', '=', False)
                # ('expense_payslip_id', '=', False)
            ])

            # self._onchange_expense_sheet_ids()
        return res

    # @api.onchange('hr_expense_sheet_ids')
    # def _onchange_expense_sheet_ids(self):
    #     expense_type = self.env.ref('expense_in_payslip.payslip_expense_input_type', raise_if_not_found=False)
    #     if not expense_type:
    #         return
    #
    #     total = sum(sheet.total_amount for sheet in self.hr_expense_sheet_ids)
    #     if not total:
    #         return
    #
    #     lines_to_keep = self.input_line_ids.filtered(lambda x: x.input_type_id != expense_type)
    #     input_lines_vals = [(5, 0, 0)] + [(4, line.id, False) for line in lines_to_keep]
    #     input_lines_vals.append((0, 0, {
    #         'amount': total,
    #         'input_type_id': expense_type
    #     }))
    #     self.update({'input_line_ids': input_lines_vals})

    def action_payslip_done(self):
        res = super(HrPayslip, self).action_payslip_done()
        for expense in self.hr_expense_sheet_ids:
            expense.write({'active_payslip_id': True})
            expense.action_sheet_move_create()
            expense.set_to_paid()
        return res

    def payslip_expenses(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Reimbursed Expenses'),
            'res_model': 'hr.expense',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.mapped('hr_expense_sheet_ids.expense_line_ids').ids)],
        }
