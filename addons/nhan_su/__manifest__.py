# -*- coding: utf-8 -*-
{
    'name': "nhan_su",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'models/models.xml',
        'security/ir.model.access.csv',
        'views/employee_views.xml',
        'views/employee_search_view.xml',
        'views/department_views.xml',
        'views/position_views.xml',
        'views/contract_views.xml',
        'views/attendance_views.xml',
        'views/salary_views.xml',
        'views/leave_views.xml',
        'views/discipline_views.xml',
        'views/reward_views.xml',
        'views/nhan_su_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
