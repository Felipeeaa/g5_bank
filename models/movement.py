# -*- coding: utf-8 -*-

from odoo import models, fields, api


class g5_bank(models.Model):
    _name = 'g5_bank.movement'
    _description = 'Movements'
    

    timesStamp = fields.Char()
    amount = fields.Integer()
    balance = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
    
#Many2One    
    esponsible_id = fields.Many2one('res.users',
        ondelete='set null', string="Responsible"

        )
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
