# -*- coding: utf-8 -*-
{
    'name' : 'Timesheets Advanced',
    'version' : '1.0',
    'category': 'Human Resources',
    'sequence': 24,
    'author': 'https://www.itis.de',
    'description': """
This module implements a Daily timesheet system.
================================================
Employees can enter their timesheets in a single entry with ease.

Can track total hours of employees and calculate amount of hours.
    """,
    'website': 'https://www.itis.de',
    'depends' : ['hr_timesheet'],
    'data': [
        'views/timesheet_view.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
