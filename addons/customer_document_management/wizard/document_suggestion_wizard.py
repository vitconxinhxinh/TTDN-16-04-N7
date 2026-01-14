from odoo import models, fields, api
import os
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class CustomerDocumentSuggestion(models.TransientModel):
    _name = 'customer.document.suggestion.wizard'
    _description = 'Gợi ý văn bản cho khách hàng'

    customer_id = fields.Many2one('customer.document.customer', string='Khách hàng', required=True)
    top_k = fields.Integer(string='Số lượng gợi ý', default=5)
    suggestion_ids = fields.One2many('customer.document.suggestion.line', 'wizard_id', string='Gợi ý')

    def action_suggest(self):
        # Đường dẫn tới các file model đã train
        base_path = os.path.join(os.path.dirname(__file__), '../../ml_data')
        model = joblib.load(os.path.join(base_path, 'news_embedding_model.joblib'))
        embeddings = joblib.load(os.path.join(base_path, 'news_embeddings.joblib'))
        texts = joblib.load(os.path.join(base_path, 'news_texts.joblib'))
        # Lấy toàn bộ văn bản của khách hàng này
        docs = self.customer_id.document_ids
        doc_texts = [f"{d.name} {d.description or ''}" for d in docs]
        if not doc_texts:
            return
        query_emb = model.encode([doc_texts[0]])
        sims = cosine_similarity(query_emb, embeddings)[0]
        top_idx = sims.argsort()[-self.top_k:][::-1]
        # Xóa gợi ý cũ
        self.suggestion_ids.unlink()
        for i in top_idx:
            self.env['customer.document.suggestion.line'].create({
                'wizard_id': self.id,
                'text': texts[i],
                'score': float(sims[i]),
            })

class CustomerDocumentSuggestionLine(models.TransientModel):
    _name = 'customer.document.suggestion.line'
    _description = 'Dòng gợi ý văn bản'

    wizard_id = fields.Many2one('customer.document.suggestion.wizard', string='Wizard')
    text = fields.Text(string='Văn bản gợi ý')
    score = fields.Float(string='Độ tương đồng')
