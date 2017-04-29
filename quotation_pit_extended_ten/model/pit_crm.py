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
    prospect_source_ids = fields.One2many('crm.lead','prospect_source','Lead')

class industry_source(models.Model):
    _name = 'industry.source'
    
    name = fields.Char('Industry Name')
    indus_ids = fields.One2many('crm.lead','industry_source_id','Lead')

class qty_machine(models.Model):
    _name = 'qty.machine'
    
    name = fields.Char('Name')
    q_machine_ids = fields.One2many('crm.lead','quantity_of_machine','Lead')

class prospect_production(models.Model):
    _name = 'prospect.production'
    
    name = fields.Char('Name')
    prospect_production_ids = fields.One2many('crm.lead','prospect_production','Lead')

class customer_group(models.Model):
    _name = 'customer.group'
    
    name = fields.Char('Name')
    customer_group_ids = fields.One2many('res.partner','customer_group_id','Lead')

class crm_lead(models.Model):
    _inherit = 'crm.lead'

    
    partner_name = fields.Char('Account Name',required=True)
    stage_new_id = fields.Many2one('crm.stage', string='Stage', track_visibility='onchange', index=True,
        domain="['|', ('team_id', '=', False), ('team_id', '=', team_id)]",
        group_expand='_read_group_stage_ids', default=lambda self: self._default_stage_id())
    prospect_quality = fields.Selection([('a','A'),('b','B'),('c','C'),('d','D'),('e','E')], 'Prospect Quality')
    website = fields.Char('Website')


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

    @api.multi
    def write(self, vals):
        # stage change: update date_last_stage_update
        if 'stage_new_id' in vals:
            vals['stage_id'] = vals.get('stage_new_id')
        return super(crm_lead, self).write(vals)

    @api.model
    def _onchange_stage_id_values(self, stage_id):
        """ returns the new values when stage_id has changed """
        if not stage_id:
            return {}
        stage = self.env['crm.stage'].browse(stage_id)
        if stage.on_change:
            return {'probability': stage.probability}
        if stage.id != self.browse(cr, uid, ids, context=context).stage_new_id.id:
            vals['stage_new_id'] = stage.id
        return {'value': vals}

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    g_map = fields.Text('map')
    partner_code = fields.Char('Code',required=True)
    street_delivery =  fields.Char('Street')
    street2_delivery =  fields.Char('Street2')
    zip_delivery =  fields.Char('Zip', size=24, change_default=True)
    city_delivery =  fields.Char('City')
    state_id_delivery =  fields.Many2one("res.country.state", 'State', ondelete='restrict')
    country_id_delivery =  fields.Many2one('res.country', 'Country', ondelete='restrict')
    mailing_address_name = fields.Char('Name')
    delivery_address_name = fields.Char('Name')
    city2_mailing =  fields.Char('City')
    city2_delivery =  fields.Char('City')
    zip2_mailing =  fields.Char('Zip')
    zip2_delivery =  fields.Char('Zip')
    currency_id =  fields.Many2one('res.currency', 'Currency')
    customer_group_id = fields.Many2one('customer.group','Customer Group')
    vat_code = fields.Char('Vat Code')
    vat_number = fields.Char('Vat Number')
    country_code = fields.Char('Country Code')

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