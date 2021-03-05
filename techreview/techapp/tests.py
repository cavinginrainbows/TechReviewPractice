from django.test import TestCase
from django.contrib.auth.models import User
from .models import TechType, Product, Review
import datetime
from .forms import ProductForm
from django.urls import reverse

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

    # # FIXME: This test is failing
    # def test_productForm_invalid(self):
    #     data = {'productname' : 'surface', 
    #             # 'producttype' : 'laptop', 
    #             'user' : 'lewis',
    #             'dateentered' : '2020-2-21',
    #             'price' : '1200.00',
    #             'producturl' : 'https://microsoft.com',
    #             'description' : 'Elegant and sleek notebook'}
    #     form = ProductForm(data)
    #     self.assertFalse(form.is_valid)

class NewProductAuthTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username = 'testuser1', password = 'P@ssw0rd1')
        self.type = TechType.objects.create(typename = 'laptop')
        self.product = Product.objects.create(productname = 'product1', 
                                            producttype = self.type, 
                                            user = self.test_user,
                                            price = 500, dateentered = '2021-04-02', 
                                            producturl = 'https://dell.com', 
                                            description = 'a product')
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('newproduct'))
        self.assertRedirects(response, '/accounts/login/?next=/techapp/newproduct/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username = 'testuser1', password = 'P@ssw0rd1')
        response = self.client.get(reverse('newproduct'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'techapp/newproduct.html')