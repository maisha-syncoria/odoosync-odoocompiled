from odoo import models, api, _


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'
