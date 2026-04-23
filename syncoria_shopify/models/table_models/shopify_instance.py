# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import pprint
from odoo import models, fields, api, _
from odoo.http import request
import requests
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)
class ModelName(models.Model):
    _inherit = 'marketplace.instance'

    apply_tax = fields.Boolean(string='Apply Tax', default=True)

    marketplace_app_id = fields.Integer(string='App ID',default=0)

    marketplace_instance_type = fields.Selection(selection_add=[('shopify', 'Shopify')], default='shopify')

    marketplace_api_key = fields.Char(string='API key')

    marketplace_api_password = fields.Char(string='Password')

    marketplace_secret_key = fields.Char(string='Secret Key')

    marketplace_host = fields.Char(string='Host')

    marketplace_webhook = fields.Boolean(
        string='Use Webhook?',
    )

    default_res_partner_id = fields.Many2one('res.partner', string='Default Contact For Order With No Customer')

    marketplace_is_shopify = fields.Boolean(compute='_compute_is_shopify' )

    @api.depends('marketplace_instance_type')
    def _compute_is_shopify(self):
        for record in self:
            record.marketplace_is_shopify = False
            if record.marketplace_instance_type == 'shopify':
                record.marketplace_is_shopify = True

    marketplace_api_version = fields.Char(
        string='Api Version',
        default="2021-01"
    )

    marketplace_payment_journal_id  = fields.Many2one(
        string='Payment Journal',
        comodel_name='account.journal',
        ondelete='restrict',
    )

    marketplace_refund_journal_id = fields.Many2one(
        string='Refund Journal',
        comodel_name='account.journal',
        ondelete='restrict'
    )

    marketplace_inbound_method_id  = fields.Many2one(
        string='Inbound Payment Method',
        comodel_name='account.payment.method',
        ondelete='restrict',
        domain=[('payment_type','=','inbound')]
    )

    marketplace_outbound_method_id  = fields.Many2one(
        string='Outbound Payment Method',
        comodel_name='account.payment.method',
        ondelete='restrict',
        domain=[('payment_type','=','outbound')]
    )

    refund_discrepancy_account_id = fields.Many2one('account.account', string='Refund Discrepancy Account')

    shopify_payment_method_mappings = fields.One2many('shopify.payment.method.mappings', 'shopify_instance_id', string='Payment method mappings')

    shopify_refund_payment_method_mappings = fields.One2many('shopify.refund.payment.method.mappings', 'shopify_instance_id', string='Refund Payment method mappings')

    shopify_shipping_method_mappings = fields.One2many('shopify.shipping.method.mappings', 'shopify_instance_id', string='Shipping method mappings')

    is_product_create = fields.Boolean(string="Enable New product creation",default=True,help="While fetching the product if enabled new product will be created otherwise only update existing products")

    is_sku = fields.Boolean(default=False)

    delivery_product_id = fields.Many2one('product.product', string="Delivery Product")

    compute_pricelist_price = fields.Boolean(default=True)

    color = fields.Integer(default=10)

    marketplace_count_orders = fields.Integer('Order Count', compute='_compute_count_of_records')

    marketplace_count_products = fields.Integer('Product Count', compute='_compute_count_of_records')

    marketplace_count_customers = fields.Integer('Customer Count', compute='_compute_count_of_records')

    marketplace_database_name = fields.Char('Database Name', compute='_compute_count_of_records')

    marketplace_current_user = fields.Char('Current User', compute='_compute_count_of_records')

    def _compute_count_of_records(self):
        """
        Count of Orders, Products, Customers for dashboard

        :return: None
        """
        for rec in self:
            search_query = [('marketplace_instance_id', '=', rec.id), ('shopify_id', '!=', False)]
            rec.marketplace_database_name = request.session.db
            rec.marketplace_current_user = self.env.user.id
            rec.marketplace_count_orders = rec.env['sale.order'].search_count(search_query)
            rec.marketplace_count_products = rec.env['shopify.product.mappings'].search_count([('shopify_instance_id', '=', rec.id)])
            rec.marketplace_count_customers = rec.env['res.partner'].search_count(search_query)
