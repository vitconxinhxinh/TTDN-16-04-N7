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

    def _extract_text_from_file(self):
        """Trích xuất text từ file (PDF, DOCX, TXT, v.v.)"""
        import base64
        import io
        
        if not self.file:
            return ""
        
        try:
            # Decode file từ binary
            file_content = base64.b64decode(self.file)
            filename = (self.name or "").lower()
            
            # Xử lý PDF
            if filename.endswith('.pdf'):
                try:
                    import pdfplumber
                    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                        text = ""
                        for page in pdf.pages[:5]:  # Chỉ lấy 5 trang đầu để nhanh
                            text += page.extract_text() or ""
                        return text[:2000]  # Giới hạn 2000 ký tự
                except:
                    pass
            
            # Xử lý DOCX
            elif filename.endswith('.docx'):
                try:
                    from docx import Document
                    doc = Document(io.BytesIO(file_content))
                    text = "\n".join([para.text for para in doc.paragraphs[:100]])
                    return text[:2000]
                except:
                    pass
            
            # Xử lý TXT, CSV
            elif filename.endswith(('.txt', '.csv')):
                try:
                    text = file_content.decode('utf-8')
                    return text[:2000]
                except:
                    try:
                        text = file_content.decode('utf-16')
                        return text[:2000]
                    except:
                        pass
            
            # Fallback: thử decode UTF-8
            try:
                text = file_content.decode('utf-8')
                return text[:2000]
            except:
                return ""
                
        except Exception as e:
            return ""
    
    def action_suggest_label(self):
        """Gọi AI để gợi ý nhãn dựa trên nội dung file thực tế."""
        self.ensure_one()
        
        # Trích xuất text từ file
        file_text = self._extract_text_from_file()
        
        # Fallback: nếu không lấy được nội dung, dùng tên file
        if not file_text:
            file_text = self.name or ""
        
        if not file_text:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Lỗi',
                    'message': 'Không thể đọc nội dung file!',
                    'sticky': False,
                    'type': 'warning',
                }
            }
        
        # Tạo wizard
        wizard = self.env['ai.suggestion.wizard'].create({
            'file_id': self.id,
        })
        
        # Gọi action_suggest trên wizard với nội dung file
        wizard.action_suggest_with_text(file_text)
        
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
        import json
        script_path = os.path.join(os.path.dirname(__file__), '..', 'controllers', 'predict.py')
        valid_labels = ['labor_contract', 'sales_contract', 'service_contract', 
                        'lease_contract', 'nda_contract', 'quotation', 'legal', 'other']
        try:
            result = subprocess.run([
                'python3', script_path, text
            ], capture_output=True, text=True, check=True, timeout=5)
            output = result.stdout.strip()
            
            # Parse JSON response
            try:
                data = json.loads(output)
                label = data.get('label', 'other')
                confidence = data.get('confidence', 0)
            except json.JSONDecodeError:
                # Fallback nếu không phải JSON
                label = output if output in valid_labels else 'other'
                confidence = 0
            
            # Map nhãn trả về sang selection
            if label in valid_labels:
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
