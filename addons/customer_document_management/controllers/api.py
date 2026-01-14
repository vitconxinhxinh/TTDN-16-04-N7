from odoo import http
from odoo.http import request, Response
import json
import requests

class CustomerDocumentAPI(http.Controller):
        @http.route('/api/suggest_documents', type='json', auth='user', methods=['POST'])
        def suggest_documents(self, customer_id=None, **kwargs):
            if not customer_id:
                return {'error': 'customer_id is required'}
            docs = request.env['customer.document.document'].sudo().search([
                ('customer_id', '=', customer_id)
            ])
            # Chuẩn bị dữ liệu gửi lên AI (ví dụ: OpenAI)
            doc_texts = [f"{d.name} {d.description or ''}" for d in docs]
            # Gọi OpenAI API (hoặc AI khác) để lấy embedding/gợi ý
            # Thay YOUR_OPENAI_API_KEY bằng key thực tế
            openai_api_key = 'YOUR_OPENAI_API_KEY'
            ai_results = []
            try:
                response = requests.post(
                    'https://api.openai.com/v1/embeddings',
                    headers={
                        'Authorization': f'Bearer {openai_api_key}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'input': doc_texts,
                        'model': 'text-embedding-ada-002'
                    },
                    timeout=10
                )
                if response.status_code == 200:
                    ai_results = response.json().get('data', [])
            except Exception as e:
                ai_results = []
            # Ở đây bạn có thể xử lý ai_results để chọn ra các văn bản liên quan nhất
            # Demo: trả về toàn bộ docs như cũ, có thể bổ sung logic lọc theo AI
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
            return {'suggested_documents': data, 'ai_results': ai_results}
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
