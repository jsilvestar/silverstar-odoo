# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Smiley',
    'version': '1.1',
    'category': 'website',
    'sequence': 23,
    'summary': 'Website Smiley',
    'description': """ website smiley
    """,
    'depends': [
        'website',
        'rating'
    ],
    'data': [
        'views/smiley_views.xml',
        'views/website_smiley_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
