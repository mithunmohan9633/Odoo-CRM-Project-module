{
    'name': 'Construction Workflow',
    'version': '1.0',
    'category': 'Construction',
    'depends': ['crm', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'data/project_stage_data.xml',
        'views/crm_lead_views.xml',
        'views/project_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
