from odoo import api, fields, models, _, Command
from odoo.tools import float_compare

class PosSession(models.Model):
    _description = "Point of Sale Session"

    _inherit = 'pos.session'
