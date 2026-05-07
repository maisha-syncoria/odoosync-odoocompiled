# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from datetime import datetime
from odoo import api, models, fields, _
from odoo.exceptions import UserError
from .canpost_request import CanadaPostRequest
from odoo.tools import pdf
from odoo.addons.odoosync_base.utils.app_delivery import AppDelivery

import logging
import json

_logger = logging.getLogger(__name__)


# from odoo.service import common
# version_info = common.exp_version()
# server_serie = version_info.get('server_serie')


def _convert_weight(weight, unit='KG'):
    ''' Convert picking weight (always expressed in KG) into the specified unit '''
    if unit != False:
        if unit.upper() == 'KG':
            return weight
        elif unit.upper() == 'LB':
            return round(weight / 0.45359237, 2)
        else:
            raise ValueError
    else:
        raise ValueError


class CanadapostServiceType(models.Model):
    _name = "canadapost.service.code"

    _description = "Canada Post Service Type"

    name = fields.Char(required=True)

    code = fields.Char(required=True)


class CanadapostOptionType(models.Model):
    _name = "canadapost.option.type"

    _description = "Canada Post Option Type"

    name = fields.Char(required=True)

    code = fields.Char(required=True)


class CanadapostPaymentMethod(models.Model):
    _name = "canadapost.payment.method"

    _description = "Canada Post Payment Method"

    name = fields.Char(required=True)


class Providercanadapost(models.Model):
    _inherit = 'delivery.carrier'

    @api.model
    def _get_defaultPackage(self):
        try:
            package_id = self.env.ref("os_delivery.cnpost_packaging_YOUR_PACKAGING").id
        except:
            package_id = None
        return package_id

    @api.model
    def _get_defaultService(self):
        try:
            service_id = self.env.ref("os_delivery.domrp").id
        except:
            service_id = None
        return service_id

    def _domain_cn_service(self):
        return [(["code","=ilike","DOM%"])]

    delivery_type = fields.Selection(selection_add=[('canadapost', ("Canada Post"))],
                                     ondelete={'canadapost': lambda recs: recs.write(
                                         {'delivery_type': 'fixed', 'fixed_price': 0})})

    canadapost_developer_username = fields.Char(
        string="Developer Username", groups="base.group_system")

    canadapost_developer_password = fields.Char(
        string="Developer Password", groups="base.group_system")

    canadapost_production_username = fields.Char(
        string="Production Username", groups="base.group_system")

    canadapost_production_password = fields.Char(
        string="Production Password", groups="base.group_system")

    canadapost_service_code = fields.Many2one(string="Service Type", comodel_name="canadapost.service.code",
                                              ondelete='set null', default=_get_defaultService)

    canadapost_return_service_code = fields.Many2one(string="Return Service Type", comodel_name="canadapost.service.code",
                                              domain=_domain_cn_service,ondelete='set null', default=_get_defaultService)

    canadapost_default_packaging_id = fields.Many2one('stock.package.type', string="Canada-post Default Package Type",
                                                      default=_get_defaultPackage)

    canadapost_weight_unit = fields.Selection(selection=[('kg', ('KG')), ('lb', ('LB'))],
                                              string="Package Weight Unit", default='kg', required=True)

    canadapost_distance_unit = fields.Selection(selection=[('in', ('IN')), ('cm', ('CM'))],
                                                string="Package Dimension Unit", default='cm', required=True)

    canadapost_option_type = fields.Many2many(
        string="Options", comodel_name="canadapost.option.type")

    canadapost_nondelivery_handling = fields.Selection(selection=[
        ('RASE', ('Return at Sender’s Expense')),
        ('RTS', ('Return to Sender')),
        ('ABAN', ('Abandon'))],
        string="Non-delivery Handling", default="RTS")

    canadapost_customer_type = fields.Selection(selection=[(
        'commercial', 'Commercial'), ('counter', 'Counter')], string="Canada-post Customer Type", default='counter')

    canadapost_customer_number = fields.Char(string="Canada-post Customer Number")

    canadapost_contract_id = fields.Char(string="Contract ID")

    canadapost_promo_code = fields.Char(string="Canada-post Promo Code")

    canadapost_payment_method = fields.Many2one(string="Payment Method", comodel_name="canadapost.payment.method",
                                                ondelete='set null')

    canadapost_mailed_on_behalf_of = fields.Char(string="Mailed on Behalf of")

    canadapost_label_image_format = fields.Selection(selection=[('pdf', ('PDF')), ('zpl', ('ZPL'))],
                                                     string="Label Format", default='pdf')

    canadapost_void_shipment = fields.Boolean(string='Canada-post Void Shipment')

    canadapost_pickup_indicator = fields.Selection(selection=[('pickup', (
        'Pick-up')), ('deposit', ('Deposit'))], string='Pick Indicator', default='pickup')

    canadapost_country_flag = fields.Boolean(default=False)
