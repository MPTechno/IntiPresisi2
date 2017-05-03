# -*- coding: utf-8 -*-

from odoo import fields, models
import base64

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    def download_txt(self):
        customer_ids = self._context.get('active_ids',[])
        if customer_ids:
            content = ''
            for customer in self.env['res.partner'].browse(customer_ids):
                content += customer.partner_code + '	' +customer.name + '	'+\
                (customer.street or '')+ '	'+(customer.city or '') + '	'+\
                (customer.state_id and customer.state_id.name or '')+ '	'+\
                (customer.zip or '')+ '	'+'\n' 
            filename = 'Customers.txt'
            f = open(filename, 'w')
            f.write(content)
            f.close()
            file_base64 = ''
            with open(filename, "r") as file:
                file_base64 = base64.b64encode(file.read())
            export_id = self.env['customer.txt.file'].create({
                                                    'txt_file': file_base64,
                                                    'file_name': filename,
                                                    })
            return {
                    'view_mode': 'form',
                    'res_id': export_id.id,
                    'res_model': 'customer.txt.file',
                    'view_type': 'form',
                    'type': 'ir.actions.act_window',
                    'context': self._context,
                    'target': 'new',
                    }    
