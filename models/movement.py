# -*- coding: utf-8 -*-

from odoo import models, fields, api



class Movement(models.Model):

    _name = 'g5_bank.movement'
    _description = 'Movements'
    
    urrency_id = fields.Many2one('res.currency', string='Currency', 
                                  default=lambda self: self.env.company.currency_id)

    timesStamp = fields.Datetime(string='Date', default=fields.Datetime.now)
    
    amount = fields.Monetary(string='Amount', currency_field='currency_id', default=0.0)
    
    balance = fields.Monetary(string='Balance', 
        compute='_compute_balance', currency_field='currency_id', default=0.0, readonly=True)
        
    description = fields.Selection([
                                   ('DEPOSIT', 'Deposit'),
                                   ('PAYMENT', 'Payment'),
                                   ], string='Movement Type', required=True, default='')
    
    #Many2One    
    g5_account_id = fields.Many2one('g5_bank.account', string="Account")
