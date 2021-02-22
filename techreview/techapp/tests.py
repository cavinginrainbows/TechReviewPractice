from django.test import TestCase
from django.contrib.auth.models import User
from .models import TechType, Product, Review
import datetime
from .forms import ProductForm

# Create your tests here.
class TechTypeTest(TestCase):
    def setUp(self):
        self.type = TechType(typename='Lenovo Laptop')

    def test_typestring(self):
        self.assertEqual(str(self.type), 'Lenovo Laptop')

    def test_tablename(self):
        self.assertEqual(str(TechType._meta.db_table), 'techtype')


class ProductTest(TestCase):
    def setUp(self):
        self.type = TechType(typename = 'Laptop')
        self.user = User(username = 'user1')
        self.product = Product(productname = 'Lenovo', 
                               producttype = self.type, 
                               user = self.user,
                               dateentered = datetime.date(2021, 1, 10),
                               price = 1200.99,
                               producturl = 'https://lenovo.com',
                               description = 'simple lappy')
    
    def test_string(self):
        self.assertEqual(str(self.product), 'Lenovo')
    
    def test_discount(self):
        disc = self.product.price * .05
        self.assertEqual(self.product.discountAmount(), disc)
    
    def test_discountedAmount(self):
        newprice = self.product.price * .95
        self.assertEqual(self.product.discountPrice(), newprice)


class NewProductForm(TestCase):
    def test_productForm(self):
        data = {'productname' : 'surface', 
                'producttype' : 'laptop', 
                'user' : 'lewis',
                'dateentered' : '2020-2-21',
                'price' : '1200.00',
                'producturl' : 'https://microsoft.com',
                'description' : 'Elegant and sleek notebook'}
        form = ProductForm(data)
        self.assertTrue(form.is_valid)

    # FIXME: This test is failing
    def test_productForm_invalid(self):
        data = {'productname' : 'surface', 
                # 'producttype' : 'laptop', 
                'user' : 'lewis',
                'dateentered' : '2020-2-21',
                'price' : '1200.00',
                'producturl' : 'https://microsoft.com',
                'description' : 'Elegant and sleek notebook'}
        form = ProductForm(data)
        self.assertFalse(form.is_valid)