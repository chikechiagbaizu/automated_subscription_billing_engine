{
    'name': 'Automated Subscription Billing Engine',
    'summary': 'Automated Subscription Billing Engine',
    'author': 'Chike Chiagbaizu',
    'maintainer': 'Chike Chiagbaizu',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'sequence': 1,
    'application': True,
    'installable': True,
    'depends': [
        'base',
        'sale',
    ],
    'data': [
        'views/view_billing_subscription_pivot.xml',
        'views/view_billing_subscription_graph.xml'
    ],
}