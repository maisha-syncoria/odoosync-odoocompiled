from odoo import fields, models


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    clover_checkout_card_brand = fields.Char('Clover Checkout Card Brand')

    clover_checkout_card_type = fields.Char('Clover Checkout Card Type')
