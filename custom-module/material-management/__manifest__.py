{
    'name': 'Material Management',
    'version': '1.0',
    'summary': 'Manage materials and their suppliers',
    'description': """
        This module allows you to manage materials with their details including
        code, name, type, buy price and related supplier.
    """,
    'author': 'Sanja Avi',
    'website': 'https://www.yourwebsite.com',
    'category': 'Inventory',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/material_views.xml',
        'data/sequence.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}