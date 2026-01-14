from odoo import models, fields

class Document(models.Model):
    _name = 'customer.document.document'
    _description = 'Văn bản số hóa khách hàng'

    name = fields.Char(string='Tên văn bản', required=True)
    document_type = fields.Selection([
        ('contract', 'Hợp đồng'),
        ('quotation', 'Báo giá'),
        ('legal', 'Tài liệu pháp lý'),
        ('other', 'Khác')
    ], string='Loại văn bản', required=True)
    issue_date = fields.Date(string='Ngày phát hành')
    file = fields.Binary(string='File đính kèm')
    description = fields.Text(string='Mô tả')
    customer_id = fields.Many2one('customer.document.customer', string='Khách hàng', required=True, ondelete='cascade')
