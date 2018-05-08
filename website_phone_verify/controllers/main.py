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
        if data.get('phone'):
            access_key = request.env['ir.config_parameter'].\
                sudo().get_param('phone_access_token')
            numverify_url = 'http://apilayer.net/api/validate'
            data = {
                'access_key': access_key,
                'number': data.get('phone'),
            }
            res = requests.get(numverify_url, params=data)
            response = res.json()
            if response.get('valid') == False:
                error["phone"] = 'error'
                error_message.append(_('Please check your phone number or country code'))
            elif response.get('success') == False:
                error["phone"] = 'error'
                error_message.append(_('please %s') % (response['error']['info'])) 
            return (error, error_message)
        else:
            error["phone"] = 'error'
        return (error, error_message)
