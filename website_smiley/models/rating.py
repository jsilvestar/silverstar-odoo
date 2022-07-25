# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api,fields, models


class Rating(models.Model):
    _inherit = "rating.rating"

    rating_smiley = fields.Boolean(string="Smiley Rating", help="Enabled if the rating has been filled from survey.")
