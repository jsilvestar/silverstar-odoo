# -*- coding: utf-8 -*-

from smartystreets import Client

from odoo import fields, models


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'website.config.settings'

    auth_id = fields.Char(related='website_id.auth_id')
    auth_token = fields.Char(related='website_id.auth_token')
