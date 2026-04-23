import json
import logging
from uuid import uuid4

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessDenied

import requests

_logger = logging.getLogger(__name__)


class PosPayment(models.Model):
    _inherit = "pos.payment"

    pos_payment_transaction = fields.Char('POS Payment Transaction',
                                          help="POS Payment Transaction with payment terminal")

    idempotency_key = fields.Char('Idempotency Key', help='Use for the moneris payment when refunding')

    card_name = fields.Char('Card Name')

    auth_code = fields.Char('Auth Code')

    masked_pan = fields.Char('Masked Pan')

    payment_terminal_order_reference = fields.Char('Order Id')

    payment_terminal_transaction_id = fields.Char('Moneris Go Transaction Id')

    tender_type = fields.Char('Tender Type')

    refunded_idempotency_key = fields.Char('Refunded Idempotency Key', help='Idempotency Key has been used to refund')
    # endregion Other
