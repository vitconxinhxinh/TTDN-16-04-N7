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
    ], string='Loại văn bản gợi ý')

    def action_suggest(self):
        """Gọi AI để gợi ý loại văn bản (dùng tên file)."""
        self.ensure_one()
        text = self.file_id.name or ''
        self._call_ai_and_update(text)

    def action_suggest_with_text(self, text):
        """Gọi AI để gợi ý loại văn bản (dùng nội dung file)."""
        self.ensure_one()
        self._call_ai_and_update(text)

    def _call_ai_and_update(self, text):
        """Gọi predict.py và cập nhật kết quả."""
        import subprocess
        import json
        import os
        
        script_path = os.path.join(
            os.path.dirname(__file__), '..', 'controllers', 'predict.py'
        )
        
        try:
            result = subprocess.run([
                'python3', script_path, text
            ], capture_output=True, text=True, timeout=5)
            
            output = result.stdout.strip()
            
            # Parse JSON response
            try:
                data = json.loads(output)
                label = data.get('label', 'other')
            except json.JSONDecodeError:
                label = output if output in ['labor_contract', 'sales_contract', 'service_contract', 
                                             'lease_contract', 'nda_contract', 'quotation', 'legal', 'other'] else 'other'
            
            # Cập nhật wizard
            self.suggested_type = label
            
        except Exception as e:
            self.suggested_type = 'other'

    def action_confirm(self):
        """Xác nhận và lưu loại văn bản vào file."""
        self.ensure_one()
        if self.suggested_type:
            self.file_id.document_type = self.suggested_type
        return {'type': 'ir.actions.act_window_close'}
