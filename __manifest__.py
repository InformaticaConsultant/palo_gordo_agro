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
        'views/cultivo_kanban_view.xml', # Vista Kanban
        'views/cultivo_state_views.xml',
    ],
    'demo': [],  # Aquí podrías agregar datos de demostración si los necesitas
    'installable': True,
    'application': True,  # Esto marca el módulo como una aplicación independiente en el menú
    'auto_install': False,  # Evita que se instale automáticamente con otros módulos
}
