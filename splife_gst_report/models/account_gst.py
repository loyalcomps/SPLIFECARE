# -*- coding: utf-8 -*-

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools import float_is_zero
from odoo import models, fields, api

class account_GSTtax(models.Model):
    _name = 'account.gst.tax'
    _description = 'GST Tax'

    move_id = fields.Many2one("account.move", string="Invoice")
    karkkidaka_kit_account = fields.Many2one('account.account',string="Karkkidaka Kit Sale")
    cgst_tax = fields.Float(string="CGST")
    sgst_tax = fields.Float(string="SGST")
    kfc_tax = fields.Float(string="KFC")
    registration_fee_account = fields.Many2one('account.account',string="Registration Fee @18%")
    reg_cgst_tax = fields.Float(string="CGST")
    reg_sgst_tax = fields.Float(string="SGST")
    reg_kfc_tax = fields.Float(string="KFC")


class AccountMove(models.Model):
    _inherit='account.move'


    @api.onchange('invoice_line_ids')
    def account_gst_onchange_invoice_line_ids(self):
        mon1 = []

        for i in self:
            if i.id:
                self._cr.execute("DELETE FROM account_gst_tax WHERE move_id=%s", (i.id,))
                # if self._cr.rowcount:
                self.invalidate_cache()

         # Generate one tax line per tax, however many invoice lines it's applied to

        taxes_grouped = self.account_generate_tax()
        gst_tax_lines = self.account_gst_tax_ids.browse([])
        gst_val = {}

        for place_of_supply, inv_tax_lines in taxes_grouped.items():  # invoice_gst_tax_lines.items():
            s = 1
            so_order = {
                # 'move_id': inv_tax_lines[0] if inv_tax_lines[0] else 0,
                'karkkidaka_kit_account': inv_tax_lines[0].id if inv_tax_lines[0].gst_report_accounts =='karkkidaka_kit_sale' else 0,
                'cgst_tax': inv_tax_lines[1] if inv_tax_lines[1] else 0,
                'sgst_tax': inv_tax_lines[2] if inv_tax_lines[2] else 0,
                'kfc_tax': inv_tax_lines[3] if inv_tax_lines[3] else 0,
                'registration_fee_account': inv_tax_lines[0].id if inv_tax_lines[0].gst_report_accounts == 'registration_fee' else 0,
                'reg_cgst_tax': inv_tax_lines[6] if inv_tax_lines[6] else 0,
                'reg_sgst_tax': inv_tax_lines[7] if inv_tax_lines[7] else 0,
                'reg_kfc_tax': inv_tax_lines[8] if inv_tax_lines[8] else 0,

            }
            mon3 = (0, 0, so_order)
            mon1.append(mon3)
        self.update({

            'account_gst_tax_ids': mon1
        })
        #     gst_tax_lines += gst_tax_lines.create(so_order)
        #
        # self.account_gst_tax_ids = gst_tax_lines
        s = 1
        return

    # @api.onchange('line_ids')
    def account_generate_tax(self):
        # self.gst_tax_ids.unlink()

        grouped_tax_lines = {}
        gst_tax_lines = self.account_gst_tax_ids
        duplicate_line_tax = {}

        for invoice_line in self.invoice_line_ids:
            move_id = self.id
            if invoice_line.discount:
                price = invoice_line.price_unit * (1 - (invoice_line.discount or 0.0) / 100.0)
            else:
                price = invoice_line.price_unit

            line_taxes = invoice_line.tax_ids.compute_all(price, invoice_line.move_id.currency_id,
                                                          invoice_line.quantity,
                                                          product=invoice_line.product_id,
                                                          partner=invoice_line.move_id.partner_id)

            duplicate_line_tax = line_taxes



            gstDict = {
                "ka_rt": 0.0, "ka_iamt": 0.0, "ka_gst": 0.0, "ka_csamt": 0.0,
                "ka_kfc": 0.0, "ka_kfc_rate": 0.0, "ka_kfc_count": 0.0,
                "ka_cgst": 0.0,"ka_sgst": 0.0,
                "re_rt": 0.0, "re_iamt": 0.0, "re_gst": 0.0, "re_csamt": 0.0,
                "re_kfc": 0.0, "re_kfc_rate": 0.0, "re_kfc_count": 0.0,
                "re_cgst": 0.0, "re_sgst": 0.0
            }

            if invoice_line.tax_ids:
                for tax_value in invoice_line.tax_ids:
                    if tax_value.amount==12 and invoice_line.account_id.gst_report_accounts == 'karkkidaka_kit_sale':
                        for tax_line in line_taxes['taxes']:
                            if 'IGST' in tax_line['name']:
                                gstDict['ka_iamt'] += tax_line['amount']
                            elif 'CGST' in tax_line['name']:
                                gstDict['ka_cgst'] += tax_line['amount']
                            elif 'SGST' in tax_line['name'] or 'UTGST' in tax_line['name']:
                                gstDict['ka_sgst'] += tax_line['amount']
                            elif 'kfc' in tax_line['name'].lower():
                                gstDict['ka_kfc'] += tax_line['amount']
                            else:
                                gstDict['csamt'] += tax_line['amount']
                    if tax_value.amount==18 and invoice_line.account_id.gst_report_accounts == 'registration_fee':
                        for tax_line in line_taxes['taxes']:
                            if 'IGST' in tax_line['name']:
                                gstDict['re_iamt'] += tax_line['amount']
                            elif 'CGST' in tax_line['name']:
                                gstDict['re_cgst'] += tax_line['amount']
                            elif 'SGST' in tax_line['name'] or 'UTGST' in tax_line['name']:
                                gstDict['re_sgst'] += tax_line['amount']
                            elif 'kfc' in tax_line['name'].lower():
                                gstDict['re_kfc'] += tax_line['amount']
                            else:
                                gstDict['re_csamt'] += tax_line['amount']


            gst_account_id = invoice_line.account_id
            gst_account_name = invoice_line.account_id.name
            rate = 0.0

            if grouped_tax_lines.get(gst_account_id):
                grouped_tax_lines[gst_account_id][0] = gst_account_id
                grouped_tax_lines[gst_account_id][1] += gstDict['ka_cgst']
                grouped_tax_lines[gst_account_id][2] += gstDict['ka_sgst']
                grouped_tax_lines[gst_account_id][3] += gstDict['ka_kfc']
                grouped_tax_lines[gst_account_id][4] += gstDict['ka_csamt']
                grouped_tax_lines[gst_account_id][5] += gstDict['ka_iamt']

                grouped_tax_lines[gst_account_id][6] += gstDict['re_cgst']
                grouped_tax_lines[gst_account_id][7] += gstDict['re_sgst']
                grouped_tax_lines[gst_account_id][8] += gstDict['re_kfc']
                grouped_tax_lines[gst_account_id][9] += gstDict['re_csamt']
                grouped_tax_lines[gst_account_id][10] += gstDict['re_iamt']
                grouped_tax_lines[gst_account_id][11] = move_id

            else:
                grouped_tax_lines[gst_account_id] = [0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0,0]
                grouped_tax_lines[gst_account_id][0] = gst_account_id
                grouped_tax_lines[gst_account_id][1] += gstDict['ka_cgst']
                grouped_tax_lines[gst_account_id][2] += gstDict['ka_sgst']
                grouped_tax_lines[gst_account_id][3] += gstDict['ka_kfc']
                grouped_tax_lines[gst_account_id][4] += gstDict['ka_csamt']
                grouped_tax_lines[gst_account_id][5] += gstDict['ka_iamt']

                grouped_tax_lines[gst_account_id][6] += gstDict['re_cgst']
                grouped_tax_lines[gst_account_id][7] += gstDict['re_sgst']
                grouped_tax_lines[gst_account_id][8] += gstDict['re_kfc']
                grouped_tax_lines[gst_account_id][9] += gstDict['re_csamt']
                grouped_tax_lines[gst_account_id][10] += gstDict['re_iamt']
                grouped_tax_lines[gst_account_id][11] = move_id





        return grouped_tax_lines


    account_gst_tax_ids = fields.One2many("account.gst.tax", "move_id", string="Tax",)


    def account_compute_taxes(self):
        """Function used in other module to compute the taxes on a fresh invoice created (onchanges did not applied)"""
        account_invoice_tax = self.env['account.gst.tax']
        ctx = dict(self._context)
        for invoice in self:
            # Delete non-manual tax lines
            if self.type not in ['out_refund','in_refund', 'out_receipt', 'in_receipt']:

                self._cr.execute("DELETE FROM account_gst_tax WHERE move_id=%s", (invoice.id,))
                # if self._cr.rowcount:
                self.invalidate_cache()

                # Generate one tax line per tax, however many invoice lines it's applied to
                tax_grouped = invoice.account_generate_tax()

                # Create new tax lines
                # if self.type not in ['out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt']:
                for tax in tax_grouped.values():
                    account_invoice_tax.create(tax)
            else:
                self.account_gst_onchange_invoice_line_ids()

        # dummy write on self to trigger recomputations
        return
        # return self.with_context(ctx).write({'invoice_line_ids': []})

    @api.model
    def create(self, vals):
        request=super(AccountMove, self).create(vals)

        if any(line.tax_ids for line in request.invoice_line_ids) and not request.account_gst_tax_ids:
            request.account_compute_taxes()
        return request

    @api.model
    def write(self, vals):
        request = super(AccountMove, self).write(vals)

        for taxes in self:
            if any(line.tax_ids for line in taxes.invoice_line_ids) and not taxes.account_gst_tax_ids:
                taxes.account_compute_taxes()
        return request



class Account_account(models.Model):
    _inherit = "account.account"

    gst_report_accounts = fields.Selection(selection=[
        ('retention_fee', 'Retention Fee'),
        ('revenue_from_physiotherapy', 'Revenue From Physiotherapy'),
        ('revenue_from_yoga', 'Revenue From Yoga'),
        ('ayurvedic_treatment', 'Ayurvedic Treatment'),
        ('beauty_treatment', 'Beauty Treatment'),
        ('medicine_sale_ayurlaya', 'Medicine Sale Ayurlaya'),
        ('gp_consultancy_revenue', 'G P Consultancy Revenue'),
        ('lab_test_revenue', 'Lab Test Revenue'),
        ('karkkidaka_kit_sale', 'Karkkidaka Kit Sale'),
        ('registration_fee', 'Registration Fee @18%')
    ], string='GST Report', tracking=True,
        )

    gst_report = fields.Boolean(default=False,store=True,string="GST Report")
    # gst_registration_fee = fields.Boolean(default=False, store=True,string="Registration Fee")