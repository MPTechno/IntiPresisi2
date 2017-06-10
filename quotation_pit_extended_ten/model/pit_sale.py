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
		print "##########",self
		self.write({'state':'sent'})
		return True