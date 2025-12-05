# -*- coding: utf-8 -*-
# from odoo import http


# class G5Bank(http.Controller):
#     @http.route('/g5_bank/g5_bank', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/g5_bank/g5_bank/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('g5_bank.listing', {
#             'root': '/g5_bank/g5_bank',
#             'objects': http.request.env['g5_bank.g5_bank'].search([]),
#         })

#     @http.route('/g5_bank/g5_bank/objects/<model("g5_bank.g5_bank"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('g5_bank.object', {
#             'object': obj
#         })
