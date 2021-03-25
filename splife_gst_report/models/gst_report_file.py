# -*- coding: utf-8 -*-

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools import float_is_zero
from odoo import models, fields, api
from io import BytesIO
# import cStringIO
import xlwt
from datetime import datetime
import base64

def _unescape(text):
    from urllib.parse import unquote_plus

    # from urllib import unquote_plus
    try:
        text = unquote_plus(text.encode('utf8'))
        return text
    except Exception as e:
        return text

class GSTREPORT(models.TransientModel):
    _name = 'gst.report.wizard'

    date_from = fields.Date('Date From',required=True,default=fields.Date.context_today)
    date_to = fields.Date('Date To',required=True,default=fields.Date.context_today)
    state = fields.Selection([('choose', 'choose'), ('get', 'get')],
                             default='choose')

    company_id = fields.Many2one('res.company', string='Company',required=True,
                                 default=lambda self: self.env['res.company']._company_default_get(
                                     'gst.report.wizard'))



    report = fields.Binary('Prepared file', filters='.xls', readonly=True)
    name = fields.Char('File Name', size=128)

    sorted_invoices = []
    pos_sorted_orders = []

    def get_valid_invoices(self):
        # Searching for customer invoices
        from_date = datetime.strptime(str(self.date_from), '%Y-%m-%d').date()
        to_date = datetime.strptime(str(self.date_to), '%Y-%m-%d').date()
        company_id=self.company_id.id

        # Get all invoices
        all_invoices = self.env['account.move'].search(
            [('invoice_date', '>=', from_date), ('invoice_date', '<=', to_date),('state', 'in', ['posted']),('type', '=', 'out_invoice'),
             ('company_id','=',company_id)])



        self.sorted_invoices = all_invoices.sorted(key=lambda p: (p.invoice_date, p.name))



    def generate_gstrsale_report(self):
        # Error handling is not taken into consideraion
        self.ensure_one()
        fp = BytesIO()
        xl_workbook = xlwt.Workbook(encoding='utf-8')

        from_date = datetime.strptime(str(self.date_from), '%Y-%m-%d').date()
        to_date = datetime.strptime(str(self.date_to), '%Y-%m-%d').date()

        # Get the invoices
        self.get_valid_invoices()

        self.generate_gst_report(xl_workbook)

        xl_workbook.save(fp)

        out = base64.encodestring(fp.getvalue())
        self.write({'state': 'get',
                    'report': out,
                    'name': 'GST' + str(from_date) + '-' + str(to_date) + '.xls'
                    })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'gst.report.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    """ GST Report """

    def category_gst_report(self):
        from_date = datetime.strptime(str(self.date_from), '%Y-%m-%d').date()
        to_date = datetime.strptime(str(self.date_to), '%Y-%m-%d').date()
        company_id = self.company_id.id

        lines = []
        res = {}


        query = '''
                    select * from
				
				(select am.invoice_date,
	   			max(rs.name) as partner_name,
				am.partner_id,
				am.journal_id,
				max(aj.name) as journal_name, 
				am.id as move_id,
               am.name as invoice_number,
			    COALESCE(sum(CASE WHEN aa.name ='Round Off' THEN aml.price_subtotal ELSE 0 END ),0)  as round_off,
			    COALESCE(sum(CASE WHEN aa.gst_report_accounts ='retention_fee' THEN aml.price_subtotal ELSE 0 END ),0)  as retention_fee,
			    COALESCE(sum(CASE WHEN aa.gst_report_accounts ='revenue_from_physiotherapy' THEN aml.price_subtotal ELSE 0 END ),0)  as revenue_from_physiotherapy,
			    COALESCE(sum(CASE WHEN aa.gst_report_accounts ='revenue_from_yoga' THEN aml.price_subtotal ELSE 0 END ),0)  as revenue_from_yoga,
			    COALESCE(sum(CASE WHEN aa.gst_report_accounts ='ayurvedic_treatment' THEN aml.price_subtotal ELSE 0 END ),0)  as ayurvedic_treatment,
			    COALESCE(sum(CASE WHEN aa.gst_report_accounts ='beauty_treatment' THEN aml.price_subtotal ELSE 0 END ),0)  as beauty_treatment,
			    COALESCE(sum(CASE WHEN aa.gst_report_accounts ='medicine_sale_ayurlaya' THEN aml.price_subtotal ELSE 0 END ),0)  as medicine_sale_ayurlaya,
			    COALESCE(sum(CASE WHEN aa.gst_report_accounts ='gp_consultancy_revenue' THEN aml.price_subtotal ELSE 0 END ),0)  as gp_consultancy_revenue,
			    COALESCE(sum(CASE WHEN aa.gst_report_accounts ='lab_test_revenue' THEN aml.price_subtotal ELSE 0 END ),0)  as lab_test_revenue,
			    COALESCE(sum(CASE WHEN aa.gst_report_accounts ='karkkidaka_kit_sale' THEN aml.price_subtotal ELSE 0 END ),0)  as karkkidaka_kit_sale,
			    COALESCE(sum(CASE WHEN aa.gst_report_accounts ='registration_fee' THEN aml.price_subtotal ELSE 0 END ),0)  as registration_fee,
			    
			 
   				COALESCE(sum(CASE WHEN aml.price_subtotal>0 THEN aml.price_subtotal ELSE 0 END ),0)  as line_sub_total,
   				COALESCE(sum(CASE WHEN aml.price_total>0 THEN aml.price_total ELSE 0 END ),0)  as price_total,

  				am.amount_total 
				from account_move_line as aml
	 			left join account_move as am on aml.move_id= am.id
	 			 
	  			left join account_account as aa on aa.id=aml.account_id
          left join account_journal as aj on (aj.id= am.journal_id)
          left join res_partner as rs on am.partner_id=rs.id
		  

          where am.type in ('out_invoice','out_refund') and am.state in ('posted')
          and am.invoice_date BETWEEN %s and %s
		  and aml.exclude_from_invoice_tab = false
		 and am.company_id = %s
		  and aa.gst_report =true
          GROUP BY  am.id) as a
		  
		  left join 
		  (
			  
			  select 
			   sum(agx.cgst_tax) as cgst_tax,
			    sum(agx.sgst_tax) as sgst_tax,
			    sum(agx.kfc_tax) as kfc_tax,
			    sum(agx.reg_cgst_tax) as reg_cgst_tax,
			    sum(agx.reg_sgst_tax) as reg_sgst_tax,
			    sum(agx.reg_kfc_tax) as reg_kfc_tax,
			  am.id as move_id
			    
				from account_gst_tax as agx
	 			left join account_move as am on agx.move_id= am.id
	 			 
	  			
          where am.type in ('out_invoice','out_refund') and am.state in ('posted')
          and am.invoice_date BETWEEN %s and %s
		 
		 and am.company_id = %s
          GROUP BY  am.id
		  
		  )b on a.move_id= b.move_id
		  		  
		  order by invoice_date
                           '''

        self.env.cr.execute(query, (self.date_from, self.date_to, self.company_id.id,self.date_from, self.date_to, self.company_id.id))
        for row in self.env.cr.dictfetchall():



            res = {
                'invoice_date': datetime.strptime(str(row['invoice_date'] ),'%Y-%m-%d').strftime('%d-%m-%Y') if row['invoice_date'] else " ",
                'partner_name': row['partner_name'] if row['partner_name'] else " ",
                'journal_name':row['journal_name'] if row['journal_name'] else " ",
                'journal_id':self.env['account.journal'].browse(row['journal_id']).name if row['journal_id'] else " ",
                'invoice_number': row['invoice_number'] if row['invoice_number'] else " ",
                'transaction_type': self.env['res.partner'].browse(row['partner_id']).property_account_receivable_id.name if row['partner_id'] else " ",
                'line_sub_total': row['line_sub_total'] if row['line_sub_total'] else 0.00,

                'amount_total': row['price_total'] if row['price_total'] else 0.00,

                'total_amount_total': row['amount_total'] if row['amount_total'] else 0.00,
                'round_off': self.env['account.move'].browse(row['move_id']).invoice_cash_rounding_id.rounding if row['move_id'] else 0.00,

                'retention_fee':row['retention_fee'] if row['retention_fee'] else 0.00,
                'revenue_from_physiotherapy':row['revenue_from_physiotherapy'] if row['revenue_from_physiotherapy'] else 0.00,
                'revenue_from_yoga':row['revenue_from_yoga'] if row['revenue_from_yoga'] else 0.00,
                'ayurvedic_treatment':row['ayurvedic_treatment'] if row['ayurvedic_treatment'] else 0.00,
                'beauty_treatment':row['beauty_treatment'] if row['beauty_treatment'] else 0.00,
                'medicine_sale_ayurlaya':row['medicine_sale_ayurlaya'] if row['medicine_sale_ayurlaya'] else 0.00,
                'gp_consultancy_revenue':row['gp_consultancy_revenue'] if row['gp_consultancy_revenue'] else 0.00,
                'lab_test_revenue':row['lab_test_revenue'] if row['lab_test_revenue'] else 0.00,
                'karkkidaka_kit_sale':row['karkkidaka_kit_sale'] if row['karkkidaka_kit_sale'] else 0.00,
                'registration_fee':row['registration_fee'] if row['registration_fee'] else 0.00,

                'cgst_tax': row['cgst_tax'] if row['cgst_tax'] else 0.00,
                'sgst_tax': row['sgst_tax'] if row['sgst_tax'] else 0.00,
                'kfc_tax': row['kfc_tax'] if row['kfc_tax'] else 0.00,
                'reg_cgst_tax': row['reg_cgst_tax'] if row['reg_cgst_tax'] else 0.00,
                'reg_kfc_tax': row['reg_kfc_tax'] if row['reg_kfc_tax'] else 0.00,
                'reg_sgst_tax': row['reg_sgst_tax'] if row['reg_sgst_tax'] else 0.00,

            }
            lines.append(res)
        if lines:
            return lines
        else:
            return []

    def generate_gst_report(self, wb1):

        linesv=[]
        # Error handling is not taken into consideraion
        self.ensure_one()

        ws1 = wb1.add_sheet('GST REPORT')

        fp = BytesIO()

        # Content/Text style
        header_content_style = xlwt.easyxf("font: name Arial size 12 px, bold 1, height 170;")
        sub_header_style = xlwt.easyxf("font: name Arial size 10 px, bold 1, height 170; align: horiz center")
        sub_header_content_style = xlwt.easyxf("font: name Arial size 10 px, height 170;")
        line_content_style = xlwt.easyxf("font: name Arial, height 170;")
        row = 1
        col = -1
        ws1.row(row).height = 500
        # ws1.write_merge(row, row, col + 1, col + 6, "GST REPORT", header_content_style)

        row += 2
        ws1.write(row, col + 1, "From:", sub_header_style)
        ws1.write(row, col + 2, self.format_date(self.date_from), sub_header_content_style)
        row += 1
        ws1.write(row, col + 1, "To:", sub_header_style)
        ws1.write(row, col + 2, self.format_date(self.date_to), sub_header_content_style)
        row += 1
        ws1.write(row, col + 1, "GSTIN", sub_header_style)
        ws1.write(row, col + 2, self.env.user.company_id.vat, sub_header_content_style)
        row += 1


        ws1.write(row, col + 1, "Legal name of the registered person", sub_header_style)
        ws1.write(row, col + 2, self.env.user.company_id.name, sub_header_content_style)
        row += 1


        line_column = (col + 5) + 1

        config = []
        tax_config = []
        un = []
        tax = []

        ws1.write(row, col + 1, "Date", sub_header_style)
        ws1.write(row, col + 2, "Transaction Type", sub_header_style)
        ws1.write(row, col + 3, "Consignee/Buyer", sub_header_style)
        ws1.write(row, col + 4, "Voucher Type", sub_header_style)
        ws1.write(row, col + 5, "Voucher No", sub_header_style)
        ws1.write(row, col + 6, "Retention Fee", sub_header_style)
        ws1.write(row, col + 7, "Revenue From Physiotherapy", sub_header_style)
        ws1.write(row, col + 8, "Revenue From Yoga", sub_header_style)
        ws1.write(row, col + 9, "Ayurvedic Treatment", sub_header_style)
        ws1.write(row, col + 10, "Beauty Treatment", sub_header_style)
        ws1.write(row, col + 11, "Medicine Sale Ayurlaya", sub_header_style)
        ws1.write(row, col + 12, "G P Consultancy Revenue", sub_header_style)
        ws1.write(row, col + 13, "Lab Test Revenue", sub_header_style)
        ws1.write(row, col + 14, "Karkkidaka Kit Sale", sub_header_style)
        ws1.write(row, col + 15, "CGST@6%", sub_header_style)
        ws1.write(row, col + 16, "SGST@6%", sub_header_style)

        ws1.write(row, col + 17, "KFC", sub_header_style)
        ws1.write(row, col + 18, "Registration Fee @18%", sub_header_style)
        ws1.write(row, col + 19, "CGST @ 9%", sub_header_style)
        ws1.write(row, col + 20, "SGST @ 9%", sub_header_style)
        ws1.write(row, col + 21, "KFC", sub_header_style)
        ws1.write(row, col + 22, "Round Off", sub_header_style)
        ws1.write(row, col + 23, "Gross Total", sub_header_style)

        row += 1


        for line in self.category_gst_report():
            ws1.write(row, col + 1, line['invoice_date'], line_content_style)
            ws1.write(row, col + 2, line['transaction_type'], line_content_style)
            ws1.write(row, col + 3, line['partner_name'], line_content_style)
            ws1.write(row, col + 4, line['journal_name'], line_content_style)
            ws1.write(row, col + 5, line['invoice_number'], line_content_style)

            ws1.write(row, col + 6, line['retention_fee'], line_content_style)
            ws1.write(row, col + 7, line['revenue_from_physiotherapy'], line_content_style)
            ws1.write(row, col + 8, line['revenue_from_yoga'], line_content_style)
            ws1.write(row, col + 9, line['ayurvedic_treatment'], line_content_style)
            ws1.write(row, col + 10, line['beauty_treatment'], line_content_style)
            ws1.write(row, col + 11, line['medicine_sale_ayurlaya'], line_content_style)
            ws1.write(row, col + 12, line['gp_consultancy_revenue'], line_content_style)
            ws1.write(row, col + 13, line['lab_test_revenue'], line_content_style)
            ws1.write(row, col + 14, line['karkkidaka_kit_sale'], line_content_style)
            ws1.write(row, col + 15, line['cgst_tax'], line_content_style)
            ws1.write(row, col + 16, line['sgst_tax'], line_content_style)
            ws1.write(row, col + 17, line['kfc_tax'], line_content_style)
            ws1.write(row, col + 18, line['registration_fee'], line_content_style)
            ws1.write(row, col + 19, line['reg_cgst_tax'], line_content_style)
            ws1.write(row, col + 20, line['reg_sgst_tax'], line_content_style)
            ws1.write(row, col + 21, line['reg_kfc_tax'], line_content_style)


            ws1.write(row, col + 22, line['round_off'], line_content_style)
            ws1.write(row, col + 23, line['amount_total'], line_content_style)

            row += 1



    def format_date(self, date_in):
        return datetime.strftime(datetime.strptime(str(date_in), DEFAULT_SERVER_DATE_FORMAT), "%d/%m/%Y")