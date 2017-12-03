# -*- coding: utf-8 -*-

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    auth_id = fields.Char("Auth ID")
    auth_token = fields.Char("Auth Token")
