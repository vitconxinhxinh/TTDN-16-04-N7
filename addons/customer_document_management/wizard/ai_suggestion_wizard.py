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
    confidence = fields.Float(string='Độ tin cậy (%)')
    file_text = fields.Text(string='Nội dung file', readonly=True)

    def action_suggest(self):
        """Gọi AI để gợi ý loại văn bản (dùng tên file)."""
        self.ensure_one()
        text = self.file_id.name or ''
        self._call_ai_and_update(text)

    def action_suggest_with_text(self, text):
        """Gọi AI để gợi ý loại văn bản (dùng nội dung file)."""
        self.ensure_one()
        self.file_text = text[:500]  # Lưu 500 ký tự đầu để debug
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
            
            # Debug: log output
            import sys
            print(f"[DEBUG] predict.py output: {output}", file=sys.stderr)
            print(f"[DEBUG] text length: {len(text)}", file=sys.stderr)
            
            # Parse JSON response
            try:
                data = json.loads(output)
                label = data.get('label', 'other')
                confidence = data.get('confidence', 0)
                print(f"[DEBUG] Parsed label: {label}, confidence: {confidence}", file=sys.stderr)
            except json.JSONDecodeError as e:
                print(f"[DEBUG] JSON parse error: {e}", file=sys.stderr)
                label = output if output in ['labor_contract', 'sales_contract', 'service_contract', 
                                             'lease_contract', 'nda_contract', 'quotation', 'legal', 'other'] else 'other'
                confidence = 0
            
            # Cập nhật wizard
            self.suggested_type = label
            self.confidence = confidence
            
        except Exception as e:
            import traceback
            print(f"[DEBUG] Exception: {traceback.format_exc()}", file=sys.stderr)
            self.suggested_type = 'other'
            self.confidence = 0

    def action_confirm(self):
        """Xác nhận và lưu loại văn bản vào file."""
        self.ensure_one()
        if self.suggested_type:
            self.file_id.document_type = self.suggested_type
        return {'type': 'ir.actions.act_window_close'}
