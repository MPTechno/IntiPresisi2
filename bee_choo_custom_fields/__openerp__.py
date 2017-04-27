# -*- coding: utf-8 -*-
{
    'name': "Custom Fields for Bee Choo",

    'summary': """
            Custom fields added in Product template.
            """,

    'description': """
        1. HS Code, Country of Origin and Notification Number added in Product Template.
        2. Custom Invoice Layout
        3. Custom Purchase Order Layout
        4. Custom Purchase Quotation Layout
        5. Custom Delivery Order Layout
        6. Custom Packing Slip Layout
        7. Custom Picking Layout
        8. Custom Partner Ledger Layout
    """,

    'author': "HashMicro / Vinay & Hoang",
    'website': "http://www.hashmicro.com",

    'category': 'HashMicro',
    'version': '0.1',

    'depends': ['base', 'product', 'sale', 'account'],

    'data': [
        # 'security/ir.model.access.csv',
        # 'data/sequence.xml',
        'templates.xml',
        'report/report_invoice.xml',
        'report/report_layout.xml',
        'report/report_purchase_order.xml',
        'report/report_purchase_quotation.xml',
        'report/report_picking.xml',
        'report/report_packing_slip.xml',
        'report/report_sale_order.xml',
        'report/report_overdue_document.xml',
        'report/report_partner_ledger.xml',
        'data/data.xml'
    ],
    
}