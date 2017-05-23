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

#!/usr/bin/python
# -*- coding: utf-8 -*-


def int_to_roman(input):
    """
   Convert an integer to Roman numerals.

   Examples:
   >>> int_to_roman(0)
   Traceback (most recent call last):
   ValueError: Argument must be between 1 and 3999

   >>> int_to_roman(-1)
   Traceback (most recent call last):
   ValueError: Argument must be between 1 and 3999

   >>> int_to_roman(1.5)
   Traceback (most recent call last):
   TypeError: expected integer, got <type 'float'>

   >>> for i in range(1, 21): print int_to_roman(i)
   ...
   I
   II
   III
   IV
   V
   VI
   VII
   VIII
   IX
   X
   XI
   XII
   XIII
   XIV
   XV
   XVI
   XVII
   XVIII
   XIX
   XX
   >>> print int_to_roman(2000)
   MM
   >>> print int_to_roman(1999)
   MCMXCIX
   """

    if type(input) != type(1):
        raise TypeError, 'expected integer, got %s' % type(input)
    if not 0 < input < 4000:
        raise ValueError, 'Argument must be between 1 and 3999'
    ints = (
        1000,
        900,
        500,
        400,
        100,
        90,
        50,
        40,
        10,
        9,
        5,
        4,
        1,
        )
    nums = (
        'M',
        'CM',
        'D',
        'CD',
        'C',
        'XC',
        'L',
        'XL',
        'X',
        'IX',
        'V',
        'IV',
        'I',
        )
    result = ''
    for i in range(len(ints)):
        count = int(input / ints[i])
        result += nums[i] * count
        input -= ints[i] * count
    return result


def roman_to_int(input):
    """
   Convert a roman numeral to an integer.
   
   >>> r = range(1, 4000)
   >>> nums = [int_to_roman(i) for i in r]
   >>> ints = [roman_to_int(n) for n in nums]
   >>> print r == ints
   1

   >>> roman_to_int('VVVIV')
   Traceback (most recent call last):
    ...
   ValueError: input is not a valid roman numeral: VVVIV
   >>> roman_to_int(1)
   Traceback (most recent call last):
    ...
   TypeError: expected string, got <type 'int'>
   >>> roman_to_int('a')
   Traceback (most recent call last):
    ...
   ValueError: input is not a valid roman numeral: A
   >>> roman_to_int('IL')
   Traceback (most recent call last):
    ...
   ValueError: input is not a valid roman numeral: IL
   """

    if type(input) != type(''):
        raise TypeError, 'expected string, got %s' % type(input)
    input = input.upper()
    nums = [
        'M',
        'D',
        'C',
        'L',
        'X',
        'V',
        'I',
        ]
    ints = [
        1000,
        500,
        100,
        50,
        10,
        5,
        1,
        ]
    places = []
    for c in input:
        if not c in nums:
            raise ValueError, 'input is not a valid roman numeral: %s' \
                % input
    for i in range(len(input)):
        c = input[i]
        value = ints[nums.index(c)]

      # If the next place holds a larger number, this value is negative.

        try:
            nextvalue = ints[nums.index(input[i + 1])]
            if nextvalue > value:
                value *= -1
        except IndexError:

         # there is no next place.

            pass
        places.append(value)
    sum = 0
    for n in places:
        sum += n

   # Easiest test for validity...

    if int_to_roman(sum) == input:
        return sum
    else:
        raise ValueError, 'input is not a valid roman numeral: %s' \
            % input

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

    email_count = fields.Integer("Emails", compute='_compute_emails_count')
    phonecall_count = fields.Integer(compute='_compute_phonecall_count',string="Phonecalls")
    partner_name = fields.Char('Account Name')
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
    created_by = fields.Many2one('res.users','Created By',default=lambda self: self.env.user)
    last_modified_by = fields.Datetime('Last Modified By')


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
    prospects_source_id = fields.Many2one('prospect.source', 'Prospect Source')
    next_step = fields.Char('Next Step')
    reason_enquiry = fields.Char('Reason')
    our_reference_ids = fields.Many2one('res.partner','Our Reference')

        # NEGOTITION INFORMATION 

    nagotiation_note = fields.Text('Negotiation n Notes')

        # DESCRIPTION INFORMATION

    description_te = fields.Text('Description')

        # SYSTEM INFORMATION
    created_by_en = fields.Many2one('res.users','Created By',default=lambda self: self.env.user)
    last_modified_by_en = fields.Datetime('Last Modified By')

        # Attachments
    attachment_en = fields.Binary('Attachment')
    attachment_type_id = fields.Many2one('attachment.type.en','Type')
    title_attach = fields.Char('Title')
    last_modified_attach = fields.Datetime('Last Modified')
    created_by_attch = fields.Many2one('res.users','Created By',default=lambda self: self.env.user)

    lead_line_ids = fields.One2many('crm.lead.line','lead_line_id',string='CRM Lead Line')

    @api.multi
    def _compute_phonecall_count(self):
        for partner in self:
            if partner.partner_id:
                partner.phonecall_count = self.env['crm.phonecall'].search_count([('partner_id', '=', partner.partner_id.id)])

    @api.multi
    def _compute_emails_count(self):
        for partner in self:
            if partner.partner_id:
                partner.email_count = self.env['mail.mail'].search_count([('recipient_ids','in', [partner.partner_id.id])])

    @api.multi
    def write(self, vals):
        # stage change: update date_last_stage_update
        if 'en_stages' in vals:
            vals['stage_id'] = vals.get('en_stages')
        if self.type == 'lead':
            vals['last_modified_by'] = fields.Datetime.now()
        else:
            vals['last_modified_by_en'] = fields.Datetime.now()
        if 'attachment_en' in vals:
            vals['created_by_attch'] = self._uid
            # vals['last_modified_attach'] = fields.Datetime.now()
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
        return super(crm_lead, self).write(vals)

    @api.model
    def create(self, vals):
        if 'type' in vals:
            if vals['type'] == 'opportunity':
                seq_num = self.env['ir.sequence'].get('crm.lead').split('-')
                vals['en_number'] =  '000' + str(seq_num[0]) + '/Enq-' + str(self.env['res.partner'].browse(vals.get('partner_id')).short_name or '') + '/IPT/' +str(int_to_roman(int(seq_num[1]))) + '/' + str(seq_num[2])
        vals['stage_id'] = vals.get('en_stages')
        return super(crm_lead, self).create(vals)

    @api.model
    def _onchange_stage_id_values(self, stage_id):
        """ returns the new values when stage_id has changed """
        vals = {}
        if not stage_id:
            return {}
        vals['en_stages'] = stage_id
        return vals

