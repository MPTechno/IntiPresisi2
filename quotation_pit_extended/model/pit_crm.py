# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.http import request
from datetime import datetime
from openerp.tools.translate import _
import openerp
from openerp import tools, api
class prospect_source(osv.osv):
    _name='prospect.source'
    _columns = {
        'name':fields.char('Prospect Source Name'),
        'prospect_source_ids':fields.one2many('crm.lead','prospect_source','Lead'),
    }

class industry_source(osv.osv):
    _name = 'industry.source'
    _columns = {
        'name':fields.char('Industry Name'),
        'indus_ids':fields.one2many('crm.lead','industry_source','Lead'),
    }
class qty_machine(osv.osv):
    _name = 'qty.machine'
    _columns = {
        'name':fields.char('Name'),
        'q_machine_ids':fields.one2many('crm.lead','quantity_of_machine','Lead'),
    }

class prospect_production(osv.osv):
    _name = 'prospect.production'
    _columns = {
        'name':fields.char('Name'),
        'prospect_production_ids':fields.one2many('crm.lead','prospect_production','Lead'),
    }

class customer_group(osv.osv):
    _name = 'customer.group'
    _columns = {
        'name':fields.char('Name'),
        'customer_group_ids':fields.one2many('res.partner','customer_group_id','Lead'),
    }


class crm_lead(osv.osv):
    _inherit = 'crm.lead'

    _columns = {
        'partner_name':fields.char('Account Name',required=True),
        'stage_new_id': fields.many2one('crm.case.stage', 'Stage', select=True,
                        domain="['&', ('section_ids', '=', section_id), '|', ('type', '=', type), ('type', '=', 'both')]"),
        'prospect_quality':fields.selection([('a','A'),('b','B'),('c','C'),('d','D'),('e','E')], 'Prospect Quality'),
        'website':fields.char('Website'),


        # Additional Information
        'no_of_employee' : fields.integer('No of Employee'),
        'annual_revenue' : fields.integer('Annual Revenue'),
        'prospect_source':fields.many2one('prospect.source','Prospect Source'),
        'industry_source':fields.many2one('industry.source','Industry'),

        # Prospect Scoring:
        'special_carbide_tools':fields.boolean('Special Carbide Tools'),
        'qty_per_month':fields.integer('Quantity Per Month'),
        'quantity_of_machine':fields.many2one('qty.machine','Quantity of Machine'),
        'prospect_production':fields.many2one('prospect.production','Production'),
        'special_carbide_tools_score':fields.integer('Special Carbide Tools Score'),
        'quantity_per_month_score':fields.integer('Quantity Per Month Score'),
        'quantity_of_machine_score':fields.integer('Quantity of Machine Score'),
        'production_score':fields.integer('Production Score'),
        'total_score':fields.integer('Total Score'),
    
        # Description Information:
        'description_prospect':fields.text('Description'),
    
        # System Information:
        'created_by':fields.char('Created By'),
        'last_modified_by':fields.char('Last Modified By'),
    }

    def write(self, cr, uid, ids, vals, context=None):
        res = super(crm_lead, self).write(cr, uid, ids, vals, context=context)
        for lead_obj in self.browse(cr, uid, ids, context=context):
            if vals.get('stage_new_id'):
                self.pool.get('crm.lead').write(cr, uid, lead_obj.id, {'stage_id':vals.get('stage_new_id')},context=context)
        return res

    def onchange_stage_id(self, cr, uid, ids, stage_id, context=None):
        if not stage_id:
            return {'value': {}}
        stage = self.pool.get('crm.case.stage').browse(cr, uid, stage_id, context=context)
        if not stage.on_change:
            return {'value': {}}
        vals = {'probability': stage.probability}
        if stage.probability >= 100 or (stage.probability == 0 and stage.sequence > 1):
                vals['date_closed'] = fields.datetime.now()
        if stage.id != self.browse(cr, uid, ids, context=context).stage_new_id.id:
            vals['stage_new_id'] = stage.id
        return {'value': vals}


class res_partner(osv.osv):
    _inherit = 'res.partner'
    _columns = {
        'partner_code':fields.char('Code',required=True),
        'street_delivery': fields.char('Street'),
        'street2_delivery': fields.char('Street2'),
        'zip_delivery': fields.char('Zip', size=24, change_default=True),
        'city_delivery': fields.char('City'),
        'state_id_delivery': fields.many2one("res.country.state", 'State', ondelete='restrict'),
        'country_id_delivery': fields.many2one('res.country', 'Country', ondelete='restrict'),
        'mailing_address_name':fields.char('Name'),
        'delivery_address_name':fields.char('Name'),
        'city2_mailing': fields.char('City'),
        'city2_delivery': fields.char('City'),
        'zip2_mailing': fields.char('Zip'),
        'zip2_delivery': fields.char('Zip'),
        'currency_id': fields.many2one('res.currency', 'Currency'),
        'customer_group_id':fields.many2one('customer.group','Customer Group'),
        'vat_code':fields.char('Vat Code'),
        'vat_number':fields.char('Vat Number'),
        'country_code':fields.char('Country Code'),

        # REFERENCE DETAILS
        'ref_name':fields.char('Name'),
        'ref_phone':fields.char('Phone'),
        'ref_mobile':fields.char('Mobile'),
        'ref_email':fields.char('Email'),
    }

    @api.multi
    def onchange_state_delivery(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id_delivery': state.country_id.id}}
        return {}