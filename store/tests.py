from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Cart, Product


class CartDeleteTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user('owner', password='pass-12345')
        self.other = User.objects.create_user('other', password='pass-12345')
        product = Product.objects.create(name='Chew Toy', price=10, description='Squeaky', image='products/toy.jpg')
        self.item = Cart.objects.create(user=self.owner, product=product, quantity=2)
        self.url = reverse('delete_cart', args=[self.item.id])

    def test_owner_can_remove_their_cart_item(self):
        self.client.login(username='owner', password='pass-12345')

        response = self.client.post(self.url)

        self.assertRedirects(response, reverse('cart'))
        self.assertFalse(Cart.objects.filter(id=self.item.id).exists())

    def test_cannot_remove_someone_elses_cart_item(self):
        self.client.login(username='other', password='pass-12345')

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Cart.objects.filter(id=self.item.id).exists())

    def test_must_be_logged_in(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('user-login'), response.url)
        self.assertTrue(Cart.objects.filter(id=self.item.id).exists())

    def test_get_request_does_not_remove(self):
        self.client.login(username='owner', password='pass-12345')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Cart.objects.filter(id=self.item.id).exists())


class CartPageTests(TestCase):

    def test_cart_has_no_placeholder_tax_line(self):
        user = User.objects.create_user('shopper', password='pass-12345')
        product = Product.objects.create(name='Chew Toy', price=10, description='Squeaky', image='products/toy.jpg')
        Cart.objects.create(user=user, product=product, quantity=2)
        self.client.login(username='shopper', password='pass-12345')

        response = self.client.get(reverse('cart'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Tax')
