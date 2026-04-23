import requests
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from ...exceptions.MonerisGo import OpenSessionFailed, CloseSessionFailed

_logger = logging.getLogger(__name__)
MONERIS = 'moneris'


class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    is_directly_payment = fields.Boolean('Is Directly Payment')
    # endregion Other
