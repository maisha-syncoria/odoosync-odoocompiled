from odoo import models, fields, api, _
from odoo.exceptions import UserError


class OmniAccount(models.Model):
    _inherit = 'omni.account'
