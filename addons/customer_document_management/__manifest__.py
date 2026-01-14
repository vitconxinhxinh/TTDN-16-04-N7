{
    'name': 'Customer Document Management',
    'version': '1.0',
    'summary': 'Quản lý khách hàng và văn bản số hóa',
    'author': 'FitDNU',
    'category': 'Tools',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/customer_views.xml',
        'views/document_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}