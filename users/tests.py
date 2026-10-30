from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Product, Review


class ReviewDeleteTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user('owner', password='pass-12345')
        self.other = User.objects.create_user('other', password='pass-12345')
        product = Product.objects.create(name='Chew Toy', price=10, description='Squeaky', image='products/toy.jpg')
        self.review = Review.objects.create(user=self.owner, product=product, rating=5, review='Great')
        self.url = reverse('user-review-delete', args=[self.review.id])

    def test_owner_can_delete_their_review(self):
        self.client.login(username='owner', password='pass-12345')

        response = self.client.post(self.url)

        self.assertRedirects(response, reverse('user-profile'))
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_cannot_delete_someone_elses_review(self):
        self.client.login(username='other', password='pass-12345')

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Review.objects.filter(id=self.review.id).exists())

    def test_must_be_logged_in(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('user-login'), response.url)
        self.assertTrue(Review.objects.filter(id=self.review.id).exists())

    def test_get_request_does_not_delete(self):
        # Deleting through a plain link would let another website trigger it
        self.client.login(username='owner', password='pass-12345')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Review.objects.filter(id=self.review.id).exists())
