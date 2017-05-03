# -*- coding: utf-8 -*-

from odoo import fields, models
import base64
from xml.etree import ElementTree
from xml.etree.ElementTree import Element,SubElement
from xml.dom import minidom

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def download_xml(self):
        order_ids = self._context.get('active_ids',[])
        if order_ids:
            Orders = Element('Orders')#Top Element
            for order in self.env['sale.order'].browse(order_ids):
                Order = SubElement(Orders,'Order')
                Order.set('OrderNumber',str(order.name))
                
                head = SubElement(Order,'head')#Header Part
                
                supplier = SubElement(head, 'Supplier')#Supplier (Company Address)
                supplier.set('SupplierCodeEdi','123')#FixMe
                supplier_name = SubElement(supplier, 'Name')
                supplier_name.text = str(order.user_id.company_id.name)
                
                StreetBox1 = SubElement(supplier, 'StreetBox1')
                if order.user_id.company_id.street:
                    StreetBox1.text = str(order.user_id.company_id.street)
                    
                StreetBox2 = SubElement(supplier, 'StreetBox2')
                if order.user_id.company_id.street2:
                    StreetBox2.text = str(order.user_id.company_id.street2)
                    
                ZipCity1 = SubElement(supplier, 'ZipCity1')
                if order.user_id.company_id.city:
                    ZipCity1.text = str(order.user_id.company_id.city) +' ' + str(order.user_id.company_id.state_id.name or '')
                    
                ZipCity2 = SubElement(supplier, 'ZipCity2')
                if order.user_id.company_id.zip:
                    ZipCity2.text = str(order.user_id.company_id.zip)
                    
                Country = SubElement(supplier, 'Country')
                if order.user_id.company_id.country_id:
                    Country.text = str(order.user_id.company_id.country_id.name)
                    
                Buyer = SubElement(head, 'Buyer')#Customer Address
                Buyer_name = SubElement(Buyer, 'Name')
                Buyer_name.text = str(order.partner_id.name)
                
                StreetBox1 = SubElement(Buyer, 'StreetBox1')
                if order.partner_id.street:
                    StreetBox1.text = str(order.partner_id.street)
                    
                StreetBox2 = SubElement(Buyer, 'StreetBox2')
                if order.user_id.company_id.street2:
                    StreetBox2.text = str(order.partner_id.street2)
                    
                ZipCity1 = SubElement(Buyer, 'ZipCity1')
                if order.user_id.company_id.city:
                    ZipCity1.text = str(order.partner_id.city) +' ' + str(order.partner_id.state_id.name or '')
                    
                ZipCity2 = SubElement(Buyer, 'ZipCity2')
                if order.partner_id.zip:
                    ZipCity2.text = str(order.partner_id.zip)
                    
                Country = SubElement(Buyer, 'Country')
                if order.partner_id.country_id:
                    Country.text = str(order.partner_id.country_id.name)
                    
                References = SubElement(head, 'References')#References    
                BuyerReference = SubElement(References, 'BuyerReference')
                BuyerReference.text = ''#FixMe
                
                BuyerComment = SubElement(References, 'BuyerComment')
                BuyerComment.text = ''#FixMe
                
                GoodsLabeling = SubElement(References, 'GoodsLabeling')#FixMe
                
                DeliveryAddress = SubElement(head, 'DeliveryAddress')#Delivery Address #FixMe: Need to confirm which value?
                DeliveryAddress_name = SubElement(DeliveryAddress, 'Name')
                DeliveryAddress_name.text = str(order.partner_shipping_id.name)
                
                StreetBox1 = SubElement(DeliveryAddress, 'StreetBox1')
                if order.partner_shipping_id.street:
                    StreetBox1.text = str(order.partner_shipping_id.street)
                    
                StreetBox2 = SubElement(DeliveryAddress, 'StreetBox2')
                if order.user_id.company_id.street2:
                    StreetBox2.text = str(order.partner_shipping_id.street2)
                    
                ZipCity1 = SubElement(DeliveryAddress, 'ZipCity1')
                if order.user_id.company_id.city:
                    ZipCity1.text = str(order.partner_shipping_id.city) +' ' + str(order.partner_shipping_id.state_id.name or '')
                    
                ZipCity2 = SubElement(DeliveryAddress, 'ZipCity2')
                if order.partner_shipping_id.zip:
                    ZipCity2.text = str(order.partner_shipping_id.zip)
                    
                Country = SubElement(DeliveryAddress, 'Country')
                if order.partner_shipping_id.country_id:
                    Country.text = str(order.partner_shipping_id.country_id.name)
                CompanyAdressFlag = SubElement(DeliveryAddress, 'CompanyAdressFlag')#FixMe
                
                Terms = SubElement(head, 'Terms')#Terms
                DeliveryTerms = SubElement(Terms, 'DeliveryTerms')
                IncoTermCombiTerm = SubElement(DeliveryTerms, 'IncoTermCombiTerm')
                if order.incoterm:
                    IncoTermCombiTerm.text = str(order.incoterm.name)
                DeliveryMethod = SubElement(DeliveryTerms, 'DeliveryMethod')
                TransportPayer = SubElement(DeliveryTerms, 'TransportPayer')
                CustomerTransportTimeDays = SubElement(DeliveryTerms, 'CustomerTransportTimeDays')
                CustomerInvoiceCode = SubElement(Terms, 'CustomerInvoiceCode')
                OrderDate = SubElement(Terms, 'OrderDate')
                if order.date_order:
                    OrderDate.text = str(order.date_order).split(' ')[0]
                    
                PaymentTerms = SubElement(Terms, 'PaymentTerms')
                
                TermsOfPaymentDays = SubElement(PaymentTerms, 'TermsOfPaymentDays')
                if order.payment_term_id:
                    TermsOfPaymentDays.text = str(order.payment_term_id.name)
                    
                Export = SubElement(head, 'Export')#Export
                Currency = SubElement(Export, 'Currency')
                if order.pricelist_id.currency_id:
                    Currency.text = str(order.pricelist_id.currency_id.name)
                Rows = SubElement(Order,'Rows')#Line Items
                line_no = 1
                for line in order.order_line:
                    Row = SubElement(Rows,'Row')
                    Row.set('RowNumber',str(line_no))
                    line_no+=1
                    Row.set('RowType','')#FixMe
                    
                    Part = SubElement(Row,'Part')
                    if line.product_id and line.product_id.part_number:
                        Part.set('PartNumber',str(line.product_id.part_number))
                    else:
                        Part.set('PartNumber','')
                    if line.product_id and line.product_id.customer_part_no:
                        Part.set('SupplierPartNumber',str(line.product_id.customer_part_no))
                    else:
                        Part.set('SupplierPartNumber','')
                    
                    Text = SubElement(Row,'Text')
                    Text.text = str(line.name or line.product_id.name)
                    
                    ReferenceNumber = SubElement(Row,'ReferenceNumber')
                    if line.product_id.default_code:
                        ReferenceNumber.text = str(line.product_id.default_code)
                    
                    Quantity = SubElement(Row,'Quantity')
                    Quantity.text = str(line.product_uom_qty)
                    
                    Unit = SubElement(Row,'Unit')
                    Unit.text = str(line.product_uom.name)
                    
                    DeliveryPeriod = SubElement(Row,'DeliveryPeriod')
                    DeliveryPeriod.text = ''#FixMe
                    
                    Each = SubElement(Row,'Each')
                    Each.text = ''#FixMe
                    
                    Discount = SubElement(Row,'Discount')
                    Discount.text = ''#FixMe
                    
                    Setup = SubElement(Row,'Setup')
                    Setup.text = ''#FixMe
                    
                    Alloy = SubElement(Row,'Alloy')
                    Alloy.text = ''#FixMe
                    
            filename = 'Sale Order XML.xml'
            f = open(filename, 'w')
            data = minidom.parseString(ElementTree.tostring(Orders)).toprettyxml()
            f.write(data)
            f.close()
            file_base64 = ''
            with open(filename, "r") as file:
                file_base64 = base64.b64encode(file.read())
            export_id = self.env['so.xml.file'].create({
                                                    'xml_file': file_base64,
                                                    'file_name': filename,
                                                    })
            return {
                    'view_mode': 'form',
                    'res_id': export_id.id,
                    'res_model': 'so.xml.file',
                    'view_type': 'form',
                    'type': 'ir.actions.act_window',
                    'context': self._context,
                    'target': 'new',
                    }

