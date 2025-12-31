from odoo import models, fields


from datetime import datetime, timedelta, time

class Attendance(models.Model):
    _name = 'nhan_su.attendance'
    _description = 'Chấm công'

    employee_id = fields.Many2one('nhan_su.employee', string='Nhân viên', required=True)
    date = fields.Date('Ngày')
    check_in = fields.Datetime('Giờ vào')
    check_out = fields.Datetime('Giờ ra')
    note = fields.Char('Ghi chú')
    late = fields.Boolean('Đi muộn', compute='_compute_late', store=True)
    overtime = fields.Float('Số giờ tăng ca', compute='_compute_overtime', store=True)
    work_hours = fields.Float('Tổng giờ làm', compute='_compute_work_hours', store=True)

    @api.depends('check_in')
    def _compute_late(self):
        for rec in self:
            if rec.check_in:
                standard_in = datetime.combine(rec.check_in.date(), time(8, 0))
                rec.late = rec.check_in > standard_in
            else:
                rec.late = False

    @api.depends('check_in', 'check_out')
    def _compute_work_hours(self):
        for rec in self:
            if rec.check_in and rec.check_out:
                delta = rec.check_out - rec.check_in
                rec.work_hours = delta.total_seconds() / 3600.0
            else:
                rec.work_hours = 0.0

    @api.depends('check_out')
    def _compute_overtime(self):
        for rec in self:
            if rec.check_out:
                standard_out = datetime.combine(rec.check_out.date(), time(17, 0))
                overtime = (rec.check_out - standard_out).total_seconds() / 3600.0
                rec.overtime = overtime if overtime > 0 else 0.0
            else:
                rec.overtime = 0.0
