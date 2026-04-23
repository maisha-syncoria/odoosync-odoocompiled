# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _

class PosPaymentAcquirer(models.Model):
    _inherit = 'pos.payment.method'

    account_id = fields.Many2one(
        string='account',
        comodel_name='omni.account',
        ondelete='restrict',
    )

    token = fields.Char()

    omnisync_active = fields.Boolean(
        string='Odoosync Active',
        )

    enable_card_wise_journal = fields.Boolean(string="Enable Card-wise Journal")

    test_with_demo_response = fields.Boolean(string="Test With Demo Response")

    demo_card_name = fields.Char(string="Card Name")

    # def _compute_omnisync_active(self):
    #     for record in self:
    #         record.omnisync_active = False
