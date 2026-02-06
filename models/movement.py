# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Movement(models.Model):

    _name = 'g5_bank.movement'
    _description = 'Movements'
    

    timesStamp = fields.Datetime(string='Date',readonly=True, default=fields.Datetime.now)
    amount = fields.Float(string='Amount', default=0.0,required=True)
    balance = fields.Float(string='Balance', 
        compute='_compute_balance', default=0.0, readonly=True)
        
    description = fields.Selection([
                                   ('DEPOSIT', 'Deposit'),
                                   ('PAYMENT', 'Payment'),
                                   ], string='Movement Type', required=True, default='')
    
    #Many2One    
    g5_account_id = fields.Many2one('g5_bank.account', string="Account")