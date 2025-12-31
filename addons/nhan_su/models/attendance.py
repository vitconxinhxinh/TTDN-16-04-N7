from odoo import models, fields

class Attendance(models.Model):
    _name = 'nhan_su.attendance'
    _description = 'Chấm công'

    employee_id = fields.Many2one('nhan_su.employee', string='Nhân viên', required=True)
    date = fields.Date('Ngày')
    check_in = fields.Datetime('Giờ vào')
    check_out = fields.Datetime('Giờ ra')
    note = fields.Char('Ghi chú')
