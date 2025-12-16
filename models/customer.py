# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Customer(models.Model):
     _name = 'g5_bank.customer'
     _description = 'Customer'
     _inherit = res.users

     account_ids = fields.Many2Many("g5_bank.account", string="Accounts")