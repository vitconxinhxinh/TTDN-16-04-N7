from odoo import models, fields

class Department(models.Model):
    _name = 'nhan_su.department'
    _description = 'Phòng ban'

    name = fields.Char('Tên phòng ban', required=True)
    code = fields.Char('Mã phòng ban')
    employee_ids = fields.One2many('nhan_su.employee', 'department_id', string='Nhân viên')
