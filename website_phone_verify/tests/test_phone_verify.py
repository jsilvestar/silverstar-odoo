# -*- coding: utf-8 -*-
import requests

import odoo
from odoo.tests.common import TransactionCase


class TestPhoneVerify(TransactionCase):
    def test_validate_phone_verify(self):
        numverify_url = 'http://apilayer.net/api/validate'
        data = {
            'access_key': 'bd6cf312bc7800bc1b82f66cbed78ebc',
            'number': '919047623077',
        }
        res = requests.get(numverify_url, params=data)
        response = res.json()
        self.assertEqual(response['valid'], True, 'Phone Verified!')
