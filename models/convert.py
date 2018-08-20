# -*- coding: utf-8 -*-

from odoo import models, fields,_,api
from xlrd import open_workbook
import os.path
class Convert(models.Model):
    _name="artarad.convert"

    def import_category_level2(self):
        # wb = open_workbook(os.path.join('D:\\Odoo\\Odoo Customers\\Simataksan\\Convert\\', 'Category Level2.xlsx'))
        wb = open_workbook('../convert/CategoryLevel2.xlsx')
        wb.sheet_names()
        sh = wb.sheet_by_index(0)
        for i in range(1, sh.nrows):
            product_cat=self.env['product.category'].search([('name','=',sh.cell(i,1).value.strip())])
            if not product_cat:
                parent=self.env['product.category'].search([('name','=',sh.cell(i,0).value.strip())])
                vals = {
                    'name':sh.cell(i,1).value.strip(),
                    'parent_id':parent.id

                }
                self.env['product.category'].create(vals)
    def import_product(self):
        # wb = open_workbook(os.path.join('D:\\Odoo\\Odoo Customers\\Simataksan\\Convert\\', 'Products.xlsx'))
        wb = open_workbook('../convert/Products.xlsx')
        wb.sheet_names()
        sh = wb.sheet_by_index(0)
        print('total rows:'+str(sh.nrows))
        products=[]
        for i in range(1, sh.nrows):
            unit=self.env['product.uom'].search([('name','=',sh.cell(i,2).value.strip())])
            categ=self.env['product.category'].search([('name','=',sh.cell(i,4).value.strip())])
            vals = {
                    'name':sh.cell(i,1).value.strip(),
                    'uom_id':unit.id,
                    'uom_po_id':unit.id,
                    'default_code':str(sh.cell(i,0).value).strip(),
                    'categ_id':categ.id,


                }
            products.append(vals)
        print('list created.')
        for vals in products :
            p=self.env['product.template'].create(vals)
            print(p.id)
            self._cr.commit()
