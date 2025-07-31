from odoo import http
from odoo.http import request, Response
import json
import werkzeug

class MaterialController(http.Controller):
    @http.route('/api/materials', type='json', auth='public', methods=['GET'], csrf=False)
    def get_materials(self, **kwargs):
        try:
            material_type = kwargs.get('type')
            domain = []
            if material_type:
                domain = [('type', '=', material_type)]
                
            materials = request.env['material.material'].sudo().search(domain)
            result = []
            for material in materials:
                result.append({
                    'id': material.id,
                    'code': material.code,
                    'name': material.name,
                    'type': material.type,
                    'buy_price': material.buy_price,
                    'supplier_id': material.supplier_id.id,
                    'supplier_name': material.supplier_id.name
                })
            return result
        except Exception as e:
            return str(e)

    @http.route('/api/materials',type='json', auth='public', methods=['POST'], csrf=False)
    def create_material(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            material = request.env['material.material'].sudo().create({
                'name': data.get('name'),
                'type': data.get('type'),
                'buy_price': float(data.get('buy_price')),
                'supplier_id': int(data.get('supplier_id')),
            })
            return {
                'id': material.id,
                'code': material.code,
                'name': material.name,
                'type': material.type,
                'buy_price': material.buy_price,
                'supplier_id': material.supplier_id.id,
                'supplier_name': material.supplier_id.name
            }

        except Exception as e:
            request.env.cr.rollback()
            return str(e)
    
    @http.route('/api/materials/<int:id>',type='json', auth='public', methods=['PUT'], csrf=False)
    def update_material(self, id, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            material = request.env['material.material'].sudo().browse(id)
            if not material.exists():
                return Response(json.dumps({'success': False, 'error': 'Material not found'}), 
                              status=404, content_type='application/json')
            
            material.sudo().write({
                'code': data.get('code', material.code),
                'name': data.get('name', material.name),
                'type': data.get('type', material.type),
                'buy_price': float(data.get('buy_price', material.buy_price)),
                'supplier_id': int(data.get('supplier_id', material.supplier_id.id)),
            })
            return {
                'id': id,
                'code': material.code,
                'name': material.name,
                'type': material.type,
                'buy_price': material.buy_price,
                'supplier_id': material.supplier_id.id,
                'supplier_name': material.supplier_id.name
            }
        except Exception as e:
            request.env.cr.rollback()
            return str(e)
    
    @http.route('/api/materials/<int:id>', type='json', auth='public', methods=['DELETE'], csrf=False)
    def delete_material(self, id, **kwargs):
        try:
            material = request.env['material.material'].browse(id)
            if not material.exists():
                return Response(json.dumps({'success': False, 'error': 'Material not found'}), 
                              status=404, content_type='application/json')
            material.unlink()
            return {'success': True}

        except Exception as e:
            request.env.cr.rollback()
            return str(e)