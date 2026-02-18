# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Account(models.Model):
    _name = 'g5_bank.account'
    _description = 'Account'

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
	#FIXME Este campo pasa a tener como etiqueta "Descripción"
	#FIXME Su propósito no será almacenar el ID porque ya existe el campo id heredado de models.Model
    name = fields.Char(string="Description", required=True) 
    #FIXME Eliminar este campo del modelo y de las vistas
    #He eliminado el campo Description, tanto como en el campo modelo como en las vistas
    balance = fields.Monetary(
        string='Balance', 
        currency_field='currency_id', 
        compute='_compute_balance', 
        store=True
    )
    #FIXME Valida que credit line no pueda ser negativo
    #He corregido la validación en _check_balance_limit(self):
    creditLine = fields.Monetary(string='Credit Line', currency_field='currency_id', default=0.0)
    beginBalance = fields.Monetary(string='Begin Balance', currency_field='currency_id', required=True)
    beginBalanceTimestamp = fields.Datetime(string='Opening Date', default=fields.Datetime.now)
    
    typeAccount = fields.Selection([
        ('STANDARD', 'Standard'),
        ('CREDIT', 'Credit'),
    ], string='Account Type', required=True, default='STANDARD')

    # Relaciones
	#FIXME Asocia la cuenta con el usuario que está creando la cuenta cuando esta última se crea.
        #He corregido la asociacion del usuario
    g5_customer_ids = fields.Many2many('res.users', string='Customers', default=lambda self: [(6, 0, [self.env.user.id])], required=True) 
    g5_movement_ids = fields.One2many('g5_bank.movement', 'g5_account_id', string='Movements')
    movement_count = fields.Integer(compute='_compute_movement_count')

    #LÓGICA

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
    
    #He creado una condicion para que no se puedan borrar cuentas con movimientos
    def unlink(self):
        for record in self:
              if record.g5_movement_ids: 

                raise ValidationError("You cannot delete accounts with associated moves.") 

        return super(Account, self).unlink() 
	#FIXME: Eliminar las SQL_CONSTRAINTS

    @api.constrains('typeAccount', 'creditLine')
    def _check_credit_line_consistency(self):
        for record in self:
            if record.typeAccount == 'STANDARD' and record.creditLine > 0:
                raise ValidationError("A 'Standard' account cannot have a credit line.")
                
    #He mojorado las comprobaciones para que asi salgan los mensajes correctos
    @api.constrains('beginBalance', 'balance', 'creditLine')
    def _check_balance_limit(self): 

        for record in self: 

            if record.beginBalance < 0 and record.creditLine < 0: 

                raise ValidationError("Neither the opening balance nor the credit line can be negative.") 

            

            if record.beginBalance < 0: 

                raise ValidationError("The opening balance cannot be negative.") 

            

            if record.creditLine < 0: 

                raise ValidationError("The credit line cannot be negative.") 
            
    #He añadido una condicion para que salga como predefinido quien esta creando la cuenta        
    @api.constrains('g5_customer_ids') 
    def _check_customer_required(self): 
        for record in self: 
            if not record.g5_customer_ids: raise ValidationError("The account must have at least one customer associated.")