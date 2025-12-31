from odoo import models, fields, api




class Salary(models.Model):
    _name = 'nhan_su.salary'
    _description = 'Lương thưởng'

    date = fields.Date('Ngày', default=fields.Date.today, required=True)
    amount = fields.Float('Số tiền', compute='_compute_amount', store=True)
    employee_id = fields.Many2one('nhan_su.employee', string='Nhân viên', required=True)
    month = fields.Selection([(str(i), 'Tháng %s' % i) for i in range(1, 13)], string='Tháng', required=True)
    year = fields.Char('Năm', required=True, default=lambda self: fields.Date.today().year)
    base_salary = fields.Float('Lương cơ bản', required=True)
    work_days = fields.Integer('Số ngày công', required=True)
    late_days = fields.Integer('Số ngày đi muộn', required=True)
    overtime_hours = fields.Float('Số giờ tăng ca', required=True)
    bonus = fields.Float('Thưởng', default=0.0)
    penalty = fields.Float('Phạt', default=0.0)
    leave_days = fields.Integer('Số ngày nghỉ phép', default=0)
    total_salary = fields.Float('Tổng lương', compute='_compute_total_salary', store=True)
    note = fields.Char('Ghi chú')

    @api.depends('total_salary')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.total_salary

    @api.depends('base_salary', 'work_days', 'late_days', 'overtime_hours', 'bonus', 'penalty', 'leave_days')
    def _compute_total_salary(self):
        for rec in self:
            # Giả sử 1 tháng chuẩn 26 ngày công
            daily_salary = rec.base_salary / 26 if rec.base_salary else 0
            overtime_pay = rec.overtime_hours * (daily_salary / 8) * 1.5
            late_penalty = rec.late_days * 50000  # 50k/lần đi muộn
            leave_penalty = rec.leave_days * daily_salary
            rec.total_salary = rec.base_salary + overtime_pay + rec.bonus - (rec.penalty + late_penalty + leave_penalty)
