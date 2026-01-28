from odoo import models, fields, api

class DocumentFile(models.Model):
    _name = 'customer.document.file'
    _description = 'Tệp đính kèm văn bản khách hàng'

    name = fields.Char(string='Tên file')
    file = fields.Binary(string='File', required=True)
    document_id = fields.Many2one('customer.document.document', string='Văn bản', required=True, ondelete='cascade')
    upload_user_id = fields.Many2one('res.users', string='Người upload', default=lambda self: self.env.uid)
    upload_date = fields.Datetime(string='Ngày upload', default=fields.Datetime.now)
    download_url = fields.Char(string='Tải về', compute='_compute_download_url', store=False)
    suggested_document_type = fields.Selection([
        ('contract', 'Hợp đồng'),
        ('quotation', 'Báo giá'),
        ('legal', 'Tài liệu pháp lý'),
        ('other', 'Khác')
    ], string='Nhãn gợi ý', readonly=True, copy=False)

    def action_suggest_label(self):
        """Gọi AI để gợi ý nhãn cho file này và cập nhật trường suggested_document_type."""
        label = self._suggest_label_from_ai(self.name or '')
        if label:
            self.suggested_document_type = label
        else:
            self.suggested_document_type = False
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'AI gợi ý',
                'message': f'Nhãn gợi ý: {label}' if label else 'Không gợi ý được nhãn!',
                'sticky': False,
            }
        }

    @classmethod
    def _suggest_label_from_ai(cls, text):
        import requests
        from odoo.tools import config
        # Lấy base url từ config
        base_url = config.get('web.base.url', 'http://localhost:8069')
        url = f"{base_url}/api/classify_text"
        try:
            resp = requests.post(url, json={"text": text}, auth=('admin', 'admin'))
            if resp.status_code == 200:
                data = resp.json()
                label = data.get('label')
                # Map nhãn trả về sang selection
                if label in dict(cls._fields['suggested_document_type'].selection):
                    return label
        except Exception:
            pass
        return None
    @api.model
    def create(self, vals):
        # Gợi ý nhãn khi upload file dựa trên tên file
        if not vals.get('suggested_document_type') and vals.get('name'):
            label = self._suggest_label_from_ai(vals['name'])
            if label:
                vals['suggested_document_type'] = label
        return super().create(vals)

    def action_view_file(self):
        """
        Trả về action để xem file trực tiếp trên trình duyệt (inline).
        """
        self.ensure_one()
        if not self.file:
            return
        return {
            'type': 'ir.actions.act_url',
            'url': f'/api/document_file/view/{self.id}',
            'target': 'self',
        }

    def _compute_download_url(self):
        for rec in self:
            if rec.id:
                rec.download_url = f'/web/content/customer.document.file/{rec.id}/file/{rec.name or "file"}?download=true'
            else:
                rec.download_url = ''

    def download_file(self):
        self.ensure_one()
        if not self.file:
            return
        return {
            'type': 'ir.actions.act_url',
            'url': self.download_url,
            'target': 'self',
        }

    def download_file_action(self):
        """
        Trả về action để tải file về từ giao diện Odoo.
        """
        self.ensure_one()
        if not self.file:
            return
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/customer.document.file/{self.id}/file/{self.name or "file"}?download=true',
            'target': 'self',
        }
