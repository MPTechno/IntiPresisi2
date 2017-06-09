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

class sequence_number_product(models.Model):
	_name = "sequence.number.product"

	partner_id = fields.Many2one('res.partner','Account')
	product_id = fields.Many2one('product.product','Product')
	sequence_number = fields.Integer('Sequence')
	drawing_number = fields.Char('Drawing Number')
	name = fields.Char('Name')


class crm_lead_line(models.Model):
	_inherit='crm.lead.line'


	@api.multi
	def create(self, vals):
		res = super(crm_lead_line, self).create(vals)
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
								list_of_part.append(pit.sequence_number)                            
							if pit.product_id.id != vals.get('product_en') and pit.drawing_number != vals.get('internal_code_en'):
								pass						
						if vals.get('part_number_product'):
							if pit.id == vals.get('part_number_product') and pit.drawing_number == vals.get('internal_code_en'):
								part_id = pit

							if pit.id == vals.get('part_number_product') and pit.drawing_number != vals.get('internal_code_en'):
								list_of_part.append(pit.sequence_number)

					if not part_id and not list_of_part:
						seq_dict = {
							'name': str(partner_obj.partner_code) + ' - ' + str(format(1, '04')),
							'partner_id':partner_obj.id,
							'product_id':vals.get('product_en'),
							'drawing_number':vals.get('internal_code_en'),
							'sequence_number': 1,
						}
						part_id = self.env['sequence.number.product'].create(seq_dict)
				else:
					draw_dict = {
						'name': str(partner_obj.partner_code) + ' - ' + format(1, '04'),
						'partner_id':partner_obj.id,
						'product_id':vals.get('product_en'),
						'drawing_number':vals.get('internal_code_en'),
						'sequence_number': 1,
					}
					part_id = self.env['sequence.number.product'].create(draw_dict)

				if list_of_part:
					seq_dict = {
						'name': str(partner_obj.partner_code) + ' - ' + str(format(max(list_of_part) + 1, '04')),
						'partner_id':partner_obj.id,
						'product_id':vals.get('product_en'),
						'drawing_number':vals.get('internal_code_en'),
						'sequence_number': max(list_of_part) + 1,
					}
					part_id = self.env['sequence.number.product'].create(seq_dict)
				res.write({'part_number_product':part_id.id})
		return res

	@api.multi
	def write(self, vals):
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
								list_of_part.append(pit.sequence_number)                            
							if self.part_number_product.id == pit.id and pit.product_id.id != self.product_en.id and pit.drawing_number != vals.get('internal_code_en'):
								pass						
						if vals.get('part_number_product'):
							if pit.id == vals.get('part_number_product') and pit.drawing_number == vals.get('internal_code_en'):
								part_id = pit
							if pit.id == vals.get('part_number_product') and pit.drawing_number != vals.get('internal_code_en'):
								list_of_part.append(pit.sequence_number)

					if not part_id and not list_of_part:
						draw_dict = {
							'name': str(partner_obj.partner_code) + ' - ' + format(1, '04'),
							'partner_id':partner_obj.id,
							'product_id':self.product_en.id,
							'drawing_number':vals.get('internal_code_en'),
							'sequence_number': 1,
						}
						part_id = self.env['sequence.number.product'].create(draw_dict)
				else:
					draw_dict = {
						'name': str(partner_obj.partner_code) + ' - ' + format(1, '04'),
						'partner_id':partner_obj.id,
						'product_id':self.product_en.id,
						'drawing_number':vals.get('internal_code_en'),
						'sequence_number': 1,
					}
					part_id = self.env['sequence.number.product'].create(draw_dict)
				if list_of_part:
					draw_dict = {
						'name': str(partner_obj.partner_code) + ' - ' + str(format(max(list_of_part) + 1, '04')),
						'partner_id':partner_obj.id,
						'product_id':self.product_en.id,
						'drawing_number':vals.get('internal_code_en'),
						'sequence_number': max(list_of_part) + 1,
					}
					part_id = self.env['sequence.number.product'].create(draw_dict)
				vals.update({'part_number_product':part_id.id})
		return super(crm_lead_line, self).write(vals)