from odoo import models, fields, api

class AISuggestionWizard(models.TransientModel):
    _name = 'ai.suggestion.wizard'
    _description = 'AI Suggestion Wizard'

    file_id = fields.Many2one('customer.document.file', string='File', required=True)
    suggested_type = fields.Selection([
        ('labor_contract', 'Hợp đồng lao động'),
        ('sales_contract', 'Hợp đồng mua bán'),
        ('service_contract', 'Hợp đồng dịch vụ'),
        ('lease_contract', 'Hợp đồng thuê'),
        ('nda_contract', 'Hợp đồng bảo mật'),
        ('quotation', 'Báo giá'),
        ('legal', 'Tài liệu pháp lý'),
        ('other', 'Khác')
    ], string='Loại văn bản gợi ý', readonly=True)
    confidence = fields.Float(string='Độ tin cậy', readonly=True)

    def action_confirm(self):
        """Xác nhận và lưu loại văn bản vào file."""
        self.ensure_one()
        if self.suggested_type:
            self.file_id.document_type = self.suggested_type
        return {'type': 'ir.actions.act_window_close'}
