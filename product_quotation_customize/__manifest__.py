# -*- coding: utf-8 -*-

{
    'name': 'Product-Quotation Customization',
    'version': '1.0',
    'summary': 'Product-Quotation Customization',
    'description': """
        Product-Quotation Customization
    """,
    'author': 'HashMicro / Amit Patel',
    'website': 'www.hashmicro.com',
    'category': 'Sale',
    'sequence': 0,
    'images': [],
    'depends': ['base','product','sale'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/sale_view.xml',
        'views/report_menu.xml',
        'views/quotation_report_view.xml',
    ],
    'installable': True,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: