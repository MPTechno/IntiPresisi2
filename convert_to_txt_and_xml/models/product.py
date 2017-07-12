# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
import odoo.addons.decimal_precision as dp

import base64
import StringIO
import xlsxwriter
import csv
import os.path

class ProductProduct(models.Model):
    _inherit = 'product.product'
    def download_txt(self):
        product_ids = self._context.get('active_ids',[])
        if product_ids:
            content = ''
            for product in self.env['product.product'].browse(product_ids):
                content += str(product.part_number or '') + '	' + str(product.name) + '   ' + str(product.part_type_id and product.part_type_id.name or '') + '   ' +\
                str(product.uom_id and product.uom_id.name or '') + '   ' + str(product.alternative_uom_id and product.alternative_uom_id.name or '') + '   '+ \
                str(product.part_code or '') + '   ' + str(product.product_group or '') + '    ' + \
                str(product.drawing_no or '') + '   ' + str(product.revision or '') + '    ' + \
                str(product.add_name_1 or '') + '   ' + str(product.add_name_2 or '') + '   ' + \
                str(product.add_name_3 or '') + '   ' + str(product.add_name_4 or '') + '   ' + \
                str(product.customer_code or '') + '   ' + str(product.lst_price or '') + '   ' + \
                str(product.customer_part_no or '') + '   ' + '\n'
            filename = '/opt/odoo/Products.txt'
            f = open(filename, 'w')
            f.write(content)
            f.close()
            file_base64 = ''
            with open(filename, "r") as file:
                file_base64 = base64.b64encode(file.read())
            export_id = self.env['product.txt.file'].create({
                                                    'txt_file': file_base64,
                                                    'file_name': filename,
                                                    })
            return {
                    'view_mode': 'form,tree',
                    'res_id': export_id.id,
                    'res_model': 'product.txt.file',
                    'view_type': 'form',
                    'type': 'ir.actions.act_window',
                    'context': self._context,
                    'target': 'new',
                    }


    def download_excel(self):
        product_ids = self._context.get('active_ids',[])
        if product_ids:
            res = self
            output =  StringIO.StringIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            row = 0
            col = 0
            bold_format = workbook.add_format({'bold':  1})
            right_format = workbook.add_format({'bold':1,'align':'right'})
            merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter'})
            
            worksheet.write(row, col,  unicode('Part Number', "utf-8"), bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            worksheet.write(row, col, unicode('Name', "utf-8"), bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            worksheet.write(row, col,unicode('Part Type', "utf-8") , bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            worksheet.write(row, col, unicode('Unit', "utf-8"), bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            worksheet.write(row, col, unicode('Alternate Unit', "utf-8"), bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            worksheet.write(row, col, unicode('Part Code', "utf-8"), bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            worksheet.write(row, col, unicode('Product Group', "utf-8"), bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            worksheet.write(row, col, unicode('Product Category', "utf-8"), bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            worksheet.write(row, col, unicode('Drawing Number', "utf-8"), bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            worksheet.write(row, col, unicode('Revision', "utf-8"), bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            worksheet.write(row, col, unicode('Add Name 1', "utf-8"), bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            worksheet.write(row, col, unicode('Add Name 2', "utf-8"), bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            worksheet.write(row, col, unicode('Add Name 3', "utf-8"), bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            worksheet.write(row, col, unicode('Add Name 4', "utf-8"), bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            worksheet.write(row, col, unicode('Customer Code', "utf-8"), bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            worksheet.write(row, col, unicode('Customer Price', "utf-8"), bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            worksheet.write(row, col, unicode('Customer Part No', "utf-8"), bold_format)
            worksheet.set_column(row, col, 20)
            col += 1

            row += 1
            for product in product_ids:
                product_obj = self.env['product.product'].browse(product)
                row += 1
                col = 0

                worksheet.write(row, col,unicode((product_obj.part_number or '').encode("utf-8"), "utf-8"))
                col += 1
                
                worksheet.write(row, col,unicode((product_obj.name or '').encode("utf-8"), "utf-8"))
                col += 1

                worksheet.write(row, col,unicode((product_obj.part_type_id.name or '').encode("utf-8"), "utf-8"))
                col += 1

                worksheet.write(row, col,unicode((product_obj.uom_id.name or '').encode("utf-8"), "utf-8"))
                col += 1

                worksheet.write(row, col,unicode((product_obj.alternative_uom_id.name or '').encode("utf-8"), "utf-8"))
                col += 1

                worksheet.write(row, col,unicode((product_obj.part_code.name or '').encode("utf-8"), "utf-8"))
                col += 1

                worksheet.write(row, col,unicode((product_obj.product_group.name or '').encode("utf-8"), "utf-8"))
                col += 1

                worksheet.write(row, col,unicode((product_obj.categ_id.name or '').encode("utf-8"), "utf-8"))
                col += 1
                
                worksheet.write(row, col,unicode((product_obj.drawing_no or '').encode("utf-8"), "utf-8"))
                col += 1

                worksheet.write(row, col,unicode((product_obj.revision or '').encode("utf-8"), "utf-8"))
                col += 1

                worksheet.write(row, col,unicode((product_obj.add_name_1 or '').encode("utf-8"), "utf-8"))
                col += 1

                worksheet.write(row, col,unicode((product_obj.add_name_2 or '').encode("utf-8"), "utf-8"))
                col += 1

                worksheet.write(row, col,unicode((product_obj.add_name_3 or '').encode("utf-8"), "utf-8"))
                col += 1

                worksheet.write(row, col,unicode((product_obj.add_name_4 or '').encode("utf-8"), "utf-8"))
                col += 1

                worksheet.write(row, col,unicode((product_obj.customer_code.name or '').encode("utf-8"), "utf-8"))
                col += 1

                worksheet.write(row, col,unicode((product_obj.lst_price or '').encode("utf-8"), "utf-8"))
                col += 1

                worksheet.write(row, col,unicode((product_obj.customer_part_no or '').encode("utf-8"), "utf-8"))
                col += 1

            row += 2
            row += 1

            workbook.close()
            output.seek(0)
            result = base64.b64encode(output.read())
            attachment_obj = self.env['ir.attachment']
            attachment_id = attachment_obj.create({'name': 'Product Excel.xlsx', 'datas_fname': 'Product Excel.xlsx', 'datas': result})
            download_url = '/web/content/' + str(attachment_id.id) + '?download=true'
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')

            return {
                "type": "ir.actions.act_url",
                "url": str(base_url) + str(download_url),
                "target": "self",
            }