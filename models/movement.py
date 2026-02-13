# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Movement(models.Model):

    _name = 'g5_bank.movement'
    _description = 'Movements'
    

    timesStamp = fields.Datetime(string='Date',readonly=True, default=fields.Datetime.now)
    amount = fields.Float(string='Amount', default=0.0,required=True)
    #FIXME No existe método de cálculo para este campo calculado
	balance = fields.Float(string='Balance', 
        compute='_compute_balance', default=0.0, readonly=True)
        
    description = fields.Selection([
                                   ('DEPOSIT', 'Deposit'),
                                   ('PAYMENT', 'Payment'),
                                   ], string='Movement Type', required=True, default='')
    
    #Many2One    
    g5_account_id = fields.Many2one('g5_bank.account', string="Account")
	
	#FIXME No hay ninguna validación de Amount
	
	#FIXME: Hay que actualizar el saldo de la cuenta al crear el movimiento.
	#Para esto tendrás que definir un método:
	#@api.model_create_multi
	#def create(self, vals_list):
        ## lógica antes de crear
        #records = super().create(vals_list)
        ## lógica después de crear
        #return records
	
	
	#FIXME: Controla que solo se pueda borrar el último movimiento
	#Para esto tendrás que definir un método:
	#def unlink(self):
    ## lógica antes de borrar
    #return super().unlink()
