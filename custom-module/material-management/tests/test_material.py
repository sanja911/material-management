from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestMaterial(TransactionCase):
    
    def setUp(self):
        super(TestMaterial, self).setUp()
        self.Material = self.env['material.material']
        self.supplier = self.env['res.partner'].create({
            'name': 'Test Supplier',
            'is_company': True,
            'is_material_supplier': True,
        })
        
        self.valid_material = {
            'name': 'Test Material',
            'type': 'fabric',
            'buy_price': 150,
            'supplier_id': self.supplier.id,
        }
    
    def test_create_material(self):
        """Test creation of valid material"""
        material = self.Material.create(self.valid_material)
        self.assertEqual(material.name, 'Test Material')
        self.assertEqual(material.type, 'fabric')
        self.assertEqual(material.buy_price, 150)
        self.assertEqual(material.supplier_id.id, self.supplier.id)
    
    def test_price_validation(self):
        """Test price validation (must be >= 100)"""
        with self.assertRaises(ValidationError):
            invalid_material = self.valid_material.copy()
            invalid_material['buy_price'] = 99
            self.Material.create(invalid_material)
      
    def test_update_material(self):
        """Test updating material"""
        material = self.Material.create(self.valid_material)
        material.write({'name': 'Updated Material'})
        self.assertEqual(material.name, 'Updated Material')
    
    def test_delete_material(self):
        """Test deleting material"""
        material = self.Material.create(self.valid_material)
        material_id = material.id
        material.unlink()
        self.assertFalse(self.Material.browse(material_id).exists())
    
    def test_filter_by_type(self):
        """Test filtering by material type"""
        # Clear existing test data
        self.Material.search([]).unlink()
        
        # Create test materials
        fabric_material = self.valid_material.copy()
        self.Material.create(fabric_material)
        
        jeans_material = self.valid_material.copy()
        jeans_material.update({
            'name': 'Jeans Material',
            'type': 'jeans',
        })
        self.Material.create(jeans_material)
        
        # Test filtering
        fabric_materials = self.Material.search([('type', '=', 'fabric')])
        self.assertEqual(len(fabric_materials), 1)
        self.assertEqual(fabric_materials[0].type, 'fabric')
        
        jeans_materials = self.Material.search([('type', '=', 'jeans')])
        self.assertEqual(len(jeans_materials), 1)
        self.assertEqual(jeans_materials[0].type, 'jeans')