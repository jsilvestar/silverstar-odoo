# -*- coding: utf-8 -*-
{
    'name': 'Partner Record',
    'version': '1.0',
    'summary': 'Fetching Partner Record using JS',
    'sequence': 3,
    'description': """
            Fetching Partner Record by using JS
    """,
    'category': 'Web',
    'author': 'J.Silver ****',
    'website': 'https://www.odoo.com',
    'depends': ['web'],
    'data': [
        'views/partner_record.xml',
        'views/partner_record_templates.xml',
    ],
    'demo': [],
    'qweb': [
        "static/src/xml/partner_record.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
