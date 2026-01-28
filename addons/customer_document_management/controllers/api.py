import subprocess

from odoo import http
from odoo.http import request, Response
import json
import base64
import os
import numpy as np


class CustomerDocumentAPI(http.Controller):

    @http.route('/api/classify_text', type='json', auth='user', methods=['POST'])
    def classify_text(self, text=None, **kwargs):
        """API nhận văn bản và trả về nhãn phân loại từ model AI mới."""
        if not text:
            return {'error': 'Missing text'}
        script_path = os.path.join(os.path.dirname(__file__), 'predict.py')
        try:
            result = subprocess.run([
                'python3', script_path, text
            ], capture_output=True, text=True, check=True)
            label = result.stdout.strip()
            return {'label': label}
        except Exception as e:
            return {'error': str(e)}

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
        # Xác định mimetype
        mimetype, _ = mimetypes.guess_type(filename)
        if not mimetype:
            # Nếu là ảnh hoặc pdf mà không đoán được, thử đoán theo đuôi file
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
                mimetype = 'image/' + filename.split('.')[-1].lower()
            elif filename.lower().endswith('.pdf'):
                mimetype = 'application/pdf'
            else:
                mimetype = 'application/octet-stream'
        # Chỉ cho phép inline với file mà browser hỗ trợ
        inline_types = ['image/', 'application/pdf', 'text/', 'application/xhtml+xml', 'application/xml']
        if any(mimetype.startswith(t) for t in inline_types):
            disposition = f'inline; filename="{filename}"'
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
                'document_type': d.document_type,
                'issue_date': d.issue_date,
                'end_date': d.end_date,
                'cost': d.cost,
                'state': d.state,
                'customer_id': d.customer_id.id,
            } for d in docs
        ]
        return {'documents': data}
