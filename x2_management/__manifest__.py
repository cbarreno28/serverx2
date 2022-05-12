# -*- coding: utf-8 -*-
{
    'name': "X2 Management",
    'summary': "",
    'author': "Biofeeder S.A.",
    'website': "https://www.biofeeder.net",
    'version': '11.0.1.0.0',
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'views/broker_mqtt_views.xml',
        'views/message_plots_views.xml',
        'views/menu_views.xml'
    ],
    "depends":  ['base', 'enterprise_theme', 'odoo_rest', 'api_oauth2'],
    'installable': True,
    'auto_install': False,
    'application': True
   }
