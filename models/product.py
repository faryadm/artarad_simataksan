# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductAttribute(models.Model):
    _inherit = "product.attribute.value"
    _description = "Product Attribute value"


    code=fields.Char(string='Attribute Value Prefix Code',help="this code add to product refrence code")


class ProductAttribute(models.Model):
    _inherit = "product.template"
    _description = "Product Template"


    pcode=fields.Char(string='Code')




class ProductProduct(models.Model):
    _inherit = "product.product"
    _description = "Product "

    # product_code=fields.Char(string='Code')
    # product_code=fields.Char(string='Code')

    @api.model
    def create(self,vals):
        res = super(ProductProduct, self).create(vals)
        gcode=res.pcode
        for variant in res.attribute_value_ids:
                gcode=(gcode or '')+(variant.code or '')
        res.default_code=gcode
