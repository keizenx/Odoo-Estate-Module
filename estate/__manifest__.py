{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Your Name',
    'category': 'Real Estate',
    'description': """
        Real Estate Management Module
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
} 