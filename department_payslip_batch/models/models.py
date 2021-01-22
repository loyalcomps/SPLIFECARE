# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError
from datetime import date, datetime, time
from collections import defaultdict
from odoo import api, fields, models
from odoo.tools import date_utils
from contextlib import contextmanager




class HrContract(models.Model):
    _inherit = 'hr.contract'


    def _generate_work_entries(self, date_start, date_stop):
        vals_list = []

        date_start = fields.Datetime.to_datetime(date_start)
        date_stop = datetime.combine(fields.Datetime.to_datetime(date_stop), datetime.max.time())

        for contract in self:
            # For each contract, we found each interval we must generate
            contract_start = fields.Datetime.to_datetime(contract.date_start)
            contract_stop = datetime.combine(fields.Datetime.to_datetime(contract.date_end or datetime.max.date()), datetime.max.time())
            last_generated_from = min(contract.date_generated_from, contract_stop)
            date_start_work_entries = max(date_start, contract_start)

            if last_generated_from > date_start_work_entries:
                contract.date_generated_from = date_start_work_entries
                vals_list.extend(contract._get_work_entries_values(date_start_work_entries, last_generated_from))

            last_generated_to = max(contract.date_generated_to, contract_start)
            date_stop_work_entries = min(date_stop, contract_stop)
            if last_generated_to < date_stop_work_entries:
                contract.date_generated_to = date_stop_work_entries
                vals_list.extend(contract._get_work_entries_values(last_generated_to, date_stop_work_entries))

        if not vals_list:
            return self.env['hr.work.entry']

        return self.env['hr.work.entry'].create(vals_list)

class HrWorkEntry(models.Model):
    _inherit = 'hr.work.entry'

    @api.model
    def _mark_conflicting_work_entries(self, start, stop):
        """
        Set `state` to `conflict` for overlapping work entries
        between two dates.
        Return True if overlapping work entries were detected.
        """
        # Use the postgresql range type `tsrange` which is a range of timestamp
        # It supports the intersection operator (&&) useful to detect overlap.
        # use '()' to exlude the lower and upper bounds of the range.
        # Filter on date_start and date_stop (both indexed) in the EXISTS clause to
        # limit the resulting set size and fasten the query.
        self.flush(['date_start', 'date_stop', 'employee_id', 'active'])
        query = """
                SELECT b1.id
                FROM hr_work_entry b1
                WHERE
                b1.date_start <= %s
                AND b1.date_stop >= %s
                AND active = TRUE
                AND EXISTS (
                    SELECT 1
                    FROM hr_work_entry b2
                    WHERE
                        b2.date_start <= %s
                        AND b2.date_stop >= %s
                        AND active = TRUE
                        AND tsrange(b1.date_start, b1.date_stop, '()') && tsrange(b2.date_start, b2.date_stop, '()')
                        AND b1.id <> b2.id
                        AND b1.employee_id = b2.employee_id
                );
            """
        self.env.cr.execute(query, (stop, start, stop, start))
        conflicts = [res.get('id') for res in self.env.cr.dictfetchall()]
        department=[]
        department_list = self.env.user.department_ids.ids
        for list in conflicts:
            if self.browse(list).department_id in department_list:
                department.append(list)
            else:
                department
        self.browse(department).write({
            'state': 'conflict',
        })
        return bool(department)

    @contextmanager
    def _error_checking(self, start=None, stop=None, skip=False):
        """
        Context manager used for conflicts checking.
        When exiting the context manager, conflicts are checked
        for all work entries within a date range. By default, the start and end dates are
        computed according to `self` (min and max respectively) but it can be overwritten by providing
        other values as parameter.
        :param start: datetime to overwrite the default behaviour
        :param stop: datetime to overwrite the default behaviour
        :param skip: If True, no error checking is done
        """
        try:
            skip = skip or self.env.context.get('hr_work_entry_no_check', False)
            start = start or min(self.mapped('date_start'), default=False)
            stop = stop or max(self.mapped('date_stop'), default=False)
            if not skip and start and stop:
                work_entries = self.sudo().with_context(hr_work_entry_no_check=True).search([
                    ('date_start', '<', stop),
                    ('date_stop', '>', start),
                    ('state', 'not in', ('validated', 'cancelled')),
                    ('company_id', 'in', self.env.user.company_ids.ids),
                    ('department_id', 'in', self.env.user.department_ids.ids)
                ])
                work_entries._reset_conflicting_state()
            yield
        finally:
            if not skip and start and stop:
                # New work entries are handled in the create method,
                # no need to reload work entries.
                work_entries = self.sudo().with_context(hr_work_entry_no_check=True).search([
                    ('date_start', '<', stop),
                    ('date_stop', '>', start),
                    ('state', 'not in', ('validated', 'cancelled')),
                    ('company_id', 'in', self.env.user.company_ids.ids),
                    ('department_id', 'in', self.env.user.department_ids.ids)
                ])
                work_entries.exists()._check_if_error()



class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'
    _description = 'Generate payslips for all selected employees'

    def _get_available_contracts_domain(self):
        res = super(HrPayslipEmployees, self)._get_available_contracts_domain()
        res.append(('department_id','in',self.env.user.department_ids.ids))
        return res



    def compute_sheet(self):
        self.ensure_one()
        if not self.env.context.get('active_id'):
            from_date = fields.Date.to_date(self.env.context.get('default_date_start'))
            end_date = fields.Date.to_date(self.env.context.get('default_date_end'))
            payslip_run = self.env['hr.payslip.run'].create({
                'name': from_date.strftime('%B %Y'),
                'date_start': from_date,
                'date_end': end_date,
            })
        else:
            payslip_run = self.env['hr.payslip.run'].browse(self.env.context.get('active_id'))

        if not self.employee_ids:
            raise UserError(_("You must select employee(s) to generate payslip(s)."))

        payslips = self.env['hr.payslip']
        Payslip = self.env['hr.payslip']

        contracts = self.employee_ids._get_contracts(payslip_run.date_start, payslip_run.date_end, states=['open', 'close'])
        contracts._generate_work_entries(payslip_run.date_start, payslip_run.date_end)
        work_entries = self.env['hr.work.entry'].search([
            ('date_start', '<=', payslip_run.date_end),
            ('date_stop', '>=', payslip_run.date_start),
            ('employee_id', 'in', self.employee_ids.ids),
            ('department_id', 'in', self.env.user.department_id.ids),
            ('company_id', 'in', self.env.user.company_ids.ids),
        ])
        self._check_undefined_slots(work_entries, payslip_run)

        validated = work_entries.action_validate()
        # if not validated:
        #     raise UserError(_("Some work entries could not be validated."))

        default_values = Payslip.default_get(Payslip.fields_get())
        for contract in contracts:
            values = dict(default_values, **{
                'employee_id': contract.employee_id.id,
                'credit_note': payslip_run.credit_note,
                'payslip_run_id': payslip_run.id,
                'date_from': payslip_run.date_start,
                'date_to': payslip_run.date_end,
                'contract_id': contract.id,
                'struct_id': self.structure_id.id or contract.structure_type_id.default_struct_id.id,
            })
            payslip = self.env['hr.payslip'].new(values)
            payslip._onchange_employee()
            values = payslip._convert_to_write(payslip._cache)
            payslips += Payslip.create(values)
        payslips.compute_sheet()
        payslip_run.state = 'verify'

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.payslip.run',
            'views': [[False, 'form']],
            'res_id': payslip_run.id,
        }

