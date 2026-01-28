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
    document_type = fields.Selection([
        ('labor_contract', 'Hợp đồng lao động'),
        ('sales_contract', 'Hợp đồng mua bán'),
        ('service_contract', 'Hợp đồng dịch vụ'),
        ('lease_contract', 'Hợp đồng thuê'),
        ('nda_contract', 'Hợp đồng bảo mật'),
        ('quotation', 'Báo giá'),
        ('legal', 'Tài liệu pháp lý'),
        ('other', 'Khác')
    ], string='Loại văn bản', copy=False)
    document_type_manual = fields.Char(string='Loại văn bản (Tùy chỉnh)', copy=False)

    def action_suggest_label(self):
        """Gọi AI để gợi ý nhãn và hiển thị wizard để xác nhận."""
        self.ensure_one()
        label = self._suggest_label_from_ai(self.name or '')
        if not label:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'AI gợi ý',
                    'message': 'Không gợi ý được nhãn!',
                    'sticky': False,
                    'type': 'warning',
                }
            }
        
        # Tạo wizard với kết quả gợi ý
        wizard = self.env['ai.suggestion.wizard'].create({
            'file_id': self.id,
            'suggested_type': label,
            'confidence': 0.85,  # Có thể lấy từ AI model nếu cần
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Gợi ý từ AI',
            'res_model': 'ai.suggestion.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',
        }

    @classmethod
    def _suggest_label_from_ai(cls, text):
        """Gọi script predict.py để phân loại văn bản."""
        import subprocess
        import os
        script_path = os.path.join(os.path.dirname(__file__), '..', 'controllers', 'predict.py')
        try:
            result = subprocess.run([
                'python3', script_path, text
            ], capture_output=True, text=True, check=True, timeout=5)
            label = result.stdout.strip()
            # Map nhãn trả về sang selection
            if label in dict(cls._fields['suggested_document_type'].selection):
                return label
        except Exception:
            pass
        return None
    @api.model
    def create(self, vals):
        # Không tự động gợi ý khi tạo, để người dùng chủ động click button
        rec = super().create(vals)
        return rec

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
