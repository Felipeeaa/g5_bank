# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Movement(models.Model):

    _name = 'g5_bank.movement'
    _description = 'Movements'
    
    #Many2One    
    g5_account_id = fields.Many2one('g5_bank.account', string="Account")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    
    timesStamp = fields.Datetime(string='Date',readonly=True, default=fields.Datetime.now)
    description = fields.Selection([
                                   ('DEPOSIT', 'Deposit'),
                                   ('PAYMENT', 'Payment'),
                                   ], string='Movement Type', required=True, default='')
    amount = fields.Float(string='Amount', default=0.0,required=True)
    #FIXME No existe método de cálculo para este campo calculado
    #balance = fields.Monetary(string="Balance", currency_field='currency_id', readonly=True)
    balance = fields.Float(string='Balance', compute='_compute_balance', default=0.0, readonly=True)
    #Calculo del balance
    @api.depends('g5_account_id.beginBalance', 'g5_account_id.balance')
    def _compute_balance(self):
         for b in self:
            if b.type_account == 'STANDARD':
                b.credito_disponible = 0.0	
        
    #FIXME No hay ninguna validación de Amount
    @api.constrains('amount', 'description', 'g5_account_id')
    def amount_validation(self):
        for m in self:
            if m.amount <= 0:
                raise ValidationError("Amount must be more than 0.")
            # Validación de fondos
            if m.description == 'PAYMENT':
                saldo = m.g5_account_id.beginBalance
                for m2 in m.g5_account_id.movement_ids:
                    if m2.id != m.id and m2._origin.id != m.id:
                        if m2.description == 'DEPOSIT':
                            saldo += m2.amount
                        elif m2.description == 'PAYMENT':
                            saldo -= m2.amount
                
                credito = m.g5_account_id.creditLine if m.g5_account_id.typeAccount == 'CREDIT' else 0.0
                total_disponible = saldo + credito

                if m.amount > total_disponible:
                    raise ValidationError(
                        "Insufficient amount.\n"
                        "Available: %.2f (Balance: %.2f + Credit: %.2f)\n"
                        "Attempted payment: %.2f" % 
                        (total_disponible, saldo, credito, m.amount)
                    )
                    
	#FIXME: Hay que actualizar el saldo de la cuenta al crear el movimiento.
	#Para esto tendrás que definir un método:
	#@api.model_create_multi
	#def create(self, vals_list):
        ## lógica antes de crear
        #records = super().create(vals_list)
        ## lógica después de crear
        #return records
	#variables de account
        
    @api.model_create_multi
    def create(self, vals_list):
        records = super(Movement, self).create(vals_list)
        for record in records:
            if record.g5_account_id:
                record.balance = record.g5_account_id.balance
        return records
    	
	#FIXME: Controla que solo se pueda borrar el último movimiento
	#Para esto tendrás que definir un método:
	#def unlink(self):
        ## lógica antes de borrar
        #return super().unlink()
    def unlink(self):
        for record in self:
            #ultimo movimiento
            last_movement = self.search([
                ('g5_account_id', '=', record.g5_account_id.id)
            ], order='timesStamp desc, id desc', limit=1)

            if record.id != last_movement.id:
                raise ValidationError("You can only delete the last movement.")
                    
            last_amount = record.amount if record.description == 'DEPOSIT' else -record.amount
            record.g5_account_id.balance -= last_amount

        return super(Movement, self).unlink()
