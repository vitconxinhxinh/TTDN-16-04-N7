from odoo import models, fields, api


class Document(models.Model):
    _name = 'customer.document.document'
    _description = 'Văn bản số hóa khách hàng'

    code = fields.Char(string='Mã VB', readonly=True, required=True, copy=False, store=True, default=False)

    name = fields.Char(string='Tên văn bản', required=True)
    document_type = fields.Selection([
        ('contract', 'Hợp đồng'),
        ('quotation', 'Báo giá'),
        ('legal', 'Tài liệu pháp lý'),
        ('other', 'Khác')
    ], string='Loại văn bản', required=True)
    issue_date = fields.Date(string='Ngày phát hành')
    end_date = fields.Date(string='Ngày kết thúc')
    cost = fields.Float(string='Chi phí')
    state = fields.Selection([
        ('active', 'Hiệu lực'),
        ('inactive', 'Hết hiệu lực')
    ], string='Trạng thái', default='active')
    file_ids = fields.One2many('customer.document.file', 'document_id', string='File đính kèm')
    description = fields.Text(string='Mô tả')
    customer_id = fields.Many2one('customer.document.customer', string='Khách hàng', required=True, ondelete='cascade')

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if 'code' in fields:
            res['code'] = self.env['ir.sequence'].next_by_code('customer.document.document')
        return res

    @api.model
    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('customer.document.document')
        return super().create(vals)
