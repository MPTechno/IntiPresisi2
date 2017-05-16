# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class res_partner(models.Model):
	_inherit = 'res.partner'
	
	@api.model
	def name_search(self, name, args=None, operator='ilike', limit=100):
		args = args or []
		recs = self.browse()
		print "\n\n=========self._context=",self._context
		if self._context.has_key('is_contact'):
			if self._context.has_key('partner_id') and self._context.get('partner_id'):
				res_partner_id = self.env['res.partner'].browse(self._context.get('partner_id'))
				print "\n\n=========",res_partner_id.child_ids
				recs = res_partner_id.child_ids
				print "\n\nRECS==",recs
		else:
			recs = self.search([('name', operator, name)] + args, limit=limit)
		return recs.name_get()

