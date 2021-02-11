from django.test import TestCase

from shop.models import Product


class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Product.objects.create(name='Sony TV - 1', price=500.0)

    def test_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        product = Product.objects.get(id=1)
        field_max_length = product._meta.get_field('name').max_length
        self.assertEquals(field_max_length, 250)

    def test_default_price(self):
        product = Product.objects.get(id=1)
        current_price = product._meta.get_field('price').default
        self.assertEquals(current_price, 0.0)

    def test_current_price(self):
        product = Product.objects.get(id=1)
        current_price = product.price
        self.assertEquals(current_price, 500.0)

    def test_get_absolute_url(self):
        product = Product.objects.get(id=1)
        self.assertEquals(product.get_absolute_url(), 'shop/product/1')
