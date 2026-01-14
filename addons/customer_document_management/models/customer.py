from odoo import models, fields

class Customer(models.Model):
    _name = 'customer.document.customer'
    _description = 'Customer'

    code = fields.Char(string='Mã KH', required=True, copy=False, readonly=True, default='New')
    name = fields.Char(string='Tên khách hàng', required=True)
    phone = fields.Char(string='Số điện thoại')
    email = fields.Char(string='Email')
    group = fields.Selection([
        ('vip', 'VIP'),
        ('thuong', 'Thường')
    ], string='Nhóm KH')
    address = fields.Char(string='Quê quán')
    state = fields.Selection([
        ('active', 'Hoạt động'),
        ('inactive', 'Ngừng HD')
    ], string='Trạng thái', default='active')
    create_date = fields.Datetime(string='Ngày tạo', readonly=True)
    document_ids = fields.One2many('customer.document.document', 'customer_id', string='Văn bản số hóa')

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('customer.document.customer') or 'New'
        return super().create(vals)
