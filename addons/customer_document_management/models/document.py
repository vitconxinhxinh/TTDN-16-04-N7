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

    def action_suggest_label(self):
        """Gọi AI để gợi ý nhãn cho tài liệu này dựa trên tên văn bản."""
        self.ensure_one()
        label = self._suggest_label_from_ai(self.name or '')
        if label:
            self.document_type = label
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'AI gợi ý',
                'message': f'Nhãn gợi ý: {dict(self._fields["document_type"].selection).get(label, "Không xác định")}' if label else 'Không gợi ý được nhãn!',
                'sticky': False,
                'type': 'success' if label else 'warning',
            }
        }

    @classmethod
    def _suggest_label_from_ai(cls, text):
        """Gọi API classify_text để lấy nhãn gợi ý."""
        import subprocess
        import os
        script_path = os.path.join(os.path.dirname(__file__), '..', 'controllers', 'predict.py')
        try:
            result = subprocess.run([
                'python3', script_path, text
            ], capture_output=True, text=True, check=True, timeout=5)
            label = result.stdout.strip()
            # Kiểm tra xem label có trong selection không
            if label in dict(cls._fields['document_type'].selection):
                return label
        except Exception:
            pass
        return None
