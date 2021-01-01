# # -*- coding: utf-8 -*-
#
from odoo import api, fields, models, tools,_
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp
from datetime import datetime

# # import odoo.addons.decimal_precision as dp
#
#
class Hsntax(models.Model):
    _name = 'hsn.tax'
    _description = 'HSN'

    taxable = fields.Float(string="Taxable Value", digits=(16, 4))
    move_id = fields.Many2one("account.move", string="Invoice")
    tax_name = fields.Char(string="Tax")
    hsn = fields.Char(string="hsn")
    rate = fields.Float(string="Rate")
    amount = fields.Float(string="amount")


class Accountmove(models.Model):
    _inherit = 'account.move'

    gst_tax_ids=fields.One2many("hsn.tax","move_id",string="Hsn")

    def get_hsn(self):
        lines = []

        for i in self:
            i._origin.gst_tax_ids.unlink()

            gst_tax_lines = i._origin.gst_tax_ids
            mon1 = []

            invoice_date = i._origin.invoice_date if i._origin.invoice_date else datetime.strptime(str(fields.Date.today()),'%Y-%m-%d').strftime('%Y-%m-%d')

            query = """
                    select
            dd.id as move_id,
                max(dd.tax_name) as tax_name,
                dd.l10n_in_hsn_code as hsn,
                max(dd.tax_base_amount) as taxable,
                dd.rate as rate,
                               sum(dd.credit) as amount
                from (select m.id as id,at.name as tax_name,pt.l10n_in_hsn_code,ml.tax_base_amount,
                      case when at.amount=1 and at.name !~~* 'IGST%%' then at.amount
                      when at.amount<>1 and at.name !~~* 'IGST%%' then at.amount
                            when at.name ~~* 'IGST%%' then at.amount end as rate,(ml.credit) as credit
                  from account_move_line as ml
                    left join account_move as m on (ml.move_id=m.id)
                    left join account_tax as at on at.id=ml.tax_line_id
                    LEFT JOIN product_product product ON (product.id=ml.product_id)
                    LEFT JOIN product_template pt ON (pt.id = product.product_tmpl_id)

                    where
                    
                     m.id = %s
                     and ml.exclude_from_invoice_tab=true
                    and ml.tax_line_id is not null)dd group by dd.l10n_in_hsn_code,dd.rate,dd.id

                """

            self.env.cr.execute(query, (i._origin.id,))

            total_work = 0
            for ans1 in self.env.cr.dictfetchall():
                move_id = ans1['move_id'] if ans1['move_id'] else 0
                tax_name = ans1['tax_name'] if ans1['tax_name'] else " "
                hsn = ans1['hsn'] if ans1['hsn'] else 0
                taxable = ans1['taxable'] if ans1['taxable'] else 0
                rate = ans1['rate'] if ans1['rate'] else 0
                amount = ans1['amount'] if ans1['amount'] else 0

                so_order = {
                    'move_id': move_id if move_id else 0,
                    'tax_name': tax_name if tax_name else 0,
                    'hsn': hsn if hsn else False,
                    'taxable': taxable if taxable else 0,
                    'rate': rate if rate else 0,
                    'amount': amount if amount else 0,
                }
                gst_tax_lines += gst_tax_lines.create(so_order)
            i._origin.gst_tax_ids = gst_tax_lines
            return

