# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Account(models.Model):
    _name = 'g5_bank.account'
    _description = 'Account'

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    name = fields.Char(string="Account ID") 
    
    description = fields.Text(string="Description", required=True)
    
    balance = fields.Monetary(
        string='Balance', 
        currency_field='currency_id', 
        compute='_compute_balance', 
        store=True
    )
    
    creditLine = fields.Monetary(string='Credit Line', currency_field='currency_id', default=0.0)
    beginBalance = fields.Monetary(string='Begin Balance', currency_field='currency_id', required=True)
    beginBalanceTimestamp = fields.Datetime(string='Opening Date', default=fields.Datetime.now)
    
    typeAccount = fields.Selection([
        ('STANDARD', 'Standard'),
        ('CREDIT', 'Credit'),
    ], string='Account Type', required=True, default='STANDARD')

    # Relaciones
    g5_customer_ids = fields.Many2many('res.users', string='Customers')
    g5_movement_ids = fields.One2many('g5_bank.movement', 'g5_account_id', string='Movements')
    movement_count = fields.Integer(compute='_compute_movement_count')

    # --- LÓGICA DE NEGOCIO ---

    @api.depends('beginBalance', 'g5_movement_ids.amount')
    def _compute_balance(self):
        for record in self:
            total_movements = sum(move.amount for move in record.g5_movement_ids)
            record.balance = record.beginBalance + total_movements

    @api.depends('g5_movement_ids')
    def _compute_movement_count(self):
        for record in self:
            record.movement_count = len(record.g5_movement_ids)


    @api.model
    def create(self, vals):
        # Si es tipo STANDARD, se fuerza el creditLine a 0 para evitar errores
        if vals.get('typeAccount') == 'STANDARD':
            vals['creditLine'] = 0.0
            
        # Si es de tipo CREDIT, se respeta el valor
        
        return super(Account, self).create(vals)
    #Validaciones
    def write(self, vals):
        
        if 'beginBalance' in vals:
             raise ValidationError("Modifying the Opening Balance (beginBalance) is not allowed once the account is created.")
        if 'typeAccount' in vals:
             raise ValidationError("Modifying the Account Type (typeAccount) is not allowed.")
        if 'balance' in vals:
             raise ValidationError("You cannot modify the Balance directly; please add a movement instead.")

        return super(Account, self).write(vals)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The account name must be unique.'),
        ('credit_line_positive', 'CHECK(creditLine >= 0)', 'The credit line cannot be negative.'),
    ]

    @api.constrains('typeAccount', 'creditLine')
    def _check_credit_line_consistency(self):
        for record in self:
            if record.typeAccount == 'STANDARD' and record.creditLine > 0:
                raise ValidationError("A 'Standard' account cannot have a credit line.")

    @api.constrains('balance', 'creditLine')
    def _check_balance_limit(self):
        for record in self:
            if record.balance < (-record.creditLine):
                raise ValidationError("The balance cannot be lower than the allowed credit limit (-{}).".format(record.creditLine))