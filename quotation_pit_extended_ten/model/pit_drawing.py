# -*- coding: utf-8 -*-
from odoo.osv.orm import setup_modifiers
from datetime import datetime
from dateutil.relativedelta import relativedelta
from lxml import etree
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
import odoo.addons.decimal_precision as dp

class product_pricelist_item(models.Model):
	_inherit = 'product.pricelist.item'

	part_number = fields.Many2one('sequence.number.partner','Price History')
	part_number_product = fields.Many2one('sequence.number.product','Part Number')
	drawing_number = fields.Char('Drawing Number')
	pricing_date = fields.Date('Pricing Date')
	quantity_new = fields.Integer('Quantity',default=0)

	@api.multi
	@api.onchange('quantity_new')
	def on_changeunit_quantity_new(self):
		for ob in self:
			ob.write({'quantity_new':self.quantity_new})

class res_partner(models.Model):
	_inherit = "res.partner"

	sequence_number = fields.Integer('Sequence',default=0)

class sequence_number_partner(models.Model):
	_name = "sequence.number.partner"

	sequence_id = fields.Many2one('res.partner','Account')
	product_id = fields.Many2one('product.product','Product')
	sequence_number = fields.Integer('Sequence')
	seq_price = fields.Float('Price')
	name = fields.Char('Name')
	pricing_date = fields.Date('Pricing Date')


class sequence_number_product(models.Model):
	_name = "sequence.number.product"

	partner_id = fields.Many2one('res.partner','Account')
	product_id = fields.Many2one('product.product','Product')
	drawing_number = fields.Char('Drawing Number')
	name = fields.Char('Name')


