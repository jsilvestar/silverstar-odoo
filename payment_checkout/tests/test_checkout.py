# -*- coding: utf-8 -*-

import odoo
from odoo import fields
from odoo.addons.payment.tests.common import PaymentAcquirerCommon
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.tools import mute_logger


@odoo.tests.common.at_install(False)
@odoo.tests.common.post_install(True)
class CheckoutCommon(PaymentAcquirerCommon):

    def setUp(self):
        super(CheckoutCommon, self).setUp()
        self.checkout = self.env.ref('payment.payment_acquirer_checkout')


@odoo.tests.common.at_install(False)
@odoo.tests.common.post_install(True)
class CheckoutTest(CheckoutCommon):

    def test_10_checkout_form_render(self):
        self.assertEqual(self.checkout.environment, 'test',
                         'test without test environment')

        self.checkout.write({
            'secret_key': 'sk_test_07f41eeb-a042-483e-9c5c-8572de332a94',
            'publishable_key': 'pk_test_ecd1351e-cba9-4a42-842f-9fc19649f0c6',
        })
        # ----------------------------------------
        # Test: button direct rendering
        # ----------------------------------------
        form_values = {
            'secret_key': self.checkout.secret_key,
            'publishable_key': self.checkout.publishable_key,
            'customerName': 'Silverstar',
            'email': 'admin.buyer@example.com',
            'amount': 1000,
            'reference': 'SO555',
            'currency': 'EUR',
            'currency_id': self.currency_euro.id,
            "billingDetails": {
                "addressLine1": 'Huge Street 2/543',
                "postcode": '1000',
                "country": 'Belgium',
                "city":  'bruges',
                "state": 'Boat',
                "phone": {
                  "number": '12345679525',
                }
            }
        }

        # render the button
        res = self.checkout.render('SO555', 1000, self.currency_euro.id,
                                   values=self.buyer_values)
        post_url = "https://cdn.checkout.com/sandbox/js/checkout.js"
        email = "norbert.buyer@example.com"
        # check form result
        if "https://cdn.checkout.com/sandbox/js/checkout.js" in res[0]:
            self.assertEqual(post_url,
                             'https://cdn.checkout.com/sandbox/js/checkout.js',
                             'Checkout: wrong form POST url')
        # Generated and received
        if email in res[0]:
            self.assertEqual(
                email, form_values.get('email'),
                'Checkout: wrong value for input %s: received %s instead of %s'
                % (email, email, form_values.get('email'))
            )

    def test_20_checkout_form_management(self):
        self.assertEqual(self.checkout.environment, 'test',
                         'test without test environment')

        # typical data posted by Checkout after client has successfully paid
        checkout_post_data = {
            u'authCode': u'865239',
            u'autoCapTime': 24.0,
            u'autoCapture': u'Y',
            u'created': u'2018-04-27T14:23:39Z',
            u'currency': u'EUR',
            u'customerIp': u'202.131.126.141',
            u'customerPaymentPlans': None,
            u'description': None,
            u'email': u'admin@yourcompany.example.com',
            u'id': u'charge_test_FEF849AE745M7398B7F0',
            u'isCascaded': False,
            u'liveMode': False,
            u'metadata': {u'order': u'SO555'},
            u'products': [],
            u'responseAdvancedInfo': u'Approved',
            u'responseCode': u'10000',
            u'responseMessage': u'Approved',
            u'riskCheck': True,
            u'card': {u'avsCheck': u'S',
                      u'billingDetails': {
                          u'addressLine1': None,
                          u'addressLine2': None,
                          u'city': None,
                          u'country': None,
                          u'phone': {},
                          u'postcode': None,
                          u'state': None},
                      u'bin': u'424242',
                      u'customerId': u'cust_C4F82831-4108-4359-B3FD-DC5F1CC5CF20',
                      u'cvvCheck': u'Y',
                      u'expiryMonth': u'06',
                      u'expiryYear': u'2018',
                      u'fingerprint': u'F639CAB2745BEE4140BF86DF6B6D6E255C5945AAC3788D923FA047EA4C208622',
                      u'id': u'card_40CADEC4-2739-4774-BE7B-A1D17713BC03',
                      u'last4': u'4242',
                      u'name': None,
                      u'paymentMethod': u'Visa'},
                      u'chargeMode': 1,
                      u'shippingDetails': {u'addressLine1': None,
                                           u'addressLine2': None,
                                           u'city': None,
                                           u'country': None,
                                           u'phone': {},
                                           u'postcode': None,
                                           u'state': None},
                      u'status': u'Authorised',
                      u'trackId': None,
                      u'transactionIndicator': 1,
                      u'udf1': None,
                      u'udf2': None,
                      u'udf3': None,
                      u'udf4': None,
                      u'udf5': None,
                      u'value': 1000
            }

        # should raise error about unknown tx
        with self.assertRaises(ValidationError):
            self.env['payment.transaction'].form_feedback(checkout_post_data,
                                                          'checkout')

        tx = self.env['payment.transaction'].create({
            'amount': 1000,
            'acquirer_id': self.checkout.id,
            'currency_id': self.currency_euro.id,
            'reference': 'SO555',
            'partner_name': 'Silverstar',
            'partner_country_id': self.country_france.id,
            'acquirer_reference': checkout_post_data.get('id')
        })
#        validate it
        tx.form_feedback(checkout_post_data, 'checkout')

        self.assertEqual(tx.state, 'done', 'Checkout: validation did not put tx into done state')
        self.assertEqual(tx.acquirer_reference, checkout_post_data.get('id'), 'Checkout: validation did not update tx payid')
#       reset tx
        tx.write({'state': 'draft', 'date_validate': False, 'acquirer_reference': False})
        # simulate an error
        checkout_post_data['responseCode'] = u'3000345'
        tx.form_feedback(checkout_post_data, 'checkout')
#         # check state
        self.assertEqual(tx.state, 'error', 'Checkout: erroneous validation did not put tx into error state')
