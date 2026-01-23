# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Customer(models.Model):
     _description = 'Customer'
     _inherit = 'res.users'

     g5_account_ids = fields.Many2many("g5_bank.account", String = "Account")
     
     
