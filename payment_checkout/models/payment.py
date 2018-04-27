# -*- coding: utf-8 -*-
import logging

from odoo import _, api, fields, models
from odoo.addons.payment.models.payment_acquirer import ValidationError

_logger = logging.getLogger(__name__)


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[
        ('checkout', 'Checkout')
    ])
    secret_key = fields.Char('Secret Key')
    publishable_key = fields.Char('Publishable Key')

    @api.multi
    def _get_checkout_urls(self, environment):
        """ Checkout URLs"""
        if environment == 'prod':
            return {
                'checkout_form_url':
                'https://api2.checkout.com/v2/charges/token'
            }
        else:
            return {
                'checkout_form_url':
                'https://sandbox.checkout.com/api2/v2/charges/token'
            }

    @api.multi
    def checkout_get_form_action_url(self):
        self.ensure_one()
        return self._get_checkout_urls(self.environment)['checkout_form_url']

    @api.multi
    def checkout_form_generate_values(self, values):
        self.ensure_one()
        checkout_tx_values = dict(values)
        checkout_tx_values.update({
            'email': values.get('partner_email'),
            "customerName": values.get('partner_name'),
            'tx_url': self.checkout_get_form_action_url(),
            'secret_key': self.secret_key,
            'publishable_key': self.publishable_key,
            'amount': values.get('amount'),
            'reference': str(values.get('reference')),
            'currency': values.get('currency') and values.get(
                'currency').name or '',
            'currency_id': values.get('currency') and values.get(
                'currency').id or '',
            "billingDetails": {
                "addressLine1": values.get("billing_partner_address"),
                "postcode": values.get('billing_partner_zip'),
                "country": values.get('billing_partner_country') and
                values.get('billing_partner_country').name or '',
                "city":  values.get('billing_partner_city'),
                "state": values.get('billing_partner_state') and
                values['billing_partner_state'].code or '',
                "phone": {
                  "number": values.get('billing_partner_phone'),
                }
            },
        })
        return checkout_tx_values


class PaymentTransactionCheckout(models.Model):
    _inherit = 'payment.transaction'

    _checkout_valid_tx_status = [10000]
    _checkout_pending_tx_status = [20000, 20000, 10100, 10200]
    _checkout_cancel_tx_status = [30004, 30007]

    @api.model
    def _checkout_form_get_tx_from_data(self, data):
        """ Given a data dict coming from checkout, verify it and find the related
        transaction record. """
        reference = data.get('metadata', {}).get('order')
        if not reference:
            checkout_error = data.get('error', {}).get('message', '')
            _logger.error(
                'Checkout: invalid reply received from checkout API, looks '
                'like the transaction failed. (error: %s)', checkout_error or
                'n/a')
            error_msg = _(
                "We're sorry to report that the transaction has failed.")
            if checkout_error:
                error_msg += " " + (_(
                    "checkout following info about the problem: '%s'") %
                                    checkout_error)
            error_msg += " " + _(
                "problem can be solved by double-checking your "
                "credit card details, or contacting your bank?")
            raise ValidationError(error_msg)

        tx = self.search([('reference', '=', reference)])
        if not tx:
            error_msg = (_(
                'Checkout: no order found for reference %s') % reference)
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        elif len(tx) > 1:
            error_msg = (_(
                'Checkout: %s orders found for reference %s') % (
                    len(tx), reference))
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        return tx[0]

    def _checkout_form_validate(self, data):
        status_code = int(data.get('responseCode'))
        if status_code in self._checkout_valid_tx_status:
            self.write({
                'state': 'done',
                'acquirer_reference': data.get('id'),
            })
            return True
        elif status_code in self._checkout_pending_tx_status:
            self.write({
                'state': 'pending',
                'acquirer_reference': data.get('id'),
            })
            return True
        elif status_code in self._checkout_cancel_tx_status:
            self.write({
                'state': 'cancel',
                'acquirer_reference': data.get('id'),
            })
            return True
        else:
            error = data.get(' responseAdvancedInfo')
            _logger.info(error)
            self.write({
                'state': 'error',
                'state_message': error,
                'acquirer_reference': data.get('id'),
            })
            return False

    @api.multi
    def _checkout_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        reference = data['metadata']['order']
        if reference != self.reference:
            invalid_parameters.append(('Reference', reference, self.reference))
        return invalid_parameters
