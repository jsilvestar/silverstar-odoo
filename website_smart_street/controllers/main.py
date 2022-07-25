# -*- coding: utf-8 -*-
import requests

from odoo import http, tools, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleAddress(WebsiteSale):
    def checkout_form_validate(self, mode, all_form_values, data):
        res = super(WebsiteSaleAddress, self).\
            checkout_form_validate(mode=mode,
                                   all_form_values=all_form_values,
                                   data=data)
        error = res[0]
        error_message = res[1]
        auth_id = request.env['ir.config_parameter'].\
            sudo().get_param('auth_id')
        auth_token = request.env['ir.config_parameter'].\
            sudo().get_param('auth_token')
        smart_street_url = 'https://us-zipcode.api.smartystreets.com/lookup'
        headers = {
            'Content-Type': 'Content-Type: application/json',
        }
        data = {
            'auth_id': auth_id,
            'auth_token': auth_token,
            'input_id': data.get('partner_id'),
            'street': data.get('street'),
            'state': data.get('state') and data['state'].code or '',
            'zipcode': data.get('zip'),
            
        }
        res = requests.get(smart_street_url, headers=headers, params=data)
        return (error, error_message)
