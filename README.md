# Project 4: Automated Subscription Billing Engine & BI Dashboard 🗓️📊

An enterprise cloud automation application providing automated background invoice generation routines and multidimensional analytical visual tools for high-volume subscription ecosystems.

## 📋 Business Case & Problem Statement
SaaS platforms and recurring business groups face structural financial bottlenecks when scaling transaction numbers. Relying on manually tracking contracts leads to massive delays in cash collections, breaks data integrity, and leaves executive boards completely blind to long-term monthly recurring revenue (MRR) trends.

**The Solution:** This app introduces an automated background scheduling worker (`ir.cron`) paired with high-performance Business Intelligence (BI) view components. At midnight every single day, the background processing thread scans database states natively, extracts parameters, and auto-generates draft customer invoice ledgers without administrative interaction. Simultaneously, custom multi-dimensional pivot matrix configurations give business directors real-time visual trend lines for financial reporting.

---

## 🛠️ Key Technical Implementations
* **Optimized High-Speed Aggregations:** Integrated native database-level group processing using Odoo’s `read_group()` tool. This layer executes optimized `GROUP BY` routines directly inside PostgreSQL, completely bypassing the memory bottlenecks of the standard Python recordset loops.
* **Modern Headless Task Automation:** Built a daily background cron worker framework optimized for modern specifications (Odoo 18.0+ / 19.0 paradigm constraints). The configuration automates long-running execution workers securely by removing obsolete parameter structures like `numbercall`.
* **Multidimensional Data Cube Visualizations:** Implemented cross-dimensional reporting architectures utilizing clean XML layout components (`<pivot>` and `<graph type="line">`), allowing real-time column grouping aggregations on live screens.
* **Atomic ORM Record Operations:** Engineered batch-safe row loop structures implementing clean database instantiations (`.create()`) combined with nested `Command.create()` tuple parameters to protect financial record histories.

---

## 🗂️ Module Directory Structure
```text
subscription_billing_engine/
├── __manifest__.py                  # Package descriptor configuration
├── __init__.py                      # Initializer configurations
├── data/
│   └── ir_cron_data.xml             # Automated cron background task scheduler configuration
├── models/
│   ├── __init__.py
│   └── sale_subscription.py         # Core subscription data tracking and cron logic models
└── views/
    └── subscription_bi_views.xml    # BI Pivot Grid and line trend chart dashboard configurations
```

---

## 🔩 Technical Specifications & Code Snippets

### Automated Daily Invoicing Worker Lifecycle Routine (Python)
```python
def cron_recurring_billing_routine(self):
    active_records = self.env['sale.subscription'].search([('stage', '=', 'active')])
    for record in active_records:
        self.env['account.move'].create({
            'partner_id': record.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': f"Automated Recurring Renewal Invoice for Contract Ref: {record.name}",
                    'quantity': 1.0,
                    'price_unit': record.recurring_amount
                })
            ]
        })
```

### Business Intelligence Grid Manifest (XML Pivot)
```xml
<pivot string="Subscription Analysis" sample="1">
    <field name="partner_id" type="row" />
    <field name="date_start" type="col" />
    <field name="recurring_amount" type="measure" />
</pivot>
```
