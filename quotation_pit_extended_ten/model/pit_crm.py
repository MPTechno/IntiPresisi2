# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
import odoo.addons.decimal_precision as dp

class prospect_source(models.Model):
    _name='prospect.source'
    
    name = fields.Char('Prospect Source Name')
    # prospect_source_ids = fields.One2many('crm.lead','prospect_source','Lead')

class industry_source(models.Model):
    _name = 'industry.source'
    
    name = fields.Char('Industry Name')
    # indus_ids = fields.One2many('crm.lead','industry_source_id','Lead')

class qty_machine(models.Model):
    _name = 'qty.machine'
    
    name = fields.Char('Name')
    # q_machine_ids = fields.One2many('crm.lead','quantity_of_machine','Lead')

class prospect_production(models.Model):
    _name = 'prospect.production'
    
    name = fields.Char('Name')
    # prospect_production_ids = fields.One2many('crm.lead','prospect_production','Lead')

class customer_group(models.Model):
    _name = 'customer.group'
    
    name = fields.Char('Name')
    # customer_group_ids = fields.One2many('res.partner','customer_group_id','Lead')

class enquiry_status(models.Model):
    _name = 'enquiry.status'
    
    name = fields.Char('Name')
    # en_status_ids = fields.One2many('crm.lead','en_status','status')

class workpiece_material(models.Model):
    _name = 'workpiece.material'
    
    name = fields.Char('Name')
    # workpiece_ids = fields.One2many('crm.lead','workpiece_material','Workpiece Material')

class coating_enquiry(models.Model):
    _name = 'coating.enquiry'
    
    name = fields.Char('Name')
    # coating_en_ids = fields.One2many('crm.lead','coating_en','Coating')

class attachment_type_en(models.Model):
    _name = 'attachment.type.en'
    
    name = fields.Char('Name')
    # attachment_type_en_ids = fields.One2many('crm.lead','attachment_type_id','Type')

class crm_new_case(models.Model):
    _name = 'crm.new.case'
    
    name = fields.Char('Name')

