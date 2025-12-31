from odoo import models, fields, api


from datetime import datetime, timedelta, time


class Attendance(models.Model):
    _name = 'nhan_su.attendance'
    _description = 'Chấm công'

    def unlink(self):
        # Lưu lại thông tin nhân viên, tháng, năm trước khi xóa
        affected = [(rec.employee_id, rec.ngay_cham_cong.month if rec.ngay_cham_cong else None, rec.ngay_cham_cong.year if rec.ngay_cham_cong else None) for rec in self]
        res = super().unlink()
        # Sau khi xóa, cập nhật lại bảng lương liên quan
        Salary = self.env['nhan_su.salary']
        for emp, month, year in affected:
            if emp and month and year:
                salary = Salary.search([
                    ('employee_id', '=', emp.id),
                    ('month', '=', str(month)),
                    ('year', '=', str(year))
                ], limit=1)
                if salary:
                    salary._compute_so_cong()
        return res
    _name = 'nhan_su.attendance'
    _description = 'Chấm công'

    @api.model
    def create(self, vals):
        att = super().create(vals)
        att.with_context(skip_update_salary_info=True)._update_salary_info()
        return att

    def write(self, vals):
        res = super().write(vals)
        if not self.env.context.get('skip_update_salary_info'):
            for rec in self:
                rec.with_context(skip_update_salary_info=True)._update_salary_info()
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
        # Đảm bảo cập nhật lại số công khi có thay đổi chấm công
        salary._compute_so_cong()
        # Ghi lại số công để cập nhật giao diện nếu là trường store=True
        salary.write({'so_cong': salary.so_cong})
        # Cập nhật số công (so_cong sẽ tự động compute)
        # Cảnh báo đi muộn/về sớm
        from datetime import time
        import re
        import pytz
        warning = False
        # Nếu giờ vào hoặc giờ ra chưa có thì không cảnh báo
        if not self.gio_vao or not self.gio_ra:
            warning = False
        else:
            # Chuyển đổi sang múi giờ Asia/Ho_Chi_Minh trước khi so sánh
            tz = pytz.timezone('Asia/Ho_Chi_Minh')
            gio_vao_local = self.gio_vao.astimezone(tz).time().replace(microsecond=0)
            gio_ra_local = self.gio_ra.astimezone(tz).time().replace(microsecond=0)
            # So sánh chính xác từng giây
            if gio_vao_local <= time(8, 45, 0) and gio_ra_local >= time(17, 30, 0):
                warning = False
                # Luôn xóa mọi cảnh báo nếu hợp lệ
                if self.note and '[Cảnh báo: Đi muộn/Về sớm]' in self.note:
                    new_note = re.sub(r'(\s*\[Cảnh báo: Đi muộn/Về sớm\])+', '', self.note).strip()
                    self.with_context(skip_update_salary_info=True).write({'note': new_note})
            else:
                if gio_vao_local > time(8, 45, 0) or gio_ra_local < time(17, 25, 0):
                    warning = True
        if warning:
            # Thêm cảnh báo nếu chưa có
            if not self.note or '[Cảnh báo: Đi muộn/Về sớm]' not in self.note:
                self.with_context(skip_update_salary_info=True).write({'note': (self.note or '') + ' [Cảnh báo: Đi muộn/Về sớm]'})
        else:
            # Luôn xóa mọi cảnh báo nếu không còn vi phạm
            if self.note and '[Cảnh báo: Đi muộn/Về sớm]' in self.note:
                new_note = re.sub(r'(\s*\[Cảnh báo: Đi muộn/Về sớm\])+', '', self.note).strip()
                self.with_context(skip_update_salary_info=True).write({'note': new_note})

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
