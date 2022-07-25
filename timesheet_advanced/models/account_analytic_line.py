# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.multi
    @api.onchange('start_hour', 'end_hour')
    def unit_amount_change(self):
        for rec in self:
            if rec.start_hour and rec.end_hour:
                if rec.end_hour > rec.start_hour:
                    rec.unit_amount = rec.end_hour - rec.start_hour
                else:
                    rec.unit_amount = (rec.end_hour - rec.start_hour + 12) % 12

    hr_timesheet_id = fields.Many2one(
        'hr.timesheet',
        string='Timesheet'
    )
    start_hour = fields.Float('Start')
    end_hour = fields.Float('End')
    unit_amount = fields.Float(
        'Quantity',
        default=0.0
    )

    # @api.onchange('start_hour', 'end_hour')
    # def onchange_date_start_end(self):
    #     if self.start_hour > 0:


    # @api.onchange('date')
    # def project_id_change(self):
    #     if self.date:
    #         date = fields.Date.from_string(
    #             self.date).strftime('%Y-%m-%d %H:%M:%S')
    #         project_task_id = self.env['project.task'].search([
    #             ('date_start', '<=', date), ('date_end', '>=', date)], limit=1)
    #         self.task_id = project_task_id.id
    #         self.project_id = project_task_id.project_id.id
    #         self.employee_id = project_task_id.user_id.id or self.env.user.id
