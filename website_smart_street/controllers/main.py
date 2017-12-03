# -*- coding: utf-8 -*-
    
import json
from smartystreets import Client

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
        api = request.env['website.config.settings'].search([],
                                                            order="id desc",
                                                            limit=1)
        if api.auth_id and api.auth_token:
            client = Client(api.auth_id, api.auth_token)
            state_id = data.get('state_id')
            if state_id:
                state = request.env['res.country.state'].sudo().browse(
                    (int(data.get('state_id'))))
                address = client.street_address({
                    'input_id': data.get('partner_id'),
                    'street': data.get('street'),
                    'city': data.get('city'),
                    'state': state.name,
                    'zipcode': data.get('zip'),
                })
            if address is None:
                error["city"] = 'error'
                error["zip"] = 'error'
                error_message.append(_('Please check city and zip code!'))
        else:
            error["name"] = 'error'
            error_message.append(_('Please Configure API!'))
        return (error, error_message)

    @http.route('/phone/check', type='http', auth='public', methods=['GET', 'POST'])
    def PhoneChange2(self, **kw):
        print 'KKKKKKKKKKKKKKKKKKKKKKKKKKK', kw
        result = []
        if kw:
            result.append({'res': kw})
        return json.dumps(result)
