from odoo import models, fields

class Customer(models.Model):
    _name = 'customer.document.customer'
    _description = 'Customer'

    name = fields.Char(string='Tên khách hàng', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Số điện thoại')
    address = fields.Char(string='Địa chỉ')
    document_ids = fields.One2many('customer.document.document', 'customer_id', string='Văn bản số hóa')
