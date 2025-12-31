from odoo import models, fields, api

class Employee(models.Model):
    _name = 'nhan_su.employee'
    _description = 'Nhân viên'

    name = fields.Char('Tên nhân viên', required=True)
    code = fields.Char('Mã nhân viên')
    department_id = fields.Many2one('nhan_su.department', string='Phòng ban')
    position_id = fields.Many2one('nhan_su.position', string='Chức vụ')
    contract_ids = fields.One2many('nhan_su.contract', 'employee_id', string='Hợp đồng lao động')
    attendance_ids = fields.One2many('nhan_su.attendance', 'employee_id', string='Chấm công')
    salary_ids = fields.One2many('nhan_su.salary', 'employee_id', string='Lương thưởng')
    leave_ids = fields.One2many('nhan_su.leave', 'employee_id', string='Nghỉ phép')
    discipline_ids = fields.One2many('nhan_su.discipline', 'employee_id', string='Kỷ luật')
    reward_ids = fields.One2many('nhan_su.reward', 'employee_id', string='Khen thưởng')
