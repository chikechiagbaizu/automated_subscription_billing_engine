from odoo import models, fields, Command

class SaleSubscription(models.Model):
    _name = 'sale.subscription'
    _description = 'Sale Subscription'

    name = fields.Char(string='Subscription ID', required=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string='Partner ID', required=True)
    recurring_amount = fields.Float(string='Recurring Amount')
    date_start = fields.Date(string='Start Date', required=True)
    stage = fields.Selection(selection=[
        ('draft','Draft'),
        ('active','Active'),
        ('closed','Closed'),
    ], default='draft', string='Stage')

    def cron_recurring_billing_routine(self):
        active_records = self.env['sale.subscription'].search([('stage','=','active')])

        for record in active_records: 
            self.env['account.move'].create({
                'partner_id': record.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({'name':f"Automated Recurring Renewal Invoice for Contract Ref: {record.name}",
                    'quantity':1.0,
                    'price_unit':record.recurring_amount})
                ]
            })