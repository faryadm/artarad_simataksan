# -*- coding: utf-8 -*-
{
    'name': "Artarad Simataksan",

    'summary': """
       Artarad Simataksan """,

    'description': """
        This module ..
    """,

    'author': "Artarad Team",
    'website': "http://www.Artarad.ir",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'web',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['web','product','mrp'],

    # always loaded
    'data': [
        'views/product.xml',
        'views/bom_view.xml',
    ],
     'qweb' : [

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}