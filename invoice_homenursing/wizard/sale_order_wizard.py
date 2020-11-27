# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProjecttimesheetCreateSalesOrder(models.TransientModel):
    _name = 'project.timesheet.create.sale.order'
    _description = "Create SO from timesheet"

    # @api.model
    # def default_get(self, fields):
    #     result = super(ProjecttimesheetCreateSalesOrder, self).default_get(fields)
    #
    #     active_model = self._context.get('active_model')
    #     if active_model != 'account.analytic.line':
    #         raise UserError(_("You can only apply this action from a Timesheet."))
    #
    #     active_id = self._context.get('active_id')
    #     if 'project_id' in fields and active_id:
    #         project = self.env['project.project'].browse(active_id)
    #         if project.billable_type != 'no':
    #             raise UserError(_("The project is already billable."))
    #         result['project_id'] = active_id
    #         result['partner_id'] = project.partner_id.id
    #     return result

    date_from = fields.Date(string='Start Date', required=True, default=fields.Date.today, )
    date_to = fields.Date(string='End Date', required=True, default=fields.Date.today, )


    project_id = fields.Many2one('project.project', "Project", domain=[('sale_line_id', '=', False)], help="Project for which we are creating a sales order", required=True)

    partner_id = fields.Many2one('res.partner', string="Customer", help="Customer of the sales order",related='project_id.partner_id',store=True)
    price_unit = fields.Float("Unit Price", help="Unit price of the sales order item.",related='project_id.rate_per_shift',store=True)
    product_uom_qty = fields.Float(string='Quantity', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    product_id = fields.Many2one('product.product',domain=[('timesheet_product', '=', True)], required=True)

    # product_id = fields.Many2one('product.product', domain=[('type', '=', 'service'), ('invoice_policy', '=', 'delivery'), ('service_type', '=', 'timesheet')], string="Service", help="Product of the sales order item. Must be a service invoiced based on timesheets on tasks. The existing timesheet will be linked to this product.", required=True)


    # currency_id = fields.Many2one('res.currency', string="Currency", related='product_id.currency_id', readonly=False)

    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     if self.product_id:
    #         self.price_unit = self.product_id.lst_price
    #     else:
    #         self.price_unit = 0.0
    # @api.depends('project_id')
    # def _compute_product_uom_qty(self):
#         query3 = """
#
# select sum(total_no_of_shift) as total_shift from account_analytic_line as a
# 				left join project_project as p on a.project_id= p.id
# 				 where to_char(date_trunc('day',a.date),'YYYY-MM-DD')::date between %s and %s
# 				 and a.company_id=%s and a.project_id=%s
# 				 and allow_billable=false
# 				 group by a.id
#
#                                                 """
#
#         self.env.cr.execute(query3, (
#         self.date_from,self.date_to,self.company_id.id, self.project_id.id))
#
#         total_shift = 0
#         for ans1 in self.env.cr.dictfetchall():
#             total_shift = ans1['total_shift'] if ans1['total_shift'] else 0
#
#         res = {
#
#             'total_shift': total_shift if total_shift else 0.0,
#         }
#
#         self.product_uom_qty = res['total_shift']
#         return


    def action_create_sale_order(self):
        sale_order = self._prepare_sale_order()
        sale_order.action_confirm()
        view_form_id = self.env.ref('sale.view_order_form').id
        action = self.env.ref('sale.action_orders').read()[0]
        action.update({
            'views': [(view_form_id, 'form')],
            'view_mode': 'form',
            'name': sale_order.name,
            'res_id': sale_order.id,
        })
        return action

    def _prepare_sale_order(self):
        # if task linked to SO line, then we consider it as billable.
        # if self.project_id.sale_line_id:
        #     raise UserError(_("The task is already linked to a sales order item."))
        #

        timesheet_with_so_line = self.env['account.analytic.line'].search_count([('project_id', '=', self.project_id.id), ('date', '>=', self.date_from),('date', '<=',self.date_to),('allow_billable','=', False)])
        if timesheet_with_so_line:
            pass
        else:
            raise UserError(_('The sales order cannot be created because some timesheets are already linked to another sales order.'))

        # create SO
        sale_order = self.env['sale.order'].create({
            'partner_id': self.project_id.partner_id.id,
            'company_id': self.project_id.company_id.id,
            'analytic_account_id': self.project_id.analytic_account_id.id,
        })
        sale_order.onchange_partner_id()
        sale_order.onchange_partner_shipping_id()

        query3 = """

        select sum(total_no_of_shift) as total_shift from account_analytic_line as a
        				left join project_project as p on a.project_id= p.id
        				 where to_char(date_trunc('day',a.date),'YYYY-MM-DD')::date between %s and %s
        				 and a.company_id=%s and a.project_id=%s
        				 and a.allow_billable=false
        				 group by a.project_id

                                                        """

        self.env.cr.execute(query3, (
            self.date_from, self.date_to, self.company_id.id, self.project_id.id))

        total_shift = 0
        for ans1 in self.env.cr.dictfetchall():
            total_shift = ans1['total_shift'] if ans1['total_shift'] else 0

        res = {

            'total_shift': total_shift if total_shift else 0.0,
        }

        self.product_uom_qty = res['total_shift']

        sale_order_line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'product_id': self.product_id.id,
            'price_unit': self.price_unit,
            'project_id': self.project_id.id,  # prevent to re-create a project on confirmation
            # 'task_id': self.task_id.id,
            'product_uom_qty': self.product_uom_qty,
        })

        # link task to SOL
        # self.task_id.write({
        #     'sale_line_id': sale_order_line.id,
        #     'partner_id': sale_order.partner_id.id,
        #     'email_from': sale_order.partner_id.email,
        # })

        # assign SOL to timesheets
        self.env['account.analytic.line'].search([('project_id', '=', self.project_id.id), ('date', '>=', self.date_from),('date', '<=',self.date_to)]).write({
            'allow_billable': True
        })

        return sale_order
