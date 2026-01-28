import subprocess
import joblib

from odoo import http
from odoo.http import request, Response
import json
import base64
import os
import numpy as np


class CustomerDocumentAPI(http.Controller):

    @http.route('/api/classify_text', type='json', auth='user', methods=['POST'])
    def classify_text(self, text=None, **kwargs):
        """API nhận văn bản và trả về nhãn phân loại từ model AI."""
        if not text:
            return {'error': 'Missing text'}
        
        import joblib
        script_dir = os.path.dirname(__file__)
        model_file = os.path.join(script_dir, 'model.pkl')
        vectorizer_file = os.path.join(script_dir, 'vectorizer.pkl')
        
        # Map từ nhãn model sang nhãn Odoo
        label_map = {
            'labor_contract': 'labor_contract',
            'lease_contract': 'lease_contract',
            'sales_contract': 'sales_contract',
            'service_contract': 'service_contract',
            'nda_contract': 'nda_contract',
        }
        
        try:
            # Load model và vectorizer
            model = joblib.load(model_file)
            vectorizer = joblib.load(vectorizer_file)
            
            # Vectorize và predict
            text_vectorized = vectorizer.transform([text])
            decision_scores = model.decision_function(text_vectorized)[0]
            
            # Softmax để lấy xác suất
            e_x = np.exp(decision_scores - np.max(decision_scores))
            probs = e_x / e_x.sum()
            
            best_idx = np.argmax(probs)
            predicted_label = model.classes_[best_idx]
            confidence = float(probs[best_idx])
            
            # Map sang nhãn Odoo
            odoo_label = label_map.get(predicted_label, 'other')
            
            return {
                'label': odoo_label,
                'original_label': predicted_label,
                'confidence': confidence
            }
        except Exception as e:
            return {'error': str(e), 'label': 'other'}

    # ...existing code...

    @http.route('/api/document_file/view/<int:file_id>', type='http', auth='user', methods=['GET'])
    def view_document_file(self, file_id, **kwargs):
        """API xem file đính kèm trực tiếp trên trình duyệt theo ID."""
        import mimetypes
        file_rec = request.env['customer.document.file'].sudo().browse(file_id)
        if not file_rec or not file_rec.file:
            return request.not_found()
        file_content = base64.b64decode(file_rec.file)
        filename = file_rec.name or f"file_{file_id}"
        
        # ========== XỬ LÝ DOCX: Convert sang HTML để xem ==========
        if filename.lower().endswith('.docx'):
            try:
                from docx import Document
                import io
                doc = Document(io.BytesIO(file_content))
                
                # Convert sang HTML
                html = "<html><head><meta charset='utf-8'><style>"
                html += "body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }"
                html += "p { margin: 10px 0; }"
                html += "</style></head><body>"
                html += f"<h2>{filename}</h2><hr>"
                
                for para in doc.paragraphs:
                    if para.text.strip():
                        html += f"<p>{para.text}</p>"
                
                html += "</body></html>"
                
                headers = [
                    ('Content-Type', 'text/html; charset=utf-8'),
                ]
                return request.make_response(html.encode('utf-8'), headers)
            except:
                # Fallback: download nếu convert lỗi
                pass
        
        # Xác định mimetype
        mimetype, _ = mimetypes.guess_type(filename)
        if not mimetype:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
                mimetype = 'image/' + filename.split('.')[-1].lower()
            elif filename.lower().endswith('.pdf'):
                mimetype = 'application/pdf'
            elif filename.lower().endswith(('.txt', '.csv', '.log')):
                mimetype = 'text/plain'
            else:
                mimetype = 'application/octet-stream'
        
        # Các file có thể xem trực tiếp trên browser
        inline_types = ['image/', 'application/pdf']
        
        # File DOC, Excel, PowerPoint không thể xem trực tiếp → tự động download
        download_extensions = ('.doc', '.xlsx', '.xls', '.pptx', '.ppt')
        if filename.lower().endswith(download_extensions):
            disposition = f'attachment; filename="{filename}"'
        elif any(mimetype.startswith(t) for t in inline_types):
            disposition = f'inline; filename="{filename}"'
        elif mimetype.startswith('text/'):
            # Text file: inline với charset UTF-8
            disposition = f'inline; filename="{filename}"'
            mimetype = 'text/plain; charset=utf-8'
        else:
            disposition = f'attachment; filename="{filename}"'
        
        headers = [
            ('Content-Type', mimetype),
            ('Content-Disposition', disposition)
        ]
        return request.make_response(file_content, headers)

    # ...existing code...

    @http.route('/api/customers', type='json', auth='user', methods=['GET'])
    def get_customers(self, **kwargs):
        customers = request.env['customer.document.customer'].sudo().search([])
        data = [
            {
                'id': c.id,
                'code': c.code,
                'name': c.name,
                'phone': c.phone,
                'email': c.email,
                'group': c.group,
                'province': getattr(c, 'province', ''),
                'district': getattr(c, 'district', ''),
                'ward': getattr(c, 'ward', ''),
                'address': c.address,
                'state': c.state,
                'create_date': c.create_date,
            } for c in customers
        ]
        return {'customers': data}

    @http.route('/api/documents', type='json', auth='user', methods=['GET'])
    def get_documents(self, **kwargs):
        docs = request.env['customer.document.document'].sudo().search([])
        data = [
            {
                'id': d.id,
                'code': d.code,
                'name': d.name,
                'issue_date': d.issue_date,
                'end_date': d.end_date,
                'cost': d.cost,
                'state': d.state,
                'customer_id': d.customer_id.id,
            } for d in docs
        ]
        return {'documents': data}
