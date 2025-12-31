from odoo import models, fields

class Contract(models.Model):
    _name = 'nhan_su.contract'
    _description = 'Hợp đồng lao động'

    name = fields.Char('Tên hợp đồng', required=True)
    employee_id = fields.Many2one('nhan_su.employee', string='Nhân viên', required=True)
    start_date = fields.Date('Ngày bắt đầu')
    end_date = fields.Date('Ngày kết thúc')
    contract_type = fields.Selection([
        ('permanent', 'Dài hạn'),
        ('temporary', 'Thời vụ'),
        ('intern', 'Thực tập')
    ], string='Loại hợp đồng')
    salary = fields.Float('Lương cơ bản')
