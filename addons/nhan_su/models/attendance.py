from odoo import models, fields, api


from datetime import datetime, timedelta, time


class Attendance(models.Model):
    _name = 'nhan_su.attendance'
    _description = 'Chấm công'

    @api.model
    def create(self, vals):
        att = super().create(vals)
        att._update_salary_info()
        return att

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            rec._update_salary_info()
        return res

    def _update_salary_info(self):
        # Tìm bảng lương tháng của nhân viên
        if not self.employee_id or not self.ngay_cham_cong:
            return
        month = str(self.ngay_cham_cong.month)
        year = str(self.ngay_cham_cong.year)
        Salary = self.env['nhan_su.salary']
        salary = Salary.search([
            ('employee_id', '=', self.employee_id.id),
            ('month', '=', month),
            ('year', '=', year)
        ], limit=1)
        if not salary:
            salary = Salary.create({
                'employee_id': self.employee_id.id,
                'month': month,
                'year': year,
                'base_salary': self.employee_id.base_salary,
            })
        # Cập nhật số công (so_cong sẽ tự động compute)
        # Cảnh báo đi muộn/về sớm
        from datetime import time
        warning = False
        if self.gio_vao and self.gio_vao.time() > time(8,45):
            warning = True
        if self.gio_ra and self.gio_ra.time() < time(17,15):
            warning = True
        if warning:
            self.note = (self.note or '') + ' [Cảnh báo: Đi muộn/Về sớm]'

    employee_id = fields.Many2one('nhan_su.employee', string='Nhân viên', required=True)
    ngay_cham_cong = fields.Date('Ngày chấm công')
    gio_vao = fields.Datetime('Giờ vào')
    gio_ra = fields.Datetime('Giờ ra')
    so_gio_lam = fields.Float('Số giờ làm', compute='_compute_so_gio_lam', store=True)
    trang_thai = fields.Selection([
        ('di_lam', 'Đi làm'),
        ('nghi', 'Nghỉ'),
        ('di_muon', 'Đi muộn'),
        ('ve_som', 'Về sớm'),
    ], string='Trạng thái', default='di_lam')
    note = fields.Char('Ghi chú')


    @api.depends('gio_vao', 'gio_ra')
    def _compute_so_gio_lam(self):
        for rec in self:
            if rec.gio_vao and rec.gio_ra:
                # Chuẩn: vào 8:30, ra 17:30, nghỉ trưa 12h-13h
                start = rec.gio_vao
                end = rec.gio_ra
                total = (end - start).total_seconds() / 3600.0
                # Trừ giờ nghỉ trưa nếu ca làm vượt qua 12h-13h
                lunch_start = start.replace(hour=12, minute=0, second=0, microsecond=0)
                lunch_end = start.replace(hour=13, minute=0, second=0, microsecond=0)
                if start < lunch_start < end:
                    lunch_overlap = min(end, lunch_end) - lunch_start
                    total -= lunch_overlap.total_seconds() / 3600.0
                rec.so_gio_lam = total
            else:
                rec.so_gio_lam = 0.0

    @api.depends('check_in', 'check_out')
    def _compute_work_hours(self):
        for rec in self:
            if rec.check_in and rec.check_out:
                delta = rec.check_out - rec.check_in
                rec.work_hours = delta.total_seconds() / 3600.0
            else:
                rec.work_hours = 0.0

    @api.depends('check_out')
    def _compute_overtime(self):
        for rec in self:
            if rec.check_out:
                standard_out = datetime.combine(rec.check_out.date(), time(17, 0))
                overtime = (rec.check_out - standard_out).total_seconds() / 3600.0
                rec.overtime = overtime if overtime > 0 else 0.0
            else:
                rec.overtime = 0.0
