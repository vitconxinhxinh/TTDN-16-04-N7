
from odoo import http
from odoo.http import request, Response
import json
import base64
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'ml_data', 'news_embedding_model')
_sentence_model = None

def get_sentence_model():
    global _sentence_model
    if _sentence_model is None:
        _sentence_model = SentenceTransformer(MODEL_PATH)
    return _sentence_model


class CustomerDocumentAPI(http.Controller):
    @http.route('/api/suggest_documents', type='json', auth='user', methods=['POST'])
    def suggest_documents(self, customer_id=None, query=None, top_k=5, **kwargs):
        import logging
        _logger = logging.getLogger(__name__)
        _logger.info('--- [AI Suggest] customer_id: %s, query: %s, top_k: %s', customer_id, query, top_k)
        if not customer_id:
            _logger.warning('customer_id is required')
            return {'error': 'customer_id is required'}
        docs = request.env['customer.document.document'].sudo().search([
            ('customer_id', '=', customer_id)
        ])
        _logger.info('--- [AI Suggest] Found %d docs for customer_id=%s', len(docs), customer_id)
        doc_texts = [f"{d.name} {d.description or ''}" for d in docs]
        _logger.debug('--- [AI Suggest] doc_texts: %s', doc_texts)
        try:
            model = get_sentence_model()
            doc_embeddings = model.encode(doc_texts)
            _logger.debug('--- [AI Suggest] doc_embeddings shape: %s', str(np.array(doc_embeddings).shape))
        except Exception as e:
            _logger.error('--- [AI Suggest] Error loading model or encoding: %s', str(e))
            return {'error': 'Model error: %s' % str(e)}

        # Nếu có truy vấn (query), tính similarity và gợi ý tài liệu liên quan nhất
        if query:
            try:
                query_emb = model.encode([query])[0]
                sims = cosine_similarity([query_emb], doc_embeddings)[0]
                _logger.info('--- [AI Suggest] Similarity scores: %s', sims)
                top_indices = np.argsort(sims)[::-1][:top_k]
                suggested = [docs[i] for i in top_indices]
                scores = [float(sims[i]) for i in top_indices]
            except Exception as e:
                _logger.error('--- [AI Suggest] Error in similarity calculation: %s', str(e))
                suggested = []
                scores = []
        else:
            suggested = docs
            scores = [1.0] * len(docs)

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
                'similarity': scores[i] if i < len(scores) else None,
            } for i, d in enumerate(suggested)
        ]
        _logger.info('--- [AI Suggest] Return %d suggested documents', len(data))
        return {'suggested_documents': data}

    @http.route('/api/document_file/download/<int:file_id>', type='http', auth='user', methods=['GET'])
    def download_document_file(self, file_id, **kwargs):
        """API download file đính kèm theo ID."""
        file_rec = request.env['customer.document.file'].sudo().browse(file_id)
        if not file_rec or not file_rec.file:
            return request.not_found()
        file_content = base64.b64decode(file_rec.file)
        filename = file_rec.name or f"file_{file_id}"
        headers = [
            ('Content-Type', 'application/octet-stream'),
            ('Content-Disposition', f'attachment; filename="{filename}"')
        ]
        return request.make_response(file_content, headers)

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
