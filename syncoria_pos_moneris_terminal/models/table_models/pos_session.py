from odoo import models, fields


class PosSession(models.Model):
    _description = "Point of Sale Session"

    _inherit = 'pos.session'
    # endregion Other
