from odoo import models, fields, api



class Employee(models.Model):
    _name = 'nhan_su.employee'
    _description = 'Nhân viên'

    base_salary = fields.Float('Lương cơ bản', default=0.0)
    allowance = fields.Float('Phụ cấp', default=0.0)
    total_salary = fields.Float('Tổng lương', compute='_compute_total_salary', store=True)

    @api.depends('base_salary', 'allowance')
    def _compute_total_salary(self):
        for rec in self:
            rec.total_salary = rec.base_salary + rec.allowance

    identifier = fields.Char('Mã định danh', required=True, copy=False, readonly=True, default=lambda self: self._generate_identifier())
    code = fields.Char('Mã nhân viên')
    late = fields.Boolean('Đi trễ')
    name = fields.Char('Họ và tên', required=True)
    province = fields.Selection([
        ('ha_noi', 'Hà Nội'),
        ('ho_chi_minh', 'Hồ Chí Minh'),
        ('hai_phong', 'Hải Phòng'),
        ('da_nang', 'Đà Nẵng'),
        ('can_tho', 'Cần Thơ'),
        ('an_giang', 'An Giang'),
        ('bac_giang', 'Bắc Giang'),
        ('bac_kan', 'Bắc Kạn'),
        ('bac_lieu', 'Bạc Liêu'),
        ('bac_ninh', 'Bắc Ninh'),
        ('ben_tre', 'Bến Tre'),
        ('binh_dinh', 'Bình Định'),
        ('binh_duong', 'Bình Dương'),
        ('binh_phuoc', 'Bình Phước'),
        ('binh_thuan', 'Bình Thuận'),
        ('ca_mau', 'Cà Mau'),
        ('cao_bang', 'Cao Bằng'),
        ('dak_lak', 'Đắk Lắk'),
        ('dak_nong', 'Đắk Nông'),
        ('dien_bien', 'Điện Biên'),
        ('dong_nai', 'Đồng Nai'),
        ('dong_thap', 'Đồng Tháp'),
        ('gia_lai', 'Gia Lai'),
        ('ha_giang', 'Hà Giang'),
        ('ha_nam', 'Hà Nam'),
        ('ha_tinh', 'Hà Tĩnh'),
        ('hai_duong', 'Hải Dương'),
        ('hau_giang', 'Hậu Giang'),
        ('hoa_binh', 'Hòa Bình'),
        ('hung_yen', 'Hưng Yên'),
        ('khanh_hoa', 'Khánh Hòa'),
        ('kien_giang', 'Kiên Giang'),
        ('kon_tum', 'Kon Tum'),
        ('lai_chau', 'Lai Châu'),
        ('lam_dong', 'Lâm Đồng'),
        ('lang_son', 'Lạng Sơn'),
        ('lao_cai', 'Lào Cai'),
        ('long_an', 'Long An'),
        ('nam_dinh', 'Nam Định'),
        ('nghe_an', 'Nghệ An'),
        ('ninh_binh', 'Ninh Bình'),
        ('ninh_thuan', 'Ninh Thuận'),
        ('phu_tho', 'Phú Thọ'),
        ('phu_yen', 'Phú Yên'),
        ('quang_binh', 'Quảng Bình'),
        ('quang_nam', 'Quảng Nam'),
        ('quang_ngai', 'Quảng Ngãi'),
        ('quang_ninh', 'Quảng Ninh'),
        ('quang_tri', 'Quảng Trị'),
        ('soc_trang', 'Sóc Trăng'),
        ('son_la', 'Sơn La'),
        ('tay_ninh', 'Tây Ninh'),
        ('thai_binh', 'Thái Bình'),
        ('thai_nguyen', 'Thái Nguyên'),
        ('thanh_hoa', 'Thanh Hóa'),
        ('thua_thien_hue', 'Thừa Thiên Huế'),
        ('tien_giang', 'Tiền Giang'),
        ('tra_vinh', 'Trà Vinh'),
        ('tuyen_quang', 'Tuyên Quang'),
        ('vinh_long', 'Vĩnh Long'),
        ('vinh_phuc', 'Vĩnh Phúc'),
        ('yen_bai', 'Yên Bái'),
    ], string='Quê quán')
    department_id = fields.Many2one('nhan_su.department', string='Phòng ban')
    position_id = fields.Many2one('nhan_su.position', string='Chức vụ')
    contract_ids = fields.One2many('nhan_su.contract', 'employee_id', string='Hợp đồng lao động')
    salary_ids = fields.One2many('nhan_su.salary', 'employee_id', string='Lương thưởng')
    leave_ids = fields.One2many('nhan_su.leave', 'employee_id', string='Nghỉ phép')
    discipline_ids = fields.One2many('nhan_su.discipline', 'employee_id', string='Kỷ luật')
    reward_ids = fields.One2many('nhan_su.reward', 'employee_id', string='Khen thưởng')

    _sql_constraints = [
        ('identifier_unique', 'unique(identifier)', 'Mã định danh phải là duy nhất!'),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('identifier'):
            vals['identifier'] = self._generate_identifier()
        return super().create(vals)

    @api.model
    def _generate_identifier(self):
        last = self.search([], order='id desc', limit=1)
        next_id = (last.id or 0) + 1
        return 'EMP%05d' % next_id
