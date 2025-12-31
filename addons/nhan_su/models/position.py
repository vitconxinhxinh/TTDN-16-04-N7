from odoo import models, fields

class Position(models.Model):
    _name = 'nhan_su.position'
    _description = 'Chức vụ'

    name = fields.Char('Tên chức vụ', required=True)
    code = fields.Char('Mã chức vụ')
    employee_ids = fields.One2many('nhan_su.employee', 'position_id', string='Nhân viên')
