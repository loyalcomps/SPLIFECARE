# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'
    _description = 'Generate payslips for all selected employees'

    employee_structure_type_id = fields.Many2one('hr.payroll.structure.type', string='Employee Salary Structure Type')

    @api.depends()
    def _get_available_contracts_domain(self):
        res = super(HrPayslipEmployees, self)._get_available_contracts_domain()
        res.append(('contract_ids.structure_type_id','=',self.employee_structure_type_id.id))
        return res

    @api.depends('employee_structure_type_id')
    def _get_employees(self):
        # YTI check dates too
        res= super(HrPayslipEmployees, self)._get_employees()
        return res

    @api.onchange('employee_structure_type_id')
    def _onchange_structure_type(self):
        self.employee_ids = self._get_employees()
        # s = [4,0,(self.env['hr.employee'].search(self._get_available_contracts_domain()).ids)]
