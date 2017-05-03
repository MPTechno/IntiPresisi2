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
                content += str(product.default_code or '') + '	' + str(product.name) + '\n'
            filename = 'Products.txt'
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
