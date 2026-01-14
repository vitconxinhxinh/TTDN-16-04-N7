from odoo import models, fields

class DocumentFile(models.Model):
    _name = 'customer.document.file'
    _description = 'Tệp đính kèm văn bản khách hàng'

    name = fields.Char(string='Tên file')
    file = fields.Binary(string='File', required=True)
    document_id = fields.Many2one('customer.document.document', string='Văn bản', required=True, ondelete='cascade')
    upload_user_id = fields.Many2one('res.users', string='Người upload', default=lambda self: self.env.uid)
    upload_date = fields.Datetime(string='Ngày upload', default=fields.Datetime.now)
