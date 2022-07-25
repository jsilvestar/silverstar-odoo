# -*- coding: utf-8 -*-

from smartystreets import Client
import odoo

from odoo.tests.common import TransactionCase


class TestAddress(TransactionCase):
    def test_validate_smart_street(self):
        ResConfig = self.env['website'].browse(1)
        ResConfig.create({
            'auth_id': '8d053a90-0b0d-6664-6222-6a731f45711f',
            'auth_token': 'stPVNKl6sYnZy49SuDUc',
        })
        client = Client(ResConfig.auth_id, ResConfig.auth_token)
        address = client.street_address({
                'input_id': '1',
                'street': '3301 South Greenfield Rd',
                'zipcode': '85297',
        })
        self.assertEqual(address.confirmed, True, 'Verification Success!')
        address = client.street_address({
                'input_id': '2',
                'street': 'silverstar',
                'zipcode': '12212',
            })
        self.assertEqual(
            address, None,
            'Verification Failed: Please check Street and zip code!')
