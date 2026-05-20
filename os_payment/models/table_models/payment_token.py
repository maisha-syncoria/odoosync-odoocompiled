# -*- coding: utf-8 -*-

from odoo import _, api, models
from odoo.exceptions import AccessError


class PaymentToken(models.Model):
    _inherit = 'payment.token'


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'
