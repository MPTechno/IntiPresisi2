# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
import re

class crm_askcode_partner(osv.osv_memory):
    _name = 'crm.askcode.partner'
    _description = 'Lead To Partner'

    _columns = {
        'code_partner':fields.char('Code',required=True),
    }

    def convert_to_part(self, cr, uid, ids,context=None):
        print "??????????????",ids,context
        if context.get('active_id'):
            w = self.browse(cr, uid, ids, context=context)
            print ">>>>>>>>>>",w , w.code_partner
            lead_obje = self.pool.get('crm.lead').browse(cr, uid, context.get('active_id'), context=context)
            partner = self.pool.get('res.partner')
            vals_dict = {}
            if lead_obje.partner_name:
                vals_dict = {
                    'name': lead_obje.partner_name,
                    'phone':lead_obje.phone,
                    'user_id': uid,
                    'partner_code':w.code_partner,
                    'email':lead_obje.email_from,
                    'street':lead_obje.street,
                    'street2':lead_obje.street2,
                    'country_id':lead_obje.country_id.id,
                    'zip':lead_obje.zip,
                    'is_company': False,
                    'type': 'contact',
                    'customer':True,
                    'supplier':False,
                }
                partner_id = partner.create(cr, uid, vals_dict, context=context)
                self.pool.get('crm.lead').write(cr, uid, context.get('active_id'), {'partner_id':partner_id},context=context)
                models_data = self.pool.get('ir.model.data')

                # Get opportunity views
                dummy, form_view = models_data.get_object_reference(cr, uid, 'base', 'view_partner_form')
                dummy, tree_view = models_data.get_object_reference(cr, uid, 'base', 'view_partner_tree')
                return {
                    'name': _('Accounts'),
                    'view_type': 'form',
                    'view_mode': 'tree, form',
                    'res_model': 'res.partner',
                    'res_id': int(partner_id),
                    'view_id': False,
                    'views': [(form_view or False, 'form'),
                              (tree_view or False, 'tree'), (False, 'kanban'),
                              (False, 'calendar'), (False, 'graph')],
                    'type': 'ir.actions.act_window',
                    'context': {}
                }