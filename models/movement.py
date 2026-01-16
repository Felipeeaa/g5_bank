# -*- coding: utf-8 -*-

from odoo import models, fields, api



class Movement(models.Model):

    _name = 'g5_bank.movement'
    _description = 'Movements'
    

    timesStamp = fields.Char()
    amount = fields.Integer()
    balance = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
    
    #Many2One    
    account_id = fields.Many2one('g5_bank.account',
        ondelete='set null', string="Account")
#
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:

#             record.value2 = float(record.value) / 100

