from odoo import models, fields

class Salary(models.Model):
    _name = 'nhan_su.salary'
    _description = 'Lương thưởng'

    employee_id = fields.Many2one('nhan_su.employee', string='Nhân viên', required=True)
    date = fields.Date('Ngày')
    amount = fields.Float('Số tiền')
    note = fields.Char('Ghi chú')
