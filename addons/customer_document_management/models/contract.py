from odoo import models, fields, api

class Contract(models.Model):
    _name = 'customer.document.contract'
    _description = 'Hợp đồng khách hàng'

    code = fields.Char(string='Mã HĐ', required=True, copy=False, readonly=True, default='New')
    name = fields.Char(string='Tên HĐ', required=True)
    contract_type = fields.Selection([
        ('dichvu', 'Dịch vụ'),
        ('muaban', 'Mua bán'),
        ('laodong', 'Lao động'),
        ('khac', 'Khác')
    ], string='Loại hợp đồng')
    value = fields.Float(string='Giá trị')
    date_start = fields.Date(string='Ngày bắt đầu')
    date_end = fields.Date(string='Ngày kết thúc')
    state = fields.Selection([
        ('active', 'Hoạt động'),
        ('inactive', 'Ngừng HD')
    ], string='Trạng thái', default='active')
    file = fields.Binary(string='File đính kèm')
    customer_id = fields.Many2one('customer.document.customer', string='Khách hàng', required=True)
    create_date = fields.Datetime(string='Ngày tạo', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('customer.document.contract') or 'New'
        return super().create(vals)
