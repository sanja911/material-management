from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Material(models.Model):
    _name = 'material.material'
    _description = 'Material'
    
    code = fields.Char(string='Material Code', required=True, default=lambda self: self._generate_material_code(),)
    name = fields.Char(string='Material Name', required=True)
    type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton'),
    ], string='Material Type', required=True)
    buy_price = fields.Float(string='Material Buy Price', required=True)
    supplier_id = fields.Many2one('res.partner', string='Related Supplier', 
                                domain=[('is_company', '=', True)], required=True)
    
    @api.model
    def _generate_material_code(self):
        return self.env['ir.sequence'].next_by_code('material.material.code') or _('New')

    @api.constrains('buy_price')
    def _check_buy_price(self):
        for record in self:
            if record.buy_price < 100:
                raise ValidationError(_('Material Buy Price cannot be less than 100'))
    
    def name_get(self):
        result = []
        for material in self:
            name = f"[{material.code}] {material.name}"
            result.append((material.id, name))
        return result