class crm_lead(models.Model):
    _inherit = 'crm.lead'

    
    partner_name = fields.Char('Account Name',required=True)
    stage_new_pr = fields.Many2one('crm.new.case','Prospects Status')
    prospect_quality = fields.Selection([('a','A'),('b','B'),('c','C'),('d','D'),('e','E')], 'Prospect Quality')
    website = fields.Char('Website')
    comp_name = fields.Char('Company')
    planned_revenue = fields.Float('Expected Revenue (Amount)', track_visibility='always')

    # Additional Information
    no_of_employee = fields.Integer('No of Employee')
    annual_revenue = fields.Integer('Annual Revenue')
    prospect_source = fields.Many2one('prospect.source','Prospect Source')
    industry_source_id = fields.Many2one('industry.source','Industry')

    # Prospect Scoring:
    special_carbide_tools = fields.Boolean('Special Carbide Tools')
    qty_per_month = fields.Integer('Quantity Per Month')
    quantity_of_machine = fields.Many2one('qty.machine','Quantity of Machine')
    prospect_production = fields.Many2one('prospect.production','Production')
    special_carbide_tools_score = fields.Integer('Special Carbide Tools Score')
    quantity_per_month_score = fields.Integer('Quantity Per Month Score')
    quantity_of_machine_score = fields.Integer('Quantity of Machine Score')
    production_score = fields.Integer('Production Score')
    total_score = fields.Integer('Total Score')

    # Description Information:
    description_prospect = fields.Text('Description')

    # System Information:
    created_by = fields.Char('Created By')
    last_modified_by = fields.Char('Last Modified By')


    # OPPORTUNITY FIELDS
    en_number = fields.Char('Enquiry Number')
    enquiry_type = fields.Selection([('new_business','New Business'),('existing_business','Existing Business')], 'Enquiry Type')
    # close_date = fields.Date('Close Date')
    stage = fields.Char('Stage')
    en_status = fields.Many2one('enquiry.status','Enquiry Status')
    en_stages = fields.Many2one('crm.stage', string='Enquiry Stage', track_visibility='onchange', index=True,
        domain="['|', ('team_id', '=', False), ('team_id', '=', team_id)]",
        group_expand='_read_group_stage_ids', default=lambda self: self._default_stage_id())

          # ADDITIONAL INFO
    prospects_source_id = fields.Many2one('crm.lead', 'Prospect Source',domain="[('type', '=', 'lead')]")
    next_step = fields.Char('Next Step')
    reason_enquiry = fields.Char('Reason')

        # NEGOTITION INFORMATION 

    nagotiation_note = fields.Text('Negotiation n Notes')

        # DESCRIPTION INFORMATION

    description_te = fields.Text('Description')

        # SYSTEM INFORMATION
    created_by_en = fields.Char('Created By')
    last_modified_by_en = fields.Char('Last Modified By')

        # Attachments

    attachment_type_id = fields.Many2one('attachment.type.en','Type')
    title_attach = fields.Char('Title')
    last_modified_attach = fields.Date('Last Modified')
    created_by_attch = fields.Date('Created By')

    lead_line_ids = fields.One2many('crm.lead.line','lead_line_id',string='CRM Lead Line')



    @api.multi
    def write(self, vals):
        # stage change: update date_last_stage_update
        if 'en_stages' in vals:
            vals['stage_id'] = vals.get('en_stages')
        if self.stage_id:
            stage = self.stage_id
            res_group = self.env['res.groups'].search([('name','=','Sales Person')])
            technical_res = self.env['res.groups'].search([('name','=','Technical Support')])
            technical_users = []
            if technical_res:
                for i in technical_res.users:
                    technical_users.append(i.partner_id.id)
            for use_group in res_group:
                for use_id in res_group.users:
                    if self.env.user.id == use_id.id:
                        if 'stage_id' in vals:
                            stagee = self.env['crm.stage'].browse(vals.get('stage_id'))
                            if stagee.name == 'Technical Drawing':
                                recipient_links = [(4, technical_users)]
                                message_data = {
                                    'type': 'notification',
                                    'subject': "Enquiry is in Technical Drawing Stage.",
                                    'body': self.name ,
                                    'partner_ids': recipient_links,
                                }
                                msg_obj = self.env['mail.message']
                                msg_obj.create(message_data)
            # for users_id in technical_res.users:
            #     if self.env.user.id == users_id.id:
            #         print ">>aiyaa kemmm..............",users_id.id , self._uid,self.env.user
            #         if stage.name not in ['Technical Drawing']:
            #             raise UserError(_('You Can Only Edit This Record If It is not in Technical Drawing Stage. Please Contact Your Administrator.'))
            #         if 'stage_id' in vals:
            #             stagee = self.env['crm.stage'].browse(vals.get('stage_id'))
            #             if stagee.name not in ['No Offer','Pricing','Collect Data']:
            #                 raise UserError(_('You Have Not Rights To Move This Record in This Stage. Please Contact Your Administrator.'))
        return super(crm_lead, self).write(vals)

    @api.model
    def create(self, vals):
        if 'type' in vals:
            if vals['type'] == 'opportunity':
                vals['en_number'] = self.env['ir.sequence'].get('crm.lead')
        return super(crm_lead, self).create(vals)

    @api.model
    def _onchange_stage_id_values(self, stage_id):
        """ returns the new values when stage_id has changed """
        vals = {}
        if not stage_id:
            return {}
        stage = self.env['crm.stage'].browse(stage_id)
        if stage.on_change:
            return {'probability': stage.probability}
        if stage.id != self.en_stages.id:
            vals['en_stages'] = stage.id
        return {'value': vals}


