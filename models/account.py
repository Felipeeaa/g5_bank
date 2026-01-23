# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Account(models.Model):
     _name = 'g5_bank.account'
     _description = 'Account'

     name = fields.Char()
     value = fields.Integer()
     value2 = fields.Float(compute="_value_pc", store=True)
     description = fields.Text()
     g5_customer_ids = fields.Many2many("g5_bank.customer", String = "Customer" )
     g5_movement_ids = fields.One2many("g5_bank.movement", "g5_account_id", String = "Movements")