class crm_lead_line(models.Model):
	_inherit='crm.lead.line'


	@api.multi
	def create(self, vals):
		if vals.get('unit_price_en') != 0.0:
			part_id = ''
			list_of_part = []
			partner_obj = self.env['crm.lead'].browse(vals.get('lead_line_id')).partner_id
			if partner_obj:
				if partner_obj.sequence_ids:
					for pit in partner_obj.sequence_ids:
						if not vals.get('part_number'):
							if pit.product_id.id == vals.get('product_en') and pit.seq_price == vals.get('unit_price_en'):
								part_id = pit
								print "111111111111111111",pit.sequence_number , pit.name
							if pit.product_id.id == vals.get('product_en') and pit.seq_price != vals.get('unit_price_en'):
								print "222222222222222222",pit.sequence_number , pit.name
								list_of_part.append(pit.sequence_number)                            
							if pit.product_id.id != vals.get('product_en') and pit.seq_price != vals.get('unit_price_en'):
								print "3333333333333333333",vals.get('unit_price_en')
				
						if vals.get('part_number'):
							if pit.id == vals.get('part_number') and pit.seq_price == vals.get('unit_price_en'):
								print "4444444444444444444",pit
								part_id = pit

							if pit.id == vals.get('part_number') and pit.seq_price != vals.get('unit_price_en'):
								list_of_part.append(pit.sequence_number)
								print "5555555555555555555",list_of_part

					if not part_id and not list_of_part:
						print ">>>>>>>>>>>>>>>>>>>>>"
						seq_dict = {
							'name': str(partner_obj.partner_code) + ' - PRICE 0000' + str(1),
							'sequence_id':partner_obj.id,
							'product_id':vals.get('product_en'),
							'seq_price':vals.get('unit_price_en'),
							'sequence_number': 1,
							'pricing_date':fields.Datetime.now(),
						}
						part_id = self.env['sequence.number.partner'].create(seq_dict)

				else:
					if not partner_obj.sequence_ids:
						seq_dict = {
							'name': str(partner_obj.partner_code) + ' - PRICE 0000' + str(1),
							'sequence_id':partner_obj.id,
							'product_id':vals.get('product_en'),
							'seq_price':vals.get('unit_price_en'),
							'sequence_number': 1,
							'pricing_date':fields.Datetime.now(),
						}
						part_id = self.env['sequence.number.partner'].create(seq_dict)

				if list_of_part:
					seq_dict = {
						'name': str(partner_obj.partner_code) + ' - PRICE 0000' + str(max(list_of_part) + 1),
						'sequence_id':partner_obj.id,
						'product_id':vals.get('product_en'),
						'seq_price':vals.get('unit_price_en'),
						'sequence_number': max(list_of_part) + 1,
						'pricing_date':fields.Datetime.now(),
					}
					part_id = self.env['sequence.number.partner'].create(seq_dict)
				vals.update({'part_number':part_id.id})
		if vals.get('internal_code_en', False):
			part_id = ''
			list_of_part = []
			partner_obj = self.env['res.partner'].browse(vals.get('partner_id'))
			draw_dict = {}
			if partner_obj:
				if partner_obj.drawing_ids:
					for pit in partner_obj.drawing_ids:
						if not vals.get('part_number_product'):
							if pit.product_id.id == vals.get('product_en') and pit.drawing_number == vals.get('internal_code_en'):
								part_id = pit
							if pit.product_id.id == vals.get('product_en') and pit.drawing_number != vals.get('internal_code_en'):
								list_of_part.append(pit.partner_id.sequence_number)                            

						if vals.get('part_number_product'):
							if pit.id == vals.get('part_number_product') and pit.drawing_number == vals.get('internal_code_en'):
								part_id = pit

							if pit.id == vals.get('part_number_product') and pit.drawing_number != vals.get('internal_code_en'):
								list_of_part.append(pit.partner_id.sequence_number)

					if not part_id and not list_of_part:
						seq_dict = {
							'name': str(partner_obj.partner_code) + ' - ' + str(format(partner_obj.sequence_number + 1, '05')),
							'partner_id':partner_obj.id,
							'product_id':vals.get('product_en'),
							'drawing_number':vals.get('internal_code_en'),
						}
						part_id = self.env['sequence.number.product'].create(seq_dict)
						partner_obj.write({'sequence_number': partner_obj.sequence_number + 1})
				else:
					draw_dict = {
						'name': str(partner_obj.partner_code) + ' - ' + format(partner_obj.sequence_number + 1, '05'),
						'partner_id':partner_obj.id,
						'product_id':vals.get('product_en'),
						'drawing_number':vals.get('internal_code_en'),
					}
					part_id = self.env['sequence.number.product'].create(draw_dict)
					partner_obj.write({'sequence_number': partner_obj.sequence_number + 1})
				print "##########",list_of_part ,vals
				if list_of_part:
					seq_dict = {
						'name': str(partner_obj.partner_code) + ' - ' + str(format(max(list_of_part) + 1, '05')),
						'partner_id':partner_obj.id,
						'product_id':vals.get('product_en'),
						'drawing_number':vals.get('internal_code_en'),
					}
					part_id = self.env['sequence.number.product'].create(seq_dict)
					partner_obj.write({'sequence_number': max(list_of_part) + 1})
				vals.update({'part_number_product':part_id.id})
		if vals.get('unit_price_en') != 0.0:
			pricelis_dict = {}
			pricelis_dict = {
				'item_ids': [(0, 0, {
						'applied_on': '0_product_variant',
						'compute_price': 'fixed',
						'product_id':vals.get('product_en'),
						'fixed_price': vals.get('unit_price_en'),
						'part_number':vals.get('part_number'),
						'drawing_number':vals.get('internal_code_en'),
						'pricing_date':fields.Datetime.now(),
						'part_number_product':vals.get('part_number_product'),
					})]
			}
			vals.update({'pricing_date':fields.Datetime.now()})
			self.env['crm.lead'].browse(vals.get('lead_line_id')).partner_id.property_product_pricelist.write(pricelis_dict)
		return super(crm_lead_line, self).create(vals)

	@api.multi
	def write(self, vals):
		print "WWWWWWWWWWcccccccccccc",vals
		if vals.get('unit_price_en') and vals.get('unit_price_en') != 0.0:
			part_id = ''
			list_of_part = []
			partner_obj = self.lead_line_id.partner_id
			if partner_obj:
				if partner_obj.sequence_ids:
					for pit in partner_obj.sequence_ids:
						if self.part_number and not vals.get('part_number'):
							if pit.product_id.id == self.product_en.id and pit.seq_price == vals.get('unit_price_en'):
								part_id = pit
								print "111111111111111111",pit.sequence_number , pit.name
							if pit.product_id.id == self.product_en.id and pit.seq_price != vals.get('unit_price_en'):
								print "222222222222222222",pit.sequence_number , pit.name
								list_of_part.append(pit.sequence_number)                            
							if self.part_number.id == pit.id and pit.product_id.id != self.product_en.id and pit.seq_price != vals.get('unit_price_en'):
								print "3333333333333333333",vals.get('unit_price_en')
						
						if vals.get('part_number'):
							if pit.id == vals.get('part_number') and pit.seq_price == vals.get('unit_price_en'):
								print "4444444444444444444",pit
								part_id = pit
							if pit.id == vals.get('part_number') and pit.seq_price != vals.get('unit_price_en'):
								list_of_part.append(pit.sequence_number)
								print "5555555555555555555",list_of_part

				if not part_id and not list_of_part:
					print "66666666666666666"
					seq_dict = {
						'name': str(partner_obj.partner_code) + ' - PRICE 0000' + str(1),
						'sequence_id':partner_obj.id,
						'product_id':self.product_en.id,
						'seq_price':vals.get('unit_price_en'),
						'sequence_number': 1,
						'pricing_date':fields.Datetime.now(),
					}
					part_id = self.env['sequence.number.partner'].create(seq_dict)

				if list_of_part:
					seq_dict = {
						'name': str(partner_obj.partner_code) + ' - PRICE 0000' + str(max(list_of_part) + 1),
						'sequence_id':partner_obj.id,
						'product_id':self.product_en.id,
						'seq_price':vals.get('unit_price_en'),
						'sequence_number': max(list_of_part) + 1,
						'pricing_date':fields.Datetime.now(),
					}
					part_id = self.env['sequence.number.partner'].create(seq_dict)
				print "WWWWWWWWWW",part_id
				vals.update({'part_number':part_id.id})
		print "WWWWWWWWWWWWW111111111WWWWWWWWWWWWWWW",vals
		if vals.get('internal_code_en', False):
			part_id = ''
			list_of_part = []
			partner_obj = self.lead_line_id.partner_id
			if partner_obj:
				if partner_obj.drawing_ids:
					for pit in partner_obj.drawing_ids:
						if self.part_number_product and not vals.get('part_number_product'):
							if pit.product_id.id == self.product_en.id and pit.drawing_number == vals.get('internal_code_en'):
								part_id = pit
							if pit.product_id.id == self.product_en.id and pit.drawing_number != vals.get('internal_code_en'):
								list_of_part.append(pit.partner_id.sequence_number)                            
							if self.part_number_product.id == pit.id and pit.product_id.id != self.product_en.id and pit.drawing_number != vals.get('internal_code_en'):
								pass						
						if vals.get('part_number_product'):
							if pit.id == vals.get('part_number_product') and pit.drawing_number == vals.get('internal_code_en'):
								part_id = pit
							if pit.id == vals.get('part_number_product') and pit.drawing_number != vals.get('internal_code_en'):
								list_of_part.append(pit.partner_id.sequence_number)

					if not part_id and not list_of_part:
						draw_dict = {
							'name': str(partner_obj.partner_code) + ' - ' + format(partner_obj.sequence_number + 1, '05'),
							'partner_id':partner_obj.id,
							'product_id':self.product_en.id,
							'drawing_number':vals.get('internal_code_en'),
						}
						part_id = self.env['sequence.number.product'].create(draw_dict)
						partner_obj.write({'sequence_number': partner_obj.sequence_number + 1})
				else:
					draw_dict = {
						'name': str(partner_obj.partner_code) + ' - ' + format(partner_obj.sequence_number + 1, '05'),
						'partner_id':partner_obj.id,
						'product_id':self.product_en.id,
						'drawing_number':vals.get('internal_code_en'),
					}
					part_id = self.env['sequence.number.product'].create(draw_dict)
					partner_obj.write({'sequence_number': partner_obj.sequence_number + 1})
				if list_of_part:
					draw_dict = {
						'name': str(partner_obj.partner_code) + ' - ' + str(format(max(list_of_part) + 1, '05')),
						'partner_id':partner_obj.id,
						'product_id':self.product_en.id,
						'drawing_number':vals.get('internal_code_en'),
					}
					part_id = self.env['sequence.number.product'].create(draw_dict)
					partner_obj.write({'sequence_number': max(list_of_part) + 1})
				vals.update({'part_number_product':part_id.id})
		if vals.get('unit_price_en')  or vals.get('internal_code_en'):
			print "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",vals
			pricelis_dict = {}
			pricelis_dict = {
				'item_ids': [(0, 0, {
						'applied_on': '0_product_variant',
						'compute_price': 'fixed',
						'product_id':self.product_en.id,
						'fixed_price': vals.get('unit_price_en'),
						'part_number':vals.get('part_number') or self.part_number.id,
						'drawing_number':vals.get('internal_code_en') or self.internal_code_en,
						'pricing_date':fields.Datetime.now(),
						'part_number_product':vals.get('part_number_product') or self.part_number_product.id,
					})]
			}
			if not vals.get('pricing_date'):
				vals.update({'pricing_date':fields.Datetime.now()})
			self.lead_line_id.partner_id.property_product_pricelist.write(pricelis_dict)
		return super(crm_lead_line, self).write(vals)

	@api.multi
	@api.onchange('unit_price_en')
	def on_changeunit_price_en(self):
		for ob in self:
			self.pricing_date = fields.Datetime.now()

	@api.multi
	@api.onchange('part_number')
	def part_number_change(self):
		for part in self:
			values = {
				'unit_price_en': part.part_number.seq_price,
				'pricing_date': part.part_number.pricing_date,
			}
		self.update(values)

	@api.multi
	@api.onchange('part_number_product')
	def part_number_product_change(self):
		for part in self:
			self.internal_code_en = part.part_number_product.drawing_number

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
		if product:
			vals['workpiece_grade'] = product.workpiece_grade.id
			vals['kind_of_machine'] = product.kind_of_machine.id
			vals['coating_en'] = product.coating_en.id
			vals['workpiece_material'] = product.workpiece_material.id
			vals['remarks_en'] = product.pro_remark
			vals['internal_code_en'] = product.drawing_no

		if product.description_sale:
			name += '\n' + product.description_sale
		vals['remarks_en'] = name
		if product:
			vals['unit_price_en'] = self.env['account.tax']._fix_tax_included_price(self._get_display_price(product), product.taxes_id, self.tax_id)
			# vals['unit_price_en'] = 0.0
		self.update(vals)