class crm_lead_line(models.Model):
    _name='crm.lead.line'
    _order = 'lead_line_id'

    @api.depends('qty_en', 'discount', 'unit_price_en', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.unit_price_en * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.currency_id, line.qty_en, product=line.product_en, partner=line.lead_line_id.partner_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'total_price_en': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

        # PRODUCT PRICELISTINGt
    lead_line_id = fields.Many2one('crm.lead',string='Listing Line',index=True)
    product_en = fields.Many2one('product.product','Product')
    qty_en = fields.Integer('Quantity')
    unit_price_en = fields.Float('Unit Price')
    total_price_en = fields.Float('Total Price')
    part_number = fields.Char('Part Number')
    tax_id = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)])
    internal_code_en = fields.Char('Internal Code')
    workpiece_material = fields.Many2one('workpiece.material','Workpiece Material')
    coating_en = fields.Many2one('coating.enquiry','Coating')
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', required=True)
    pricing_date = fields.Date('Pricing Date')
    remarks_en = fields.Text('Remarks')
    currency_id = fields.Many2one(related='lead_line_id.partner_id.property_product_pricelist.currency_id', store=True, string='Currency', readonly=True)
    discount = fields.Float(string='Discount (%)', digits=dp.get_precision('Discount'), default=0.0)
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    price_tax = fields.Monetary(compute='_compute_amount', string='Taxes', readonly=True, store=True)
    total_price_en = fields.Monetary(compute='_compute_amount', string='Total', readonly=True, store=True)

    @api.multi
    def _get_display_price(self, product):
        if self.lead_line_id.partner_id.property_product_pricelist.discount_policy == 'without_discount':
            from_currency = self.currency_id
            return from_currency.compute(product.lst_price, self.currency_id)
        return product.with_context(pricelist=self.currency_id.id).price


    @api.multi
    @api.onchange('product_en')
    def product_id_change(self):
        vals = {}
        
        if not self.product_en:
            return {'domain': {'product_uom': []}}

        vals = {}
        domain = {'product_uom': [('category_id', '=', self.product_en.uom_id.category_id.id)]}
        if not self.product_uom or (self.product_en.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_en.uom_id

        product = self.product_en.with_context(
            lang=self.lead_line_id.partner_id.lang,
            partner=self.lead_line_id.partner_id.id,
            pricelist=self.lead_line_id.partner_id.property_product_pricelist.id,
            quantity=vals.get('qty_en') or self.qty_en,
        )
        vals['qty_en'] = 1.0
        name =''
        if product.description_sale:
            name += '\n' + product.description_sale
        vals['remarks_en'] = name
        if product:
            vals['unit_price_en'] = self.env['account.tax']._fix_tax_included_price(self._get_display_price(product), product.taxes_id, self.tax_id)
        self.update(vals)

class res_partner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _get_euro(self):
        return self.env['res.currency.rate'].search([('rate', '=', 1)], limit=1).currency_id

    @api.model
    def _get_user_currency(self):
        currency_id = self.env['res.users'].browse(self._uid).company_id.currency_id
        return currency_id or self._get_euro()

    email_count = fields.Integer("Emails", compute='_compute_emails_count')
    partner_code = fields.Char('Code',required=True)
    street_delivery =  fields.Char('Street')
    street2_delivery =  fields.Char('Street2')
    zip_delivery =  fields.Char('Zip', size=24, change_default=True)
    city_delivery =  fields.Char('City')
    state_id_delivery =  fields.Many2one("res.country.state", 'State', ondelete='restrict')
    country_id_delivery =  fields.Many2one('res.country', 'Country', ondelete='restrict')
    mailing_address_name = fields.Char('Mailing Address')
    delivery_address_name = fields.Char('Delivery Address')
    city2_mailing =  fields.Char('City')
    city2_delivery =  fields.Char('City')
    zip2_mailing =  fields.Char('Zip')
    zip2_delivery =  fields.Char('Zip')
    currency_new_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self._get_user_currency())
    customer_group_id = fields.Many2one('customer.group','Customer Group')
    vat_code = fields.Char('Vat Code')
    vat_number = fields.Char('Vat Number')
    country_code = fields.Char('Country Code')
    state_id2 = fields.Many2one("res.country.state", 'State', ondelete='restrict')
    state_id2_delivery = fields.Many2one("res.country.state", 'State', ondelete='restrict')
        # REFERENCE DETAILS
    ref_name = fields.Char('Name')
    ref_phone = fields.Char('Phone')
    ref_mobile = fields.Char('Mobile')
    ref_email = fields.Char('Email')

    @api.multi
    def onchange_state_delivery(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id_delivery': state.country_id.id}}
        return {}

    @api.multi
    def _compute_emails_count(self):
        for partner in self:
            partner.email_count = self.env['mail.mail'].search_count([('recipient_ids','in', [partner.id])])


class product_pricelist(models.Model):
    _inherit = 'product.pricelist'

    @api.model
    def create(self, vals):
        vals['name'] = vals['name'] + self.env['ir.sequence'].get('product.pricelist')
        return super(product_pricelist, self).create(vals)

class sale_order(models.Model):
    _inherit= 'sale.order'

    @api.multi
    @api.onchange('opportunity_id')
    def onchange_opportunity_id(self):
        res = {'value':{}}
        order_lines = []
        if self.opportunity_id and self.opportunity_id.lead_line_ids:
            for op_line in self.opportunity_id.lead_line_ids:
                taxlist = []
                for itax in op_line.tax_id:
                    taxlist.append(itax.id)
                print ">>>>>>>>>>>>>>>>",taxlist
                line_dict = {
                    'product_id':op_line.product_en,
                    'product_uom_qty':op_line.qty_en,
                    'price_unit':op_line.unit_price_en,
                    'discount':op_line.discount,
                    'tax_id':[(6,0,taxlist)],
                    'product_uom':op_line.product_uom,
                    'currency_id':op_line.currency_id,
                }
                order_lines.append((0, 0, line_dict))
                self.order_line = order_lines
        # return res