class sequence_number_partner(models.Model):
    _name = "sequence.number.partner"

    sequence_id = fields.Many2one('res.partner','Account')
    product_id = fields.Many2one('product.product','Product')
    sequence_number = fields.Integer('Sequence')
    seq_price = fields.Float('Price')
    name = fields.Char('Name')

# class part_number_line(models.Model):
#     _name = "part.number.line"

#     part_line_id = fields.Many2one('crm.lead.line','Line')
#     seq_price = fields.Float('Price')
#     name = fields.Char('Name')
#     product_id = fields.Many2one('product.product', 'Product')
#     partner_id = fields.Many2one('res.partner', 'Account')

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

    @api.model
    def _get_partner(self):
        partner = False
        context = self._context or {}
        if context.get('partner_id'):
            partner = context.get('partner_id')
        return partner

        # PRODUCT PRICELISTINGt
    
    lead_line_id = fields.Many2one('crm.lead',string='Listing Line',index=True)
    product_en = fields.Many2one('product.product','Product')
    qty_en = fields.Integer('Quantity')
    unit_price_en = fields.Float('Unit Price')
    total_price_en = fields.Float('Total Price')
    part_number = fields.Many2one('sequence.number.partner','Price History')
    tax_id = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)])
    internal_code_en = fields.Char('Internal Code')
    workpiece_material = fields.Many2one('workpiece.material','Workpiece Material')
    coating_en = fields.Many2one('coating.enquiry','Coating')
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', required=True)
    pricing_date = fields.Date('Pricing Date')
    remarks_en = fields.Text('Remarks')
    partner_id = fields.Many2one(string='Account' ,default=_get_partner,store=True, readonly=True)
    currency_id = fields.Many2one(related='lead_line_id.partner_id.property_product_pricelist.currency_id', store=True, string='Currency', readonly=True)
    discount = fields.Float(string='Discount (%)', digits=dp.get_precision('Discount'), default=0.0)
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    price_tax = fields.Monetary(compute='_compute_amount', string='Taxes', readonly=True, store=True)
    total_price_en = fields.Monetary(compute='_compute_amount', string='Total', readonly=True, store=True)

    @api.multi
    @api.onchange('unit_price_en')
    def on_changeunit_price_en(self):
        for ob in self:
            self.pricing_date = fields.Datetime.now()

    @api.multi
    @api.onchange('part_number')
    def part_number_change(self):
        for part in self:
            self.unit_price_en = part.part_number.seq_price

    @api.multi
    def create(self, vals):
        if vals.get('product_en'):
            pricelis_dict = {}
            for priclist in self.env['crm.lead'].browse(vals.get('lead_line_id')).partner_id.property_product_pricelist.item_ids:
                if priclist.product_id.id == vals.get('product_en'):
                    pricelis_dict = {
                        'item_ids': [(1, priclist.id, {'fixed_price': vals.get('unit_price_en')})]
                    }
            if not pricelis_dict:
                pricelis_dict = {
                    'item_ids': [(0, 0, {
                            'applied_on': '0_product_variant',
                            'compute_price': 'fixed',
                            'product_id':vals.get('product_en'),
                            'fixed_price': vals.get('unit_price_en'),
                        })]
                }
            vals.update({'pricing_date':fields.Datetime.now()})
            self.env['crm.lead'].browse(vals.get('lead_line_id')).partner_id.property_product_pricelist.write(pricelis_dict)
        res = super(crm_lead_line, self).create(vals)
        
        if vals.get('unit_price_en') != 0.0:
            part_id = ''
            list_of_part = []
            partner_obj = self.env['crm.lead'].browse(vals.get('lead_line_id')).partner_id
            if partner_obj:
                if partner_obj.sequence_ids:
                    for pit in partner_obj.sequence_ids:
                        if pit.product_id.id == vals.get('product_en') and pit.seq_price == vals.get('unit_price_en'):
                            part_id = pit
                            print "111111111111111111",pit.sequence_number , pit.name
                        if pit.product_id.id == vals.get('product_en') and pit.seq_price != vals.get('unit_price_en'):
                            print "222222222222222222",pit.sequence_number , pit.name
                            list_of_part.append(pit.sequence_number)                            
                        if pit.product_id.id != vals.get('product_en') and pit.seq_price != vals.get('unit_price_en'):
                            print "3333333333333333333",vals.get('unit_price_en')
                            seq_dict = {
                                'name': str(partner_obj.partner_code) + ' - PRICE 000' + str(1),
                                'sequence_id':partner_obj.id,
                                'product_id':vals.get('product_en'),
                                'seq_price':vals.get('unit_price_en'),
                                'sequence_number': 1,
                            }
                            part_id = self.env['sequence.number.partner'].create(seq_dict)
                else:
                    print ">>>>>>>>>>>>>>>>>>>>>"
                    seq_dict = {
                        'name': str(partner_obj.partner_code) + ' - PRICE 000' + str(1),
                        'sequence_id':partner_obj.id,
                        'product_id':vals.get('product_en'),
                        'seq_price':vals.get('unit_price_en'),
                        'sequence_number': 1,
                    }
                    part_id = self.env['sequence.number.partner'].create(seq_dict)

                if list_of_part:
                    seq_dict = {
                        'name': str(partner_obj.partner_code) + ' - PRICE 000' + str(max(list_of_part) + 1),
                        'sequence_id':partner_obj.id,
                        'product_id':vals.get('product_en'),
                        'seq_price':vals.get('unit_price_en'),
                        'sequence_number': max(list_of_part) + 1,
                    }
                    part_id = self.env['sequence.number.partner'].create(seq_dict)
                res.write({'part_number':part_id.id})
        return res

    @api.multi
    def write(self, vals):
        if vals.get('unit_price_en'):
            pricelis_dict = {}
            for priclist in self.lead_line_id.partner_id.property_product_pricelist.item_ids:
                if priclist.product_id.id == self.product_en.id:
                    pricelis_dict = {
                        'item_ids': [(1, priclist.id, {'fixed_price': vals.get('unit_price_en')})]
                    }
            if not pricelis_dict:
                pricelis_dict = {
                    'item_ids': [(0, 0, {
                            'applied_on': '0_product_variant',
                            'compute_price': 'fixed',
                            'product_id':self.product_en.id,
                            'fixed_price': vals.get('unit_price_en'),
                        })]
                }
            vals.update({'pricing_date':fields.Datetime.now()})
            self.lead_line_id.partner_id.property_product_pricelist.write(pricelis_dict)
            
            if vals.get('unit_price_en') != 0.0:
                part_id = ''
                list_of_part = []
                partner_obj = self.lead_line_id.partner_id
                if partner_obj:
                    if partner_obj.sequence_ids:
                        for pit in partner_obj.sequence_ids:
                            if pit.product_id.id == self.product_en.id and pit.seq_price == vals.get('unit_price_en'):
                                part_id = pit
                                print "111111111111111111",pit.sequence_number , pit.name
                            if pit.product_id.id == self.product_en.id and pit.seq_price != vals.get('unit_price_en'):
                                print "222222222222222222",pit.sequence_number , pit.name
                                list_of_part.append(pit.sequence_number)                            
                            if pit.product_id.id != self.product_en.id and pit.seq_price != vals.get('unit_price_en'):
                                print "3333333333333333333",vals.get('unit_price_en')
                                seq_dict = {
                                    'name': str(partner_obj.partner_code) + ' - PRICE 000' + str(1),
                                    'sequence_id':partner_obj.id,
                                    'product_id':self.product_en.id,
                                    'seq_price':vals.get('unit_price_en'),
                                    'sequence_number': 1,
                                }
                                part_id = self.env['sequence.number.partner'].create(seq_dict)
                    else:
                        print ">>>>>>>>>>>>>>>>>>>>>"
                        seq_dict = {
                            'name': str(partner_obj.partner_code) + ' - PRICE 000' + str(1),
                            'sequence_id':partner_obj.id,
                            'product_id':self.product_en.id,
                            'seq_price':vals.get('unit_price_en'),
                            'sequence_number': 1,
                        }
                        part_id = self.env['sequence.number.partner'].create(seq_dict)

                    if list_of_part:
                        seq_dict = {
                            'name': str(partner_obj.partner_code) + ' - PRICE 000' + str(max(list_of_part) + 1),
                            'sequence_id':partner_obj.id,
                            'product_id':self.product_en.id,
                            'seq_price':vals.get('unit_price_en'),
                            'sequence_number': max(list_of_part) + 1,
                        }
                        part_id = self.env['sequence.number.partner'].create(seq_dict)
                    vals.update({'part_number':part_id.id})
        return super(crm_lead_line, self).write(vals)

    # @api.multi
    # def unlink(self):
    #     for un in self:
    #         unlink_list = []
    #         for isd in self.env['part.number.line'].search([('part_line_id','=',un.id)]):
    #             isd.unlink()
    #     return super(crm_lead_line, self).unlink()

    @api.multi
    def _get_display_price(self, product):
        product_context = {}
        product_context['pricelist'] = self.lead_line_id.partner_id.property_product_pricelist.id
        price = product.with_context(product_context).price
        return price


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
            # vals['unit_price_en'] = 0.0
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


    sequence_ids = fields.One2many('sequence.number.partner','sequence_id','Sequence')
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
    vat_number = fields.Char('Vat Number (NPWP No.)')
    country_code = fields.Char('Country Code')
    state_id2 = fields.Many2one("res.country.state", 'State', ondelete='restrict')
    state_id2_delivery = fields.Many2one("res.country.state", 'State', ondelete='restrict')
        # REFERENCE DETAILS
    ref_name = fields.Char('Name')
    ref_phone = fields.Char('Phone')
    ref_mobile = fields.Char('Mobile')
    ref_email = fields.Char('Email')
    short_name = fields.Char('Short Name', required=True)
    acc_type = fields.Selection(string='Account Type',selection=[('local','Local'), ('international', 'International')],default="local")

    _sql_constraints = [('partner_code_uniq', 'unique (partner_code)', "Account Code already exists !")]

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

    hide_confirm = fields.Boolean('Hide')
    or_sale_id = fields.Many2one('Origin')

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
                line_dict = {
                    'product_id':op_line.product_en,
                    'product_uom_qty':op_line.qty_en,
                    'part_number':op_line.part_number.id,
                    'price_unit':op_line.unit_price_en,
                    'discount':op_line.discount,
                    'stat_line':'open',
                    'tax_id':[(6,0,taxlist)],
                    'product_uom':op_line.product_uom,
                    'currency_id':op_line.currency_id,
                }
                order_lines.append((0, 0, line_dict))
                self.order_line = order_lines
        # return res

    @api.multi
    def action_confirm(self):
        for order in self:
            new_order  = ''
            num_of_line = 0
            line_list = []
            for line in order.order_line:
                if line.confirm_line_box == True and line.stat_line == 'open':
                    taxlist = []
                    for itax in line.tax_id:
                        taxlist.append(itax.id)
                    line_list.append((0, 0, {
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_uom_qty,
                        'price_unit':line.price_unit,
                        'discount': line.discount,
                        'name':line.name,
                        'part_number':line.part_number.id,
                        'stat_line':'so',
                        'confirm_line_box':True,
                        'layout_category_id':line.layout_category_id.id,
                        'product_uom':line.product_uom.id,
                        'customer_lead':line.customer_lead,
                        'tax_id':[(6,0,taxlist)],
                    }))
                    line.write({'stat_line':'so'})
            for line in order.order_line:
                if line.stat_line == 'so':
                    num_of_line += 1
            if line_list:
                order_name = self.search_count([('or_sale_id','=',order.id)])
                if order_name == 0:
                    order_name = 1
                else:
                    order_name += 1
                sale_dict = {
                    'name':order.name + '/SO' + str(order_name),
                    'sale_order_name_id':order.sale_order_name_id.id,
                    'partner_id':order.partner_id.id,
                    'date_order':order.date_order,  
                    'pricelist_id':order.pricelist_id.id,
                    'user_id':order.user_id.id,
                    'picking_policy':order.picking_policy,
                    'opportunity_id':order.opportunity_id.id,
                    'warehouse_id':order.warehouse_id.id,
                    'team_id':order.team_id.id,
                    'or_sale_id':order.id,
                    'revision':order.revision,
                    'goods_label':order.goods_label,
                    'payment_term_id':order.payment_term_id.id,
                    'hide_confirm':True,
                    'order_line':line_list,
                }
                new_order = self.env['sale.order'].create(sale_dict)
                new_order.state = 'sale'
                new_order.confirmation_date = fields.Datetime.now()
                new_order.order_line._action_procurement_create()
                if self.env.context.get('send_email'):
                    new_order.force_quotation_send()
        
                if self.env['ir.values'].get_default('sale.config.settings', 'auto_done_setting'):
                    new_order.action_done()
            if len(order.order_line) != 0:
                if num_of_line == len(order.order_line):
                    order.write({'hide_confirm':True})
            if line_list:
                models_data = self.env['ir.model.data']
                # Get opportunity views
                dummy, form_view = models_data.get_object_reference('sale', 'view_order_form')
                dummy, tree_view = models_data.get_object_reference('sale', 'view_order_tree')
                return {
                    'name': _('Sale Order'),
                    'view_type': 'form',
                    'view_mode': 'tree, form',
                    'res_model': 'sale.order',
                    'res_id': int(new_order.id),
                    'view_id': False,
                    'views': [(form_view or False, 'form'),
                              (tree_view or False, 'tree'),],
                    'type': 'ir.actions.act_window',
                    'context': {}
                }
            else:
                raise UserError(_('Please Select Order Line Before Confirm Order.'))
        return True

