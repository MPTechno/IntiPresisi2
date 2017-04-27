# -*- coding: utf-8 -*-
from openerp import http

# class BeeChooCustomFields(http.Controller):
#     @http.route('/bee_choo_custom_fields/bee_choo_custom_fields/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bee_choo_custom_fields/bee_choo_custom_fields/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bee_choo_custom_fields.listing', {
#             'root': '/bee_choo_custom_fields/bee_choo_custom_fields',
#             'objects': http.request.env['bee_choo_custom_fields.bee_choo_custom_fields'].search([]),
#         })

#     @http.route('/bee_choo_custom_fields/bee_choo_custom_fields/objects/<model("bee_choo_custom_fields.bee_choo_custom_fields"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bee_choo_custom_fields.object', {
#             'object': obj
#         })