# -*- coding: utf-8 -*-

from odoo import fields, models


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'website.config.settings'

    phone_access_token = fields.Char(
        related='website_id.phone_access_token'
    )

    def set_phone_access_token(self):
        self.env['ir.config_parameter'].set_param(
            'phone_access_token', (self.phone_access_token or '').strip())
