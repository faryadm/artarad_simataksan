# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning,UserError

def combs(pools):
    # combs(['ABCD', 'xy']) --> Ax Ay Bx By Cx Cy Dx Dy
    result = [set([])]
    for pool in pools:
      tmp=[]
      for y in pool:
        for x in result:
         tmp.append(x|set([y]) )
      result = tmp
    return result

class MrpBom(models.Model):
    _inherit='mrp.bom'


    product_template_ids = fields.One2many('bom.product.template.line', 'bom_id', 'BoM Products', copy=True)
    bom_status= fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], default="draft",string="Bom Status")

    # my code
    # def create_bom_line(self):
    #     for rec in self:
    #         rec.bom_line_ids=[]
    #         mainatt=[]
    #         for attline in rec.product_tmpl_id.attribute_line_ids:
    #             mainatt.append(attline.attribute_id.id)
    #
    #         mainvar=[]
    #         for mvar in rec.product_tmpl_id.product_variant_ids:
    #             mainvar.append(mvar.attribute_value_ids.ids)
    #
    #         for pt in rec.product_template_ids:
    #                 subatt=[]
    #                 for attline in pt.product_id.attribute_line_ids:
    #                      subatt.append(attline.attribute_id.id)
    #                 b3 = [val for val in mainatt if val in subatt]
    #                 # for id in b3:
    #                 allvalue=self.env['product.attribute.value'].search([('attribute_id','in',b3)]).ids
    #                 mainval=[]
    #                 for mvar in mainvar:
    #                    tmp=[]
    #                    for mvarid in mvar:
    #                        if mvarid in allvalue:
    #                            tmp.append(mvarid)
    #                    if tmp not in mainval:
    #                         mainval.append(tmp)
    #
    #
    #
    #                 for pv in pt.product_id.product_variant_ids:
    #
    #                     subvar=pv.attribute_value_ids.ids
    #
    #
    #                     for item in mainval:
    #                             if set(item)<=set(subvar):
    #                                 self.env['mrp.bom.line'].create({
    #                                     'bom_id': rec.id,
    #                                     'product_id': pv.id,
    #                                     'product_qty': pt.qty,
    #                                     'attribute_value_ids': [(6,0, item)],
    #                                      })
    #                 # create product template as sub prdouct of bom




    def create_bom_line(self):


        self.env['mrp.bom.line'].search([('bom_id', '=', self.ids[0])]).unlink()

        for bomt_line in self.product_template_ids:

          var_atts=[] # list of lists(sets)  # valid attribute_values of each attribute (multi_value_atts)
          single_value_atts = []

          for protem_att_line in bomt_line.product_id.attribute_line_ids:
              aa = set(protem_att_line.value_ids) & set(bomt_line.component_variant_ids)
              if aa:     #if child template have a filter in this att
                if len(aa)>1:
                  raise UserError(_('Warning 1 %s' %protem_att_line.name))
                single_value_atts += list(aa)
              elif len(protem_att_line.value_ids)==1:
                single_value_atts += protem_att_line.value_ids
              else:
                att_line_parent=bomt_line.bom_id.product_tmpl_id.attribute_line_ids.filtered(lambda att_li: att_li.attribute_id == protem_att_line.attribute_id)
                if not att_line_parent:
                     raise UserError(_('Please derermine this attribute : %s'%protem_att_line.attribute_id.name ))
                else:
                    att_line_parent=att_line_parent[0]
                if set(protem_att_line.value_ids) >= set(att_line_parent.value_ids):
                  var_atts.append(set(protem_att_line.value_ids) & set(att_line_parent.value_ids))
                else:
                  raise UserError(_('Error 2 %s' %bomt_line.product_id.name))


          var_atts = combs(var_atts) #posible variant_value combinations
          single_value_atts = set(single_value_atts)

          all_vars = self.env['product.product'].search([('product_tmpl_id', '=', int(bomt_line.product_id))])
          for p_var in all_vars:
            if set(p_var.attribute_value_ids)-single_value_atts in var_atts:
              bline = {}
              bline['bom_id'] = int(bomt_line.bom_id)
              bline['product_id'] = int(p_var)
              bline['product_qty'] = bomt_line.qty
              bline['attribute_value_ids'] = [(6,0, [int(AV) for AV in (set(p_var.attribute_value_ids)-single_value_atts)|set(bomt_line.p_variant_ids)] )]
              self.env['mrp.bom.line'].create(bline)

class MrpBomProductTemplateLine(models.Model):
    _name='bom.product.template.line'



    bom_id=fields.Many2one('mrp.bom',string="Bom")
    product_id=fields.Many2one('product.template',"Component Template")
    qty=fields.Integer(string="QTY",default=1)
    component_variant_ids=fields.Many2many('product.attribute.value','bom_line_attribute_line_rel','bomline_id','att_id',string="Component Variants",)
    p_variant_ids=fields.Many2many('product.attribute.value','bom_line_attribute_line_rel2','bomline_id','att_id',string="Product Variants",)