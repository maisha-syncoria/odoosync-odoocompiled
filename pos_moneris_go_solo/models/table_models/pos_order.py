from odoo import api, fields, models,_
from odoo.tools import float_compare
from odoo.tools import float_is_zero, float_round, float_repr, float_compare, formatLang

class PosOrder(models.Model):
    _inherit = 'pos.order'

    payment_ids = fields.One2many('pos.payment', 'pos_order_id', inverse='_check_duplicate_payments')

    refund_total = fields.Float(string="Refund Total", compute='_compute_refund_total', store=True)

    total_tip_amount = fields.Float(string='Tip Amount', digits=0, readonly=True, compute='_compute_tip_amount',store=True)

    total_amount_without_tip = fields.Float(string='Total without Tip', digits=0, readonly=True, compute='_compute_tip_amount',store=True)

    @api.depends('payment_ids.is_refund', 'payment_ids.amount')
    def _compute_refund_total(self):
        for order in self:
            refund_sum = abs(sum(payment.amount for payment in order.payment_ids if payment.is_refund))
            order.refund_total = refund_sum

    def _check_duplicate_payments(self):
        print('_check_duplicate_payments', self)
        """Inverse method: Remove duplicate payments for the same bill_number, keeping the latest."""

    @api.depends('amount_total','lines')
    def _compute_tip_amount(self):
        for order in self.search([]):
            tip_product = order.config_id.tip_product_id
            if tip_product:
                tip_lines = order.lines.filtered(lambda line: line.product_id.id == tip_product.id)
                order.total_tip_amount = sum(tip_lines.mapped('price_subtotal_incl'))
                order.total_amount_without_tip = order.amount_total - order.total_tip_amount
