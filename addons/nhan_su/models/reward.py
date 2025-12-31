from odoo import models, fields

class Reward(models.Model):
    _name = 'nhan_su.reward'
    _description = 'Khen thưởng'

    employee_id = fields.Many2one('nhan_su.employee', string='Nhân viên', required=True)
    date = fields.Date('Ngày')
    reason = fields.Char('Lý do')
    amount = fields.Float('Số tiền thưởng')
    note = fields.Char('Ghi chú')
