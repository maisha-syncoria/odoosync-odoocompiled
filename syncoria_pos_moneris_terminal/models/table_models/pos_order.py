from odoo import api, fields, models
from odoo.tools import float_compare


class PosOrder(models.Model):
    _inherit = 'pos.order'
    # endregion Other
