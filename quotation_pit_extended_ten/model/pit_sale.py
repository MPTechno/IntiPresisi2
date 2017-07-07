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

class ProductType(models.Model):
    _name = 'product.type'    
    name = fields.Char('Name', size=256)

class res_users(models.Model):
	_inherit = 'res.users'

	sales_person_b = fields.Boolean('Sales Person')
	sales_coordinator_b = fields.Boolean('Sales Coordinator')
	technical_support_b = fields.Boolean('Technical Support')
	director_b = fields.Boolean('Director')
	president_director_b = fields.Boolean('President Director')
	admin_b = fields.Boolean('Admin')
	sales_supervisor_b = fields.Boolean('Sales Supervisor')

class res_company(models.Model):
	_inherit = 'res.company'

	sign_line_text = fields.Char('Sign Line Name')


class sale_order(models.Model):
	_inherit = 'sale.order'
	
	@api.multi
	def action_quotation_send_stage(self):
		self.write({'state':'sent'})
		return True

class part_code_pit(models.Model):
	_name = 'part.code.pit'

	name = fields.Char('Part Code')

class product_group_pit(models.Model):
	_name = 'product.group.pit'

	name = fields.Char('Product Group')

class product_template(models.Model):
	_inherit = 'product.template'

	workpiece_grade = fields.Many2one('workpiece.grade','Workpiece Grade')
	kind_of_machine = fields.Many2one('kind.of.machine','Kind of Machine')
	part_code = fields.Many2one('part.code.pit','Part Code')
	product_group = fields.Many2one('product.group.pit','Product Group')
	type_id   = fields.Many2one('product.type', 'Product Type')
	workpiece_material = fields.Many2one('workpiece.material','Workpiece Material')
	coating_en = fields.Many2one('coating.enquiry','Coating')
	pricing_date = fields.Date('Pricing Date')
	pro_remark = fields.Text('Remarks')

class crm_stage(models.Model):
	_inherit = 'crm.stage'

	stage_known = fields.Integer('Stage Num')

    
class product_product(models.Model):
	_inherit = 'product.product'

	item_product_ids = fields.One2many('product.pricelist.item', 'product_id', 'Pricelist Items')


    

    
