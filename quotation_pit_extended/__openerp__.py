# -*- coding: utf-8 -*-
{
    'name': "Quotation Lead Extended",

    'summary': """
        Allowing users to generate quotation for a opportunity
        """,

    'description': """
        1. Users can generate quotations and sales orders to an opportunity
        2. There will be a button on the top right of each opportunity to view all the quotations related to him
        3. Instead of "Convert to Quotation", have "Create Quotation" on all opportunity regardless of the kanban status.
        4. Add one button "Convert to Customer" in all Opportunity, which will update the Opportunity status to "Won", and customer record is created
    """,

    'author': "HashMicro / Parikshit Vaghasiya",
    'website': "http://www.hashmicro.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'HashMicro',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'crm',
        'sale_crm',
    ],

    # always loaded
    'data': [
        'data/crm_stage_data_v.xml',
        'wizard/lead_ask_code_view.xml',
        'views/pit_crm_view.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}