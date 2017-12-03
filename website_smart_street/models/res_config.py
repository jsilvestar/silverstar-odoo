# -*- coding: utf-8 -*-

from odoo import fields, models


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'website.config.settings'

    auth_id = fields.Char(related='website_id.auth_id')
    auth_token = fields.Char(related='website_id.auth_token')

    def set_auth_id_token_key(self):
        self.env['ir.config_parameter'].set_param(
            'auth_id', (self.auth_id or '').strip())
        self.env['ir.config_parameter'].set_param(
            'auth_token', (self.auth_token or '').strip())
