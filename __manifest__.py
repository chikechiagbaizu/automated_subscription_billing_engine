{
    'name': 'Automated Subscription Billing Engine',
    'summary': 'Recurring customer invoicing from subscriptions via an idempotent cron.',
    'description': """
    Automated Subscription Billing Engine
    =====================================
    Creates recurring customer invoices from subscription records.
    A scheduled action bills only subscriptions that are due and then
    advances the next invoice date, so repeated runs never bill the same
    period twice. Supports monthly and yearly recurrence, catch-up billing
    for missed runs, and month-end date handling.
    """,
    'maintainer': 'Chike Chiagbaizu',
    'version': '19.0.1.1.0',
    'license': 'LGPL-3',
    'sequence': 1,
    'application': True,
    'installable': True,
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'data/ir_cron_subscription_billing_worker.xml',
        'data/ir_sequence_billing_subscription.xml',
        'security/billing_subscription_groups.xml',
        'security/ir.model.access.csv',
        'views/billing_subscription_actions.xml',
        'views/view_billing_subscription_form.xml',
        'views/view_billing_subscription_list.xml',
        'views/view_billing_subscription_pivot.xml',
        'views/view_billing_subscription_graph.xml',
        'views/billing_subscription_menus.xml',
    ],
}