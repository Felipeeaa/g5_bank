# -*- coding: utf-8 -*-
import enum
from odoo import api, fields, models

class Account(models.Model):
    _name = 'g5_bank.account'
    _description = 'Account'

# Campo técnico necesario para Monetary
    currency_id = fields.Many2one('res.currency', string='Currency', 
                                  default=lambda self: self.env.company.currency_id)
# El id lo da predeterminado Odoo (es decir lo añade automático)                                 
    name = fields.Char()
    description = fields.Text(required=True)
    balance = fields.Monetary(string='Balance', currency_field='currency_id', default=0.0)
    creditLine = fields.Monetary(string='Credit Line', currency_field='currency_id', default=0.0)
    beginBalance = fields.Monetary(string='Begin Balance', currency_field='currency_id', required=True)
    beginBalanceTimestamp = fields.Datetime(string='Opening Date', default=fields.Datetime.now)
    
# Eleccion del tipo de la cuenta
    typeAccount = fields.Selection([
                                   ('STANDARD', 'Standard'),
                                   ('CREDIT', 'Credit'),
                                   ], string='Account Type', required=True, default='STANDARD')

#Relaciones de Customer (muchos amuchos) y de Movement (uno a muchos)                                   
    g5_customer_ids = fields.Many2many('res.users', string='Customer')
    g5_movement_ids = fields.One2many('g5_bank.movement', 'g5_account_id', string='Movements')