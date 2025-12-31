from odoo import models, fields

class Discipline(models.Model):
    _name = 'nhan_su.discipline'
    _description = 'Kỷ luật'

    employee_id = fields.Many2one('nhan_su.employee', string='Nhân viên', required=True)
    date = fields.Date('Ngày')
    reason = fields.Char('Lý do')
    amount = fields.Float('Số tiền phạt')
    note = fields.Char('Ghi chú')
