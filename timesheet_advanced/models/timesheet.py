# -*- coding: utf-8 -*-

# from lxml import etree
from xml.etree import ElementTree as ET

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HrTimesheet(models.Model):
    _name = 'hr.timesheet'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _description = 'HR Timesheet'

    date = field_name = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.today()
    )
    amount = field_name = fields.Float(
        string='Amount'
    )
    state = fields.Selection([
        ('new', 'New'),
        ('draft', 'Open'),
        ('confirm', 'Waiting Approval'),
        ('done', 'Approved')],
        default='new', track_visibility='onchange',
        string='State', required=True, index=True,
    )
    timesheet_ids = fields.One2many(
        'account.analytic.line',
        'hr_timesheet_id',
        string='Timesheets'
    )

    @api.onchange('date')
    def onchange_date(self):
        vals = {}
        if self.date:
            user_id = self.env.user.id
            date = fields.Date.from_string(
            self.date).strftime('%Y-%m-%d %H:%M:%S')
            project_task_ids = self.env['project.task'].search([
                ('user_id', '=', user_id),
                ('date_start', '<=', date),
                ('date_end', '>=', date)])
            print ('project_task_ids>>>>>>>>>>>>>>>>', project_task_ids)
            if project_task_ids:
                for project_task_id in project_task_ids:
                    vals['timesheet_ids']=[(0,0,{
                        'date': self.date,  
                        'employee_id': project_task_id.user_id.id or user_id,
                        'project_id': project_task_id.project_id.id or False,
                        'task_id': project_task_id.id or False,
                        'name': ''.join(ET.fromstring(project_task_id.description).itertext()) or ' ',
                    })]
            print ('valsssssssssssssssss', vals)
            # if self.date > fields.Date.today():
            #     raise UserError(
            #         "You cannot create for future date: %s" % self.date)
            # elif self.date < fields.Date.today():
            #     raise UserError(
            #         "You cannot create for Past date: %s" % self.date)
        return {'value': vals}

    def _timesheet_preprocess(self, vals):
        if vals.get('project_id') and not vals.get('account_id'):
            project = self.env['project.project'].browse(vals.get('project_id'))
            vals['account_id'] = project.analytic_account_id.id
        # employee implies user
        if vals.get('employee_id') and not vals.get('user_id'):
            employee = self.env['hr.employee'].browse(vals['employee_id'])
            vals['user_id'] = employee.user_id.id
        return vals

    @api.multi
    def name_get(self):
        for rec in self:
            if rec.date:
                return [(rec['id'], _('Week ') + str(fields.Date.from_string(
                    rec['date']).isocalendar()[1]))
                    for rec in self.sudo().read(['date'], load='_classic_write')]

    @api.constrains('date')
    def _check_date(self):
        if self.date:
            if self.date > fields.Date.today():
                raise UserError(
                    "You cannot create for future date: %s" % self.date)
            if self.date < fields.Date.today():
                    raise UserError(
                        "You cannot create for Past date: %s" % self.date)
