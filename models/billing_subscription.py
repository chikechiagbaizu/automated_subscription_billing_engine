from odoo import models, fields, Command, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class BillingSubscription(models.Model):
    _name = 'billing.subscription'
    _description = 'Billing Subscription'

    _recurring_amount_constraint = models.Constraint(
        'CHECK(recurring_amount > 0)',
        'Recurring amount should be greater than 0.'
    )

    name = fields.Char(string='Subscription Reference', default=lambda self: self.env['ir.sequence'].next_by_code('billing.subscription'))
    partner_id = fields.Many2one(comodel_name="res.partner", string='Customer', required=True)
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency", default=lambda self: self.env.company.currency_id)
    recurring_amount = fields.Monetary(currency_field="currency_id", string='Recurring Amount', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    stage = fields.Selection(selection=[
        ('draft','Draft'),
        ('active','Active'),
        ('closed','Closed'),
    ], default='draft', string='Stage', readonly=True)
    next_invoice_date = fields.Date(string='Next Invoice Date', readonly=True)
    recurrence = fields.Selection(
        selection=[
            ('monthly','Monthly'),
            ('yearly','Yearly'),
        ],
        string='Recurrence', required=True)

    @api.constrains('start_date')
    def _check_start_date(self):
        today = fields.Date.context_today(self)

        for record in self:
            if record.start_date < today:
                raise ValidationError("Start date should be today or a date ahead.")
    
    def action_active(self):
        today = fields.Date.context_today(self)

        for record in self:
            if record.stage != 'draft':
                raise UserError('Only a draft record can be activated.')
            
            # A draft that sat past its start date starts billing today,
            # not from the old date, so no backlog is billed.
            first_date = max(record.start_date, today)
            record.write({
                'stage': 'active',
                'start_date': first_date,
                'next_invoice_date': first_date
            })

    def action_closed(self):
        for record in self:
            if record.stage in ['draft','closed']:
                raise UserError('You cannot close draft or already closed billing subscription.')
            record.stage = 'closed'
    
    def _get_next_invoice_date(self):
        self.ensure_one()
        anchor_day = self.start_date.day
        if self.recurrence == 'monthly':
            step = relativedelta(months=1, day=anchor_day)
        else:
            step = relativedelta(years=1, day=anchor_day)
        return self.next_invoice_date + step

    @api.model
    def cron_recurring_billing_routine(self):
        today = fields.Date.context_today(self)
        active_records = self.search([('stage','=','active'),('next_invoice_date','<=',today)])

        for record in active_records:
            while record.next_invoice_date <= today:
                invoice = self.env['account.move'].create({
                    'partner_id': record.partner_id.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        Command.create({'name':f"Automated Recurring Renewal Invoice for Contract Ref: {record.name}",
                        'quantity': 1.0,
                        'price_unit': record.recurring_amount})
                    ]
                })

                invoice.action_post()
                
                record.next_invoice_date = record._get_next_invoice_date()
            