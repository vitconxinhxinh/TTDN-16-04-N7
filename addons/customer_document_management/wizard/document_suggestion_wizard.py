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
        # Lấy toàn bộ văn bản đã gắn với khách hàng này trong Odoo
        docs = self.customer_id.document_ids
        self.suggestion_ids.unlink()
        for d in docs:
            self.env['customer.document.suggestion.line'].create({
                'wizard_id': self.id,
                'text': f"{d.name} {d.description or ''}",
                'score': 1.0,  # Mặc định 1.0 vì không dùng AI
            })

class CustomerDocumentSuggestionLine(models.TransientModel):
    _name = 'customer.document.suggestion.line'
    _description = 'Dòng gợi ý văn bản'

    wizard_id = fields.Many2one('customer.document.suggestion.wizard', string='Wizard')
    text = fields.Text(string='Văn bản gợi ý')
    score = fields.Float(string='Độ tương đồng')
