# -*- coding: utf-8 -*-
import logging
import pprint
import werkzeug

import requests
import json

from odoo.http import request
from odoo import http

_logger = logging.getLogger(__name__)


class CheckOutController(http.Controller):

    @http.route('/payment/checkout/create_charge', type='json', auth="public")
    def checkout_success(self, **post):
        """ Create a payment transaction
        Expects the result from the user input from checkout.js popup"""
        TX = request.env['payment.transaction']
        tx = None
        if post.get('tx_ref'):
            tx = TX.sudo().search([('reference', '=', post['tx_ref'])])
        if not tx:
            tx_id = (post.get('tx_ref') or request.session.get(
                'sale_transaction_id') or request.session.get(
                    'website_payment_tx_id'))
            tx = TX.sudo().browse(int(tx_id))
        if not tx:
            raise werkzeug.exceptions.NotFound()
        url = post.get('tx_url')
        headers = {
            'Authorization': post.get('secret_key'),
            'Content-Type': 'application/json;charset=UTF-8',
        }
        data = {
            "autoCapTime": "24",
            "autoCapture": "Y",
            "chargeMode": 1,
            "email": post.get('email'),
            "customerName": post.get('customerName'),
            "value": post.get('amount'),
            "currency": post.get('currency'),
            "trackId": post.get('order_no'),
            "transactionIndicator": "1",
            "customerIp": requests.get('https://l2.io/ip').text,
            "cardToken": post.get('cardtoken'),
            "card": {
                'billingDetails': post.get('billingDetails'),
            },
            "metadata": {
                "order": post.get('tx_ref'),
            },
        }
        payload = json.dumps(data)
        res = requests.post(url, headers=headers, data=payload)
        response = res.json()
        _logger.info('Checkout : entering form_feedback with post data %s',
                     pprint.pformat(response))
        if response:
            request.env['payment.transaction'].sudo().with_context(
                lang=None).form_feedback(response, 'checkout')
        return post.get('return_url')
