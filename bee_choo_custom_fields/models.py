# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools import amount_to_text_en
from openerp.osv import fields, osv

class Sale_Order(osv.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self, cr, uid, order, lines, context=None):

        if context is None:
            context = {}
        res = super(Sale_Order,self)._prepare_invoice(cr, uid, order, lines, context)
        res['schedule_new_date'] = order.schedule_new_date
        return res

class stock_move(osv.osv):
    _inherit = "stock.move"

    def _picking_assign(self, cr, uid, move_ids, procurement_group, location_from, location_to, context=None):

        # Call super function
        res = super(stock_move, self)._picking_assign(cr, uid, move_ids, procurement_group, location_from, location_to, context=context)

        # Get move id
        move = self.browse(cr, uid, move_ids, context=context)[0]

        # Get the values from the move
        order_obj = self.pool.get("sale.order")
        order_id = order_obj.search(cr, uid, [('name','=', move.origin)], context=context)
        vals = order_obj.read(cr, uid, order_id, ['schedule_new_date'])

        # Get client reference from move values
        for value in vals:
            if value.has_key('schedule_new_date'):
                order_ref = value['schedule_new_date']
        # If exists client reference update stock picking client_order_ref field
        if order_ref:
            stock_pick_obj = self.pool.get("stock.picking")
            stock_pick_id = stock_pick_obj.search(cr, uid, [('origin', '=', move.origin)], context=context)
            stock_pick_obj.write(cr, uid, stock_pick_id, {'min_date': order_ref}, context=context)
        return

from openerp import models, fields, api
from openerp.tools import amount_to_text_en, english_number


def amount_to_text_fixed(number, currency):
    number = '%.2f' % number
    units_name = currency
    list = str(number).split('.')
    start_word = english_number(int(list[0]))
    end_word = english_number(int(list[1]))
    cents_number = int(list[1])
    cents_name = (cents_number > 1) and 'Cents' or 'Cent'
    return ' '.join(filter(None, [units_name, start_word, (start_word or units_name) and (end_word or cents_name) and 'and', end_word, cents_name]))

class bee_choo_product_custom_fields(models.Model):
    _inherit = "product.template"

    country_of_origin = fields.Many2one(comodel_name="res.country", string="Country of Origin", required=False)
    hs_code = fields.Char(string="HS Code", required=False)
    notification_no = fields.Char(string="Notification Number", required=False)
    optimum_no = fields.Char(string="Optimum Number", required=False)
    packing_size = fields.Char(string="Packing Size")


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    attention = fields.Many2one('res.users', string="Attention", related='partner_id.user_id')
    attn_tel = fields.Char(string="Tel", related='partner_id.phone')
    attn_email = fields.Char(string="Email", related='partner_id.email')
    prepared_by = fields.Char(string="Prepared By")

    amount_to_text = fields.Char(compute='_amount_in_words', string='In Words', help="The amount in words")

    @api.depends('amount_total')
    @api.one
    def _amount_in_words(self):
        if self.partner_id.lang == 'en_US':
            if self.currency_id.spelling :
                currency = self.currency_id.spelling
            else:
                currency = self.currency_id.name
            self.amount_to_text = amount_to_text_fixed(self.amount_total, currency=currency)

PurchaseOrder()


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    attention = fields.Char(string="Attention")
    attn_tel = fields.Char(string="Tel")
    amount_to_text = fields.Char(compute='_amount_in_words', string='In Words', help="The amount in words")
    schedule_new_date = fields.Date('Schedule Date')

    @api.depends('amount_total')
    @api.one
    def _amount_in_words(self):
        if self.partner_id.lang == 'en_US':
            if self.pricelist_id.currency_id.spelling:
                currency = self.pricelist_id.currency_id.spelling
            else:
                currency = self.pricelist_id.currency_id.name
            self.amount_to_text = amount_to_text_fixed(self.amount_total, currency=currency)

    @api.multi
    def get_data(self):
        product_list = []
        for sale in self.order_line:
            vals = {}
            vals['country_origin'] = sale.product_id.country_of_origin.name
            vals['description'] = sale.product_id.name
            vals['qty']= int(sale.product_uom_qty)
            vals['net_wt'] = int(sale.product_id.weight_net)
            vals['package'] = int(sale.product_packaging.qty)
            if sale.product_packaging.qty:
                vals['carton_ref'] = '1 ~ ' + str(int(sale.product_packaging.qty))
            else:
                vals['carton_ref'] = ''
            product_list.append(vals)
        return product_list

    @api.multi
    def get_total_data(self):
        total_list = []
        qty, weight, pack = 0.0,0.0,0.0
        for sale in self.order_line:
            qty += sale.product_uom_qty
            weight += sale.product_id.weight_net
            pack += sale.product_packaging.qty
        vals = {}
        vals['qty']= int(qty)
        vals['net_wt'] = int(weight)
        vals['package'] = int(pack)
        total_list.append(vals)
        return total_list

    @api.multi
    def get_pallet(self):
        packing_list = []
        for sale in self.order_line:
            vals = {}
            if sale.product_id and sale.product_id.packing_size:
                vals['packing_size']= sale.product_id.packing_size + ' ( Item '+ '1 ~ ' + str(int(sale.product_packaging.qty)) + ' )'
            else:
                vals['packing_size'] = ''
            packing_list.append(vals)
        return packing_list



