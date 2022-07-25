# -*- coding: utf-8 -*-
import base64
import xlsxwriter

from cStringIO import StringIO
from odoo import api, fields, models


class InvoiceReport(models.TransientModel):
    _name = "invoice.report"
    _description = "Account Invoice Report"

    invoice_ids = fields.Many2many(
        'account.invoice',
        string='Invoice',
        required=True
    )

    def account_invoice_print(self):
        attch_obj = self.env['ir.attachment']
        fp = StringIO()
        workbook = xlsxwriter.Workbook(fp)
        sheet = workbook.add_worksheet('Report')

        tbl_head_fmt = workbook.add_format()
        tbl_head_fmt.set_bold()
        tbl_head_fmt.set_font_size(10)
        tbl_head_fmt.set_font_name('Calibri')
        tbl_head_fmt.set_font_color('white')
        tbl_head_fmt.set_bg_color('#6a6a77')
        tbl_head_fmt.set_align('center')

        head_fmt = workbook.add_format({
            'border': 1,
            'font_name': 'Calibri',
            'align': 'center',
            'font_size': 10,
            'bold': True
        })

        float_fmt = workbook.add_format({
        	'font_size': 10,
            'align': 'center',
		    'num_format': '#,##0.00'
        })

        # Set Headers
        sheet.write(0, 0, '#', tbl_head_fmt)
        sheet.write(0, 1, 'Customer', tbl_head_fmt)
        sheet.write(0, 2, 'Invoice Date', tbl_head_fmt)
        sheet.write(0, 3, 'Number', tbl_head_fmt)
        sheet.write(0, 4, 'Sales Person', tbl_head_fmt)
        sheet.write(0, 5, 'Due Date', tbl_head_fmt)
        sheet.write(0, 6, 'Total', tbl_head_fmt)
        sheet.write(0, 7, 'Status', tbl_head_fmt)

        # Set Column width
        sheet.set_column(1, 0, 3)
        for i in range(0, 11):
            sheet.set_column(1, i, 12)

        # Freeze Row
        sheet.freeze_panes(1, 0)

        # Set Table data format
        tbl_data_fmt = workbook.add_format(
        	{
        	'font_color': '#000000',
        	'font_name': 'Calibri',
        	'align': 'left',
        	'font_size': 9
        	})

        # Text Wrap
        add_data_fmt = tbl_data_fmt
        add_data_fmt.set_text_wrap()

        # Building rows
        row = 1
        for invoice_id in self.invoice_ids:
        	sheet.write(row, 0, row)
        	sheet.write(row, 1, invoice_id.partner_id.name or '')
        	sheet.write(row, 2, invoice_id.date_invoice)
        	sheet.write(row, 3, invoice_id.number)
        	sheet.write(row, 4, invoice_id.user_id.name)
        	sheet.write(row, 5, invoice_id.date_due)
        	sheet.write(row, 6, invoice_id.amount_total)
        	sheet.write(row, 7, invoice_id.state)
        	row += 1

        workbook.close()
        data = base64.b64encode(fp.getvalue())
        fp.close()
        attach_ids = attch_obj.search([
            ('res_model', '=', 'invoice.report')])
        if attach_ids:
            try:
                attach_ids.unlink()
            except:
                pass

        # Creating Attachment
        doc_id = attch_obj.create({
            'name': '%s.xlsx' % ('Invoice Report'),
                    'datas': data,
                    'res_model': 'invoice.report',
                    'datas_fname': '%s.xlsx' % ('Invoice Report'),
        })

        # Downloading the file
        return {
            'type': 'ir.actions.act_url',
            'url': 'web/content/%s?download=true' % (doc_id.id),
            'target': 'current',
        }
