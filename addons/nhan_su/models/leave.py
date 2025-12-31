from odoo import models, fields

class Leave(models.Model):
    _name = 'nhan_su.leave'
    _description = 'Nghỉ phép'

    employee_id = fields.Many2one('nhan_su.employee', string='Nhân viên', required=True)
    start_date = fields.Date('Từ ngày')
    end_date = fields.Date('Đến ngày')
    reason = fields.Char('Lý do')
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('approved', 'Đã duyệt'),
        ('refused', 'Từ chối')
    ], string='Trạng thái', default='draft')