SaleOrder()

class CustomAccountInvoice(models.Model):
    _inherit = 'account.invoice'

    invoice_default_number = fields.Char('Invoice Number')
    amount_to_text = fields.Char(compute='_amount_in_words', string='In Words', help="The amount in words")
    name = fields.Char(string='Reference/Description', index=True, readonly=False)
    schedule_new_date = fields.Date('Schedule Date')

    @api.model
    def create(self, vals):
        res = super(CustomAccountInvoice, self).create(vals)
        picking_obj = self.env['stock.picking']
        parent_id = self.search([('number', '=', res.origin)], limit=1)
        if res.type == 'out_refund' and res.origin and parent_id and len(parent_id) >0:
            res.write({'invoice_default_number': self.invoice_default_number})
        else:
            if res and res.origin and res.reference:
                deli_order_id = picking_obj.search([('name','=', res.origin),('origin','=',res.reference)])
                if deli_order_id and len(deli_order_id) > 0:
                    for record in deli_order_id:
                        res.write({'invoice_default_number': record.invoice_default_number})
            if not res.invoice_default_number:
                invoice_default_number = self.env['ir.sequence'].get('invoice.number.default')
                res.write({'invoice_default_number': invoice_default_number})
        return res

    @api.depends('amount_total')
    @api.one
    def _amount_in_words(self):
        if self.partner_id.lang == 'en_US':
            if self.currency_id.spelling:
                currency = self.currency_id.spelling
            else:
                currency = self.currency_id.name
            self.amount_to_text = amount_to_text_fixed(self.amount_total, currency=currency)


class PickingQuantity(models.Model):

   _inherit = 'stock.move'
   
   do_quantity = fields.Float(string='Quantity',
                               store=True,
                               related='product_uos_qty')


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    @api.depends('move_lines.do_quantity')
    def _total_qty(self):
        currentqty = 0
        for move_line in self.move_lines:
            currentqty = currentqty + move_line.do_quantity

        self.qty_total = currentqty

    qty_total = fields.Float(compute='_total_qty', string='Total Quantity')

    order_ids = fields.One2many('sale.order', string='Orders', compute='_get_order_ids')
    payment_term = fields.Many2one('account.payment.term', string='Payment Term', compute='_get_payment_term')
    attention = fields.Many2one('res.users', related='partner_id.user_id', string="Attention")
    attn_tel = fields.Char(string="Tel", related='partner_id.phone')
    issued_by = fields.Char(string="Issued By")
    invoice_default_number = fields.Char('Invoice Number')


    @api.one
    def _get_order_ids(self):
        if self.group_id and self.group_id.id:
            self.order_ids = self.env['sale.order'].search([('procurement_group_id', '=', self.group_id.id)])

    @api.model
    def create(self, vals):
        stock_picking_id = super(StockPicking, self).create(vals)
        #if not vals.get('origin'):
    	invoice_default_number = self.env['ir.sequence'].get('invoice.number.default')
    	stock_picking_id.write({'invoice_default_number':invoice_default_number})
        return stock_picking_id
    
    @api.one
    def _get_payment_term(self):
        for order in self.order_ids:
            self.payment_term = order.payment_term

StockPicking()

class res_currency(models.Model):
    _inherit = 'res.currency'

    spelling = fields.Char('Spelling Name')


class res_partner(models.Model):
    _inherit = 'res.partner'

    attention = fields.Char('Attention')