class sale_order_line(models.Model):
    _inherit= 'sale.order.line'

    part_number = fields.Many2one('sequence.number.partner','Part Number')
    confirm_line_box = fields.Boolean('.')
    stat_line = fields.Selection([('so','SO'),('open','Open')],'Status',default='open')


    @api.multi
    def create(self, vals):
        if not vals.get('name'):
            vals.update({'name':self.env['product.product'].browse(vals.get('product_id')).name})
        if vals.get('product_id'):
            pricelis_dict = {}
            for priclist in self.env['sale.order'].browse(vals.get('order_id')).partner_id.property_product_pricelist.item_ids:
                if priclist.product_id.id == vals.get('product_id'):
                    pricelis_dict = {
                        'item_ids': [(1, priclist.id, {'fixed_price': vals.get('price_unit')})]
                    }
            if not pricelis_dict:
                pricelis_dict = {
                    'item_ids': [(0, 0, {
                            'applied_on': '0_product_variant',
                            'compute_price': 'fixed',
                            'product_id':vals.get('product_id'),
                            'fixed_price': vals.get('price_unit'),
                        })]
                }
            self.env['sale.order'].browse(vals.get('order_id')).partner_id.property_product_pricelist.write(pricelis_dict)
        return super(sale_order_line, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('price_unit'):
            pricelis_dict = {}
            for priclist in self.order_id.partner_id.property_product_pricelist.item_ids:
                if priclist.product_id.id == self.product_id.id:
                    pricelis_dict = {
                        'item_ids': [(1, priclist.id, {'fixed_price': vals.get('price_unit')})]
                    }
            if not pricelis_dict:
                pricelis_dict = {
                    'item_ids': [(0, 0, {
                            'applied_on': '0_product_variant',
                            'compute_price': 'fixed',
                            'product_id':self.product_id.id,
                            'fixed_price': vals.get('price_unit'),
                        })]
                }
            self.order_id.partner_id.property_product_pricelist.write(pricelis_dict)
        return super(sale_order_line, self).write(vals)