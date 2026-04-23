from odoo import models
from odoo.http import request, BadRequest
from odoo.exceptions import MissingError, AccessDenied


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"
