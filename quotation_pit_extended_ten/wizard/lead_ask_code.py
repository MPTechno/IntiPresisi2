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


class crm_askcode_partner(models.TransientModel):
	_name = 'crm.askcode.partner'
	_description = 'Lead To Partner'


	short_name = fields.Char('Short Name', required=True)
	code_partner = fields.Char('Code',required=True)
	acc_type = fields.Selection(string='Account Type',selection=[('local','Local'), ('international', 'International')],default="local")

	@api.onchange('acc_type')
	def onchange_acc_type(self):
		for partner in self:
			if self._context.get('active_id'):
				lead_obje = self.env['crm.lead'].browse(self._context.get('active_id'))
				if self.acc_type == 'local':
					self.code_partner = str(1130)+ '/' + str(lead_obje.comp_name[:1])
				else:
					self.code_partner = str(1137)+ '/' + str(lead_obje.comp_name[:1])

	@api.v7
	def convert_to_part(self,context=None):
		if context.get('active_id'):
			w = self
			lead_obje = self.env['crm.lead'].browse(context.get('active_id'))
			partner = self.env['res.partner']
			vals_dict = {}
			if lead_obje.comp_name:
				sale_pricelist_id = self.env['product.pricelist'].create({
					'name':str(w.short_name) + '_' + str(w.code_partner),
					'item_ids': [(0, 0, {
							'applied_on': '3_global',
							'compute_price': 'fixed',
							'fixed_price': 0.0,
						})]
				})
				contact_dict = {
					'partner_code': w.code_partner + '/CON',
					'short_name':w.short_name,
					'acc_type':w.acc_type,
					'name':lead_obje.name,
					'title':lead_obje.title.id,
					'function':lead_obje.function,
					'user_id': self._uid,
					'email':lead_obje.email_from,
					'mobile':lead_obje.mobile,
					'property_product_pricelist':sale_pricelist_id.id,
					'is_company': False,
					'company_type':'person',
					'type': 'contact',
					'customer':True,
					'supplier':False,
				}
				vals_dict = {
					'partner_code': w.code_partner,
					'short_name':w.short_name,
					'acc_type':w.acc_type,
					'child_ids':[(0,0,contact_dict)],
					'name':lead_obje.comp_name,
					'phone':lead_obje.phone,
					'user_id': self._uid,
					'partner_code':w.code_partner,
					'street':lead_obje.street,
					'street2':lead_obje.street2,
					'city':lead_obje.city,
					'state_id':lead_obje.state_id.id,
					'website':lead_obje.website,
					'fax':lead_obje.fax,
					'country_id':lead_obje.country_id.id,
					'zip':lead_obje.zip,
					'property_product_pricelist':sale_pricelist_id.id,
					'is_company': True,
					'company_type':'company',
					'type': 'contact',
					'customer':True,
					'supplier':False,
				}
				partner_id = partner.create(vals_dict)
				lead_obje.unlink()
				models_data = self.env['ir.model.data']

				# Get opportunity views
				dummy, form_view = models_data.get_object_reference('base', 'view_partner_form')
				dummy, tree_view = models_data.get_object_reference('base', 'view_partner_tree')
				return {
					'name': _('Accounts'),
					'view_type': 'form',
					'view_mode': 'tree, form',
					'res_model': 'res.partner',
					'res_id': int(partner_id),
					'view_id': False,
					'views': [(form_view or False, 'form'),
							  (tree_view or False, 'tree'),],
					'type': 'ir.actions.act_window',
					'context': {}
				}


class crm_askcode_ponumber(models.TransientModel):
	_name = 'crm.askcode.ponumber'

	po_num = fields.Char('PO Number', required=True)

	@api.one
	def confirm_sale(self):
		self.with_context({'po_num':self.po_num})
		context = self.env.context.copy()
		context.update({'po_num':self.po_num})
		new_order = self.env['sale.order'].browse(self._context.get('active_id')).with_context(context).action_confirm()
		print ">>>>>>>>",new_order
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


class coating_date_wizard(models.TransientModel):
	_name = 'coating.date.wizard'

	start_date = fields.Date('Start Date', required=True)
	end_date = fields.Date('End Date',required=True)

	@api.multi
	def get_total(self, obj):
		sale_obj = self.env['sale.order'].search([('state','=','sale'),('confirmation_date','>=',obj.start_date),('confirmation_date','<=',obj.end_date)])
		list_of_line = 0.0
		if sale_obj:
			for order in sale_obj:
				for line in order.order_line:
					if line.coating_en:
						list_of_line += line.price_subtotal
		final_dict = {
			'currency_id':self.env.user.company_id.currency_id,
			'total':list_of_line
		}
		return final_dict		

	@api.multi
	def get_order_line(self,obj):
		sale_obj = self.env['sale.order'].search([('state','=','sale'),('confirmation_date','>=',obj.start_date),('confirmation_date','<=',obj.end_date)])
		list_of_line = []
		if sale_obj:
			for order in sale_obj:
				for line in order.order_line:
					if line.coating_en:
						list_of_line.append(line)
		return list_of_line

	@api.multi
	def confirm_print(self):
		datas = {
			'ids': [],
			'model': 'sale.order',
			'date_start': self.start_date,
			'date_stop': self.end_date
		}
		return self.env['report'].get_action([], 'quotation_pit_extended_ten.coating_report_template', data=datas)
