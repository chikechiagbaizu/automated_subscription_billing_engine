# Automated Subscription Billing Engine

An Odoo 19 module that generates recurring customer invoices from simple
subscription records. A scheduled action (cron) finds subscriptions that are
due, creates the invoice, and moves the next billing date forward, so running
the job twice never bills the same period twice.

> **Status:** work in progress. The core subscription model and idempotent
> billing cron are implemented. Items marked *Planned* below are not built yet.

## What it does today

- **`billing.subscription` model** with customer, recurring amount, currency,
  start date, recurrence (monthly or yearly), stage, and next invoice date.
- **Stage workflow:** `draft -> active -> closed`, with guarded transitions.
  Only a draft can be activated, and only an active subscription can be closed.
  Closed subscriptions cannot be reactivated.
- **Idempotent billing cron:** each run bills only active subscriptions whose
  `next_invoice_date` is today or earlier, then advances that date. A second
  run immediately afterwards creates nothing.
- **Catch-up billing:** if the cron missed days, it creates one invoice per
  missed period, never beyond today.
- **Safe activation:** a draft activated after its start date begins billing
  from today, so no backlog is billed.
- **Month-end handling:** a subscription starting on the 31st is billed on the
  last day of shorter months and returns to the 31st afterwards
  (31 Jan -> 28 Feb -> 31 Mar -> 30 Apr).
- **Validation:** the recurring amount must be greater than zero, and the start
  date cannot be in the past.
- `stage` and `next_invoice_date` are read-only so they are changed only
  through the workflow methods.

## How billing works

1. Create a subscription (draft) and activate it. `next_invoice_date` is set
   to the start date, or to today if the start date has passed.
2. The cron `cron_recurring_billing_routine` searches for subscriptions with
   `stage = active` and `next_invoice_date <= today`.
3. For each one it creates and posts a customer invoice, then sets
   `next_invoice_date` to the next period, keeping the original billing day.
4. The loop repeats for that subscription until its next date is in the
   future, then moves to the next subscription.

## Requirements

- Odoo 19.0
- Depends on the `account` module

## Installation

1. Place the module folder in your Odoo addons path. The folder name must match
   the technical name `automated_subscription_billing_engine`.
2. Restart Odoo and update the apps list.
3. Install **Automated Subscription Billing Engine**.

## Planned

These are not implemented yet:

- **Complete invoice lines:** product, taxes, income account, and an invoice
  date set to the period being billed (currently catch-up invoices are all
  dated on the day the cron runs).
- **Duplicate guard:** link each invoice to its subscription and billing
  period, with a database-level uniqueness check.
- **Failure isolation:** process each subscription in its own savepoint and in
  batches, so one bad record cannot roll back the whole run.
- **Security:** access groups and `ir.model.access.csv` for users and managers.
- **Views and menus:** form, list, and buttons for activate/close.
- **Automated tests** (`TransactionCase`) covering: invoice created when due,
  not created when not due, not created twice, date advanced correctly,
  month-end behaviour, and failure isolation.

## Known limitations

- The cron currently runs in a single transaction. One failing subscription
  rolls back the whole run until failure isolation is added.
- "Today" is calculated from the context time zone, so the UI and the cron user
  can disagree on the date around midnight.
- Only monthly and yearly recurrence is supported, with no custom interval.
- Invoices are posted automatically; there is no draft-review option yet.

## Project layout

```
automated_subscription_billing_engine/
├── __manifest__.py
├── data/          # scheduled action (cron)
├── models/        # billing.subscription
└── views/         # to be added
```

## License

LGPL-3