# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2014 Agent ERP GmbH
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the impliedaa warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#
##############################################################################

from openerp.osv import osv
from openerp.osv import fields
from openerp.addons.decimal_precision import decimal_precision as dp
from networkx import nx
import re
import logging
from openerp import api

_logger = logging.getLogger(__name__)


class crm_lead(osv.osv):
    _inherit = 'crm.lead'
    _columns = {
        'km': fields.char(
            'KM',
        ),
    }

    def show_google_map(self, cr, uid, ids, context):
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'google_map_locator', 'view_crm_lead_map')
        view_id = view_ref and view_ref[1] or False,
        return {
        'type': 'ir.actions.act_window',
        'name': 'Crm Lead',
        'res_model': 'crm.lead',
        'res_id': ids[0],
        'view_id': view_id,
        'view_type': 'form',
        'view_mode': 'form',
        'target': 'new',
        'nodestroy': True,
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
