#!/usr/bin/python3

import unittest
from models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):
    def test_init(self):
        my_module = BaseModel()
        self.assertIsNotNone(my_module.id)
        self.assertIsNotNone(my_module.created_at)
        self.assertIsNotNone(my_module.updated_at)
        
    def test_save(self):
        my_module = BaseModel()
        
        init_updated_at = my_module.updated_at
        
        curr_updated_at = my_module.save()
        
        self.assertNotEqual(init_updated_at, curr_updated_at)

    def test_to_dict(self):
        my_module = BaseModel()

        my_module_dict = my_module.to_dict()
        self.assertIsInstance(my_module_dict, dict)

        self.assertEqual(my_module_dict["__class__"], 'BaseModel')
        self.assertEqual(my_module_dict["id"], my_module.id)
        self.assertEqual(my_module_dict["created_at"], my_module.created_at.isoformat())
        self.assertEqual(my_module_dict["updated_at"], my_module.updated_at.isoformat())

    def test_str(self):
        my_module = BaseModel()
        
        self.assertTrue(str(my_module).startswith('[BaseModel]'))
        
        self.assertIn(my_module.id, str(my_module))
        
        self.assertIn(str(my_module.__dict__), str(my_module))

if __name__ == "__main__":
    unittest.main()
