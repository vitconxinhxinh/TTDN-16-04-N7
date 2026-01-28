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
        """Trích xuất text từ file - convert mọi định dạng thành text"""
        import base64
        import io
        import tempfile
        import os
        
        if not self.file:
            return ""
        
        try:
            file_content = base64.b64decode(self.file)
            filename = (self.name or "").lower()
            text = ""
            
            # Lưu file tạm để xử lý
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp_file:
                tmp_file.write(file_content)
                tmp_file.flush()
                tmp_path = tmp_file.name
            
            try:
                # ========== PDF ==========
                if filename.endswith('.pdf'):
                    # Thử pdfplumber trước
                    try:
                        import pdfplumber
                        with pdfplumber.open(tmp_path) as pdf:
                            for page in pdf.pages[:10]:
                                page_text = page.extract_text()
                                if page_text:
                                    text += page_text + "\n"
                    except:
                        pass
                    
                    # Nếu không có text, thử PyPDF2
                    if not text.strip():
                        try:
                            import PyPDF2
                            with open(tmp_path, 'rb') as f:
                                pdf_reader = PyPDF2.PdfReader(f)
                                for page in pdf_reader.pages[:10]:
                                    text += page.extract_text() + "\n"
                        except:
                            pass
                
                # ========== DOCX ==========
                elif filename.endswith('.docx'):
                    try:
                        from docx import Document
                        doc = Document(tmp_path)
                        text = "\n".join([para.text for para in doc.paragraphs])
                    except:
                        pass
                
                # ========== DOC (cũ) ==========
                elif filename.endswith('.doc'):
                    # Thử antiword
                    try:
                        import subprocess
                        result = subprocess.run(['antiword', tmp_path], 
                                              capture_output=True, text=True, timeout=10)
                        if result.returncode == 0:
                            text = result.stdout
                    except:
                        pass
                    
                    # Nếu không có antiword, thử catdoc
                    if not text.strip():
                        try:
                            import subprocess
                            result = subprocess.run(['catdoc', tmp_path], 
                                                  capture_output=True, text=True, timeout=10)
                            if result.returncode == 0:
                                text = result.stdout
                        except:
                            pass
                
                # ========== TXT, CSV, LOG ==========
                elif filename.endswith(('.txt', '.csv', '.log')):
                    encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252', 'iso-8859-1']
                    for encoding in encodings:
                        try:
                            with open(tmp_path, 'r', encoding=encoding) as f:
                                text = f.read()
                                break
                        except:
                            continue
                
                # ========== Fallback: Thử đọc như text ==========
                if not text.strip():
                    encodings = ['utf-8', 'latin-1', 'cp1252']
                    for encoding in encodings:
                        try:
                            with open(tmp_path, 'r', encoding=encoding, errors='ignore') as f:
                                text = f.read()
                                if text.strip():
                                    break
                        except:
                            continue
            
            finally:
                # Xóa file tạm
                try:
                    os.unlink(tmp_path)
                except:
                    pass
            
            # Giới hạn độ dài text
            return text[:5000] if text else ""
                
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
