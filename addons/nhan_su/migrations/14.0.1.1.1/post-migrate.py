from odoo import api, SUPERUSER_ID

def update_attendance_notes(env):
    attendances = env['nhan_su.attendance'].search([])
    for att in attendances:
        att._update_salary_info()

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    update_attendance_notes(env)
