# -*- coding: utf-8 -*-
{
    'name': "FMD Bank",
    'application' : True,
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """

        Module in charge of creating, reading, updating and deleting
	the introduced customers, accounts and movements of a bank.
	Admin users having the privileges of managing all data, while
	common users can just manage its own information 
    """,

    'author': "FMD_Bank",
    'website':"https://site.educa.madrid.org/ies.sanjuandelacruz.pozuelodealarcon/ ",


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security_rules.xml',
        'views/accountMenu.xml',
        'views/movementMenu.xml',
        'views/customerMenu.xml',
        'views/reports.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
