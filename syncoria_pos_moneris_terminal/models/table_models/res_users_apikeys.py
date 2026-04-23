import time

from odoo import models
from odoo.addons.base.models.res_users import INDEX_SIZE, KEY_CRYPT_CONTEXT

from ...exceptions.ExpireAPIKey import ExpireAPIKey


class APIKeys(models.Model):
    _inherit = 'res.users.apikeys'
