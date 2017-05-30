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
                content += customer.partner_code + '	' +customer.name + '	'+ str(customer.mailing_address_name or '') +'    '+\
                str(customer.street or '')+ '	'+str(customer.street2 or '')+ '    '+str(customer.city or '') + '	'+(customer.city2_mailing or '') + '  '+\
                str(customer.delivery_address_name or '')+ ' '+ (customer.street_delivery or '')+ '  '+(customer.street2_delivery or '')+ '  '+\
                str(customer.zip_delivery or '')+ ' '+ (customer.zip2_delivery or '')+ '  '+str(customer.lang or '')+ '  '+\
                str(customer.currency_new_id and customer.currency_new_id.name or '')+ '	'+str(customer.customer_group_id and customer.customer_group_id.name or '')+ '  ' +\
                str(customer.vat_code or '')+ '   ' +str(customer.vat_number or '')+ '   ' + str(customer.country_id and customer.country_id.code or '') + '    ' + \
                (customer.phone or '')+ '   ' +(customer.fax or '') + '   ' +(customer.email or '')+ '   ' +\
                (customer.ref_name or '')+ '   ' +(customer.ref_phone or '') + '   ' +(customer.ref_mobile or '')+ '   ' +(customer.ref_email or '')+'\n' 
            filename = '/opt/odoo/Customers.txt'
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
