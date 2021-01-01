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
    # sgst_rate = fields.Float(string="Rate")
    # cgst_rate = fields.Float(string="Rate")
    # cgst_amount = fields.Float(string="amount")
    # sgst_rate = fields.Float(string="Rate")
    # sgst_amount = fields.Float(string="amount")
    # igst_rate = fields.Float(string="Rate")
    # igst_amount = fields.Float(string="amount")
    # kfc_rate = fields.Float(string="Rate")
    # kfc_amount = fields.Float(string="amount")
    # total_amount = fields.Float(string="GST amount")


class Accountmove(models.Model):
    _inherit = 'account.move'

    gst_tax_ids=fields.One2many("hsn.tax","move_id",string="Hsn")

    # @api.onchange('invoice_line_ids')
    # def get_hsn(self):
    #     grouped_tax_lines = {}
    #     for invoice in self:
    #         a = []
    #         x = []
    #         flag = False
    #         for invoice_line in invoice.invoice_line_ids:
    #             if invoice_line.product_id:
    #                 prod_id = invoice_line.product_id.l10n_in_hsn_code
    #             else:
    #                 prod_id = 0.0
    #             line_amount = 0.0
    #             product_hsn = ""
    #             if invoice_line.quantity and invoice.type in ('out_refund', 'out_invoice'):
    #                 line_amount = invoice_line.price_subtotal
    #                 # product_hsn = invoice_line.product_id.hsn
    #             rate = 0.0
    #             gstDict = {
    #                 "cgst_rate": 0.0, "cgst_amount": 0.0,
    #                 "sgst_rate": 0.0, "sgst_amount": 0.0,
    #                 "igst_rate": 0.0, "igst_amount": 0.0,
    #                  "kfc_rate": 0.0, "kfc_amount": 0.0,
    #                 "gst": 0.0,
    #             }
    #             if self.line_ids:
    #                 for rateObj in self.line_ids:
    #                     if rateObj.tax_line_id.amount_type == "group":
    #                         for childObj in rateObj.tax_line_id.children_tax_ids:
    #                             if not childObj.cess and not childObj.kfc:
    #                                 rate = childObj.amount * 2
    #                                 break
    #                     else:
    #                         rate = rateObj.tax_line_id.amount
    #
    #                 for tax in self.line_ids:
    #                     if tax.tax_line_id:
    #                         if 'CGST' in tax.name:
    #                             gstDict['cgst_rate'] += tax.credit
    #                             gstDict['cgst_amount'] += tax.credit
    #                         if 'SGST' in tax.name:
    #                             gstDict['sgst_rate'] += tax.credit
    #                             gstDict['sgst_amount'] += tax.credit
    #                         if 'IGST' in tax.name:
    #                             gstDict['igst_rate'] += tax.credit
    #                             gstDict['igst_amount'] += tax.credit
    #                         if 'KFC' in tax.name:
    #                             gstDict['kfc_rate'] += tax.credit
    #                             gstDict['kfc_amount'] += tax.credit
    #
    #
    #             if grouped_tax_lines.get(prod_id):
    #                 if grouped_tax_lines[prod_id].get(rate):
    #                     grouped_tax_lines[prod_id][rate][0] += prod_id
    #                     grouped_tax_lines[prod_id][rate][1] += line_amount
    #                     grouped_tax_lines[prod_id][rate][2] += gstDict['cgst_rate']
    #                     grouped_tax_lines[prod_id][rate][3] += gstDict['cgst_amount']
    #                     grouped_tax_lines[prod_id][rate][4] += gstDict['sgst_rate']
    #                     grouped_tax_lines[prod_id][rate][5] += gstDict['sgst_amount']
    #                     grouped_tax_lines[prod_id][rate][6] += gstDict['igst_rate']
    #                     grouped_tax_lines[prod_id][rate][7] = gstDict['igst_amount']
    #                     grouped_tax_lines[prod_id][rate][8] = gstDict['kfc_rate']
    #                     grouped_tax_lines[prod_id][rate][9] += gstDict['kfc_amount']
    #                     grouped_tax_lines[prod_id][rate][10] =gstDict['gst']
    #
    #
    #             else:
    #                 grouped_tax_lines[prod_id] = {
    #                     rate: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    #                 grouped_tax_lines[prod_id][rate][0] = prod_id
    #                 grouped_tax_lines[prod_id][rate][1] += line_amount
    #                 grouped_tax_lines[prod_id][rate][2] += gstDict['cgst_rate']
    #                 grouped_tax_lines[prod_id][rate][3] += gstDict['cgst_amount']
    #                 grouped_tax_lines[prod_id][rate][4] += gstDict['sgst_rate']
    #                 grouped_tax_lines[prod_id][rate][5] += gstDict['sgst_amount']
    #                 grouped_tax_lines[prod_id][rate][6] += gstDict['igst_rate']
    #                 grouped_tax_lines[prod_id][rate][7] = gstDict['igst_amount']
    #                 grouped_tax_lines[prod_id][rate][8] = gstDict['kfc_rate']
    #                 grouped_tax_lines[prod_id][rate][9] += gstDict['kfc_amount']
    #                 grouped_tax_lines[prod_id][rate][10] = gstDict['gst']
    #
    #     # for place_of_supply, inv_tax_lines in grouped_tax_lines.items():
    #     for place_of_supply, inv_tax_lines in sorted(grouped_tax_lines.items(), key=lambda p: p[0]):
    #         # for product, tax_details in sorted(inv_tax_lines.items(), key=lambda s: s[0].id):
    #         s=1
                # for product, tax_details in inv_tax_lines.items():
                # for tax_id, base_amount in tax_details.items():
                #     # for invoice_det in place_of_supply:
                #
                #     ws1.write(row, col + 1, place_of_supply, line_content_style)


    # @api.onchange('invoice_line_ids')
    def get_hsn(self):
        # self.ensure_one()
        lines = []

        for i in self:

            gst_tax_lines = i._origin.gst_tax_ids
            mon1 = []

            invoice_date = i._origin.invoice_date if i._origin.invoice_date else datetime.strptime(str(fields.Date.today()),'%Y-%m-%d').strftime('%Y-%m-%d')

            # if i._origin.id == False:
            #     i.create()
            #     invoice = i._origin.id
            # else:
            #     invoice = i._origin.id
            #
            #
            # if i._origin.company_id:
            #     company=i._origin.company_id.id
            # else:
            #     company=i.env.user.company_id.id
            #

            query = """
                    select
            dd.id as move_id,
                max(dd.tax_name) as tax_name,
                dd.l10n_in_hsn_code as hsn,
                max(dd.tax_base_amount) as taxable,
                dd.rate as rate,
                               sum(dd.credit) as amount
                from (select m.id as id,at.name as tax_name,pt.l10n_in_hsn_code,ml.tax_base_amount,
                      case when at.amount=1 then at.amount end as rate,(ml.credit) as credit
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
                lines.append(so_order)

            # if lines:
            #
            #     return lines
            # else:
            #     return []
    #             so = self.env['hsn.tax'].create(so_order)
    #         i._origin.gst_tax_ids = so
    #             #
                gst_tax_lines += gst_tax_lines.create(so_order)
            i._origin.gst_tax_ids = gst_tax_lines
            return
