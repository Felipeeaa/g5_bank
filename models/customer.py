# -*- coding: utf-8 -*-
import re  # <--- Necesario para validar expresiones regulares (email)
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Customer(models.Model):
    _description = 'Customer'
    _inherit = 'res.users'

    g5_account_ids = fields.Many2many("g5_bank.account", string="Account")

    # --- Validación del código postal (ZIP) ---
    @api.constrains('zip')
    def _check_zip_validation(self):
        for record in self:
            if record.zip:
                if not record.zip.isdigit():
                    raise ValidationError("El código postal debe contener únicamente números.")
                if len(record.zip) > 5:
                    raise ValidationError("El código postal no puede tener más de 5 dígitos.")

    # --- Validación del correo (Login) ---
    @api.constrains('login')
    def _check_login_validation(self):
        for record in self:
            if record.login:
                # Explicación del patrón regex r"^.+@.+\..+$":
                # ^      : Empieza la cadena
                # .+     : Al menos un carácter cualquiera
                # @      : Una arroba
                # .+     : Al menos un carácter (el dominio)
                # \.     : Un punto literal
                # .+     : Al menos un carácter (la extensión .com, .es, etc)
                match = re.match(r"^.+@.+\..+$", record.login)
                
                if not match:
                    raise ValidationError("El correo electrónico debe tener un formato válido (ejemplo: usuario@dominio.com).")
                
    @api.constrains('mobile')
    def _check_mobile_validation(self):
        for record in self:
            if not record.mobile.isdigit():
                raise ValidationError("El numero de telefono debe contener unicamente numeros")