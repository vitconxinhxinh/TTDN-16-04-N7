from odoo import models, fields, api

class Customer(models.Model):
    _name = 'customer.document.customer'
    _description = 'Customer'

    code = fields.Char(string='Mã KH', readonly=True, required=True, copy=False, store=True)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if 'code' in fields:
            res['code'] = self.env['ir.sequence'].next_by_code('customer.document.customer')
        return res
    name = fields.Char(string='Tên khách hàng', required=True)
    phone = fields.Char(string='Số điện thoại')
    email = fields.Char(string='Email')
    group = fields.Selection([
        ('vip', 'VIP'),
        ('thuong', 'Thường')
    ], string='Nhóm KH')
    province = fields.Char(string='Tỉnh/Thành phố')
    district = fields.Char(string='Quận/Huyện')
    ward = fields.Char(string='Xã/Phường')
    address = fields.Char(string='Địa chỉ cụ thể')
    state = fields.Selection([
        ('active', 'Hoạt động'),
        ('inactive', 'Ngừng HD')
    ], string='Trạng thái', default='active')
    create_date = fields.Datetime(string='Ngày tạo', readonly=True)
    document_ids = fields.One2many('customer.document.document', 'customer_id', string='Văn bản số hóa')

    @api.model
    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('customer.document.customer')
        res = super().create(vals)
        return res

    def unlink(self):
        for rec in self:
            raise models.UserError('Không được xóa khách hàng!')
        return super().unlink()
