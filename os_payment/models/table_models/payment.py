# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _

class Paymentprovider(models.Model):
    _inherit = 'payment.provider'

    account_id = fields.Many2one(
        string='account',
        comodel_name='omni.account',
        ondelete='restrict',
    )

    test_transaction_schedule_id = fields.Char(string="Test Transaction Schedule ID")

    token = fields.Char(copy=False)

    omnisync_active = fields.Boolean(
        string='Active',
        compute='_compute_omnisync_active')

    def _compute_omnisync_active(self):
        for record in self:
            record.omnisync_active = False


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    is_clik2pay_sync_button_visible = fields.Boolean(compute='_check_is_clik2pay_sync_visible')

    resolvepay_payment_date = fields.Char(string="Resolve Pay payment datetime")

    rp_payout_transaction_id = fields.Char(string="Resolve Pay Payout Transaction Id")

    rp_payout_id = fields.Char(string="Resolve Pay Payout Id")

    rp_payout_transaction_type = fields.Selection(
        selection=[
            ('advance', 'advance'),
            ('payment', 'payment'),
            ('refund', 'refund'),
            ('monthly_fee', 'monthly_fee'),
            ('annual_fee', 'annual_fee'),
            ('non_advanced_invoice_fee', 'non_advanced_invoice_fee'),
            ('merchant_payment', 'merchant_payment'),
            ('mdr_extension', 'mdr_extension'),
            ('credit_note', 'credit_note'),
        ],
        string='Resolve Pay Transaction Type',
    )

    rp_payout_transaction_amount_gross = fields.Float('amount_gross')

    rp_payout_transaction_amount_fee = fields.Float('amount_fee')

    rp_payout_transaction_amount_net = fields.Float('amount_net')
