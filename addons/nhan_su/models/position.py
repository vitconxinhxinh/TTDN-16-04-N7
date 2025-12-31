from odoo import models, fields

class Position(models.Model):
    _name = 'nhan_su.position'
    _description = 'Chức vụ'

    name = fields.Char('Tên chức vụ', required=True)
    code = fields.Char('Mã chức vụ', readonly=True, copy=False, default=lambda self: self._generate_code())

    @api.model
    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = self._generate_code()
        return super().create(vals)

    @api.model
    def _generate_code(self):
        last = self.search([], order='id desc', limit=1)
        next_id = (last.id or 0) + 1
        return 'CV%03d' % next_id
    employee_ids = fields.One2many('nhan_su.employee', 'position_id', string='Nhân viên')
