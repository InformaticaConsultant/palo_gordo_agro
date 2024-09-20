{
    'name': 'Palo Gordo Agro',
    'version': '1.0',
    'summary': 'Módulo para la gestión agrícola de Ingenio Palo Gordo',
    'description': 'Gestión de campos, cultivos y producción agrícola.',
    'author': 'Tu Nombre',
    'category': 'Agriculture',
    'depends': ['base', 'stock', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/campo_views.xml',
        'views/campo_menu.xml',
        'views/consumo_insumos_views.xml',
        'views/cultivo_views.xml',
        'views/cultivo_menu_config_view.xml',  # Menú de configuración
        'views/cultivo_kanban_view.xml',       # Vista Kanban
        'views/cultivo_state_views.xml',       # Vista de estados
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
