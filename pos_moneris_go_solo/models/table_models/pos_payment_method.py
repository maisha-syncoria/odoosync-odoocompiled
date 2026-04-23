import requests
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from ...exceptions.MonerisGo import OpenSessionFailed, CloseSessionFailed
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)
MONERIS = 'moneris'


class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    is_directly_payment = fields.Boolean('Is Directly Payment')

    moneris_device_id = fields.Many2one("moneris.device", ondelete='restrict',
                                        domain=lambda self: [('journal_id', '=', self.id)], )

    account_id = fields.Many2one(
        string='account',
        comodel_name='omni.account',
        ondelete='restrict',
    )

    moneris_payment_journal_config_ids = fields.One2many('pos.moneris.payment.journal.config', 'pos_payment_id')
    # endregion Other


class PosMonerisPaymentJournalConfig(models.Model):
    _name = 'pos.moneris.payment.journal.config'

    card_name = fields.Char(required=True, copy=False)

    is_other_payment = fields.Boolean(copy=False)

    pos_payment_id = fields.Many2one('pos.payment.method', required=True)

    receivable_account_id = fields.Many2one('account.account', required=True)

    journal_id = fields.Many2one('account.journal', string='Journal', ondelete='cascade', required=True)
