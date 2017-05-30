# -*- coding: utf-8 -*-
from odoo import api, fields, models
import base64

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
