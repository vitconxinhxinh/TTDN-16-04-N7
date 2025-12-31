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
    so_cong = fields.Float('Số công', compute='_compute_so_cong', store=True)
    late_days = fields.Integer('Số ngày đi muộn', required=True)
    overtime_hours = fields.Float('Số giờ tăng ca', required=True)
    bonus = fields.Float('Thưởng', default=0.0)
    penalty = fields.Float('Phạt', default=0.0)
    leave_days = fields.Integer('Số ngày nghỉ phép', default=0)
    luong_nhan = fields.Float('Lương nhận', compute='_compute_luong_nhan', store=True)
    note = fields.Char('Ghi chú')

    @api.depends('luong_nhan')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.luong_nhan


    @api.depends('employee_id', 'month', 'year')
    def _compute_so_cong(self):
        for rec in self:
            # Đếm số công từ bảng chấm công theo tháng/năm
            if rec.employee_id and rec.month and rec.year:
                attendances = self.env['nhan_su.attendance'].search([
                    ('employee_id', '=', rec.employee_id.id),
                    ('ngay_cham_cong', '>=', f"{rec.year}-{rec.month.zfill(2)}-01"),
                    ('ngay_cham_cong', '<=', f"{rec.year}-{rec.month.zfill(2)}-31")
                ])
                rec.so_cong = sum(1 for a in attendances if a.trang_thai == 'di_lam')
            else:
                rec.so_cong = 0

    @api.depends('so_cong', 'base_salary', 'bonus', 'penalty')
    def _compute_luong_nhan(self):
        for rec in self:
            cong = rec.so_cong or 1
            daily_salary = rec.base_salary / cong if rec.base_salary else 0
            rec.luong_nhan = rec.so_cong + daily_salary + rec.bonus - rec.penalty
