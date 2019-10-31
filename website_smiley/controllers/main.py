# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.http import request


class SmileyController(http.Controller):
    
    @http.route('/smiley/rating', type='json', auth='public')
    def smiley_rating(self, uuid, rate, reason=None, **kwargs):
        Rating = request.env['rating.rating']
        values = {
        	'res_id': 1,
        	'res_model': 'mail.channel',
            'rating': rate,
            'smiley_rating': True
        }
        rating = Rating.sudo().create(values)
        return rating.id
