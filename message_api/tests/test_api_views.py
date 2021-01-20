from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from accounts.models import User
from message_api import models, api_views


class MessageTest(TestCase):

	def setUp(self) -> None:
		self.superuser = User.objects.create_superuser(
			'mgajewski19@gmail.com',
			password='Pass!234'
		)
		self.client = APIRequestFactory()
		self.test_message = models.Message.objects.create(
			slug='test',
			text='Test message',
			counter=2
		)

	def test_retrieve(self):
		request = self.client.get(
			reverse('api:message-detail', kwargs={
				'slug': self.test_message.slug
			})
		)
		retrieve_view = api_views.MessageViewSet.as_view(
			{'get': 'retrieve'}
		)

		response = retrieve_view(request, slug=self.test_message.slug)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data.get('text'), self.test_message.text)

	def test_create_authorized(self):
		request = self.client.post(
			reverse('api:message-list'),
			data={
				'slug': 'hello-world',
				'text': 'Oh hello!'
			}
		)
		force_authenticate(request, user=self.superuser)
		create_view = api_views.MessageViewSet.as_view(
			{'post': 'create'}
		)

		response = create_view(request)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data.get('counter'), 0)

	def test_create_unauthorized(self):
		request = self.client.post(
			reverse('api:message-list'),
			data={
				'slug': 'wrong',
				'text': 'You should`t see that'
			}
		)

		create_view = api_views.MessageViewSet.as_view(
			{'post': 'create'}
		)

		response = create_view(request)
		self.assertEqual(response.status_code, 401)

	def test_update_authorized(self):
		request = self.client.patch(
			reverse('api:message-detail', kwargs={
				'slug': self.test_message.slug
			}),
			data={
				'slug': 'changed-one',
				'text': 'Im changed yeaa'
			}
		)
		force_authenticate(request, user=self.superuser)

		update_view = api_views.MessageViewSet.as_view(
			{'patch': 'update'}
		)

		response = update_view(request, slug=self.test_message.slug)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data.get('counter'), 0)

	def test_update_unauthorized(self):
		request = self.client.patch(
			reverse('api:message-detail', kwargs={
				'slug': self.test_message.slug
			}),
			data={
				'slug': 'nope',
				'text': 'Not today my friend'
			}
		)

		update_view = api_views.MessageViewSet.as_view(
			{'patch': 'update'}
		)

		response = update_view(request, slug=self.test_message.slug)
		self.assertEqual(response.status_code, 401)

	def test_delete_authorized(self):
		request = self.client.delete(
			reverse('api:message-detail', kwargs={
				'slug': self.test_message.slug
			}),
		)
		force_authenticate(request, user=self.superuser)

		delete_view = api_views.MessageViewSet.as_view(
			{'delete': 'destroy'}
		)

		response = delete_view(request, slug=self.test_message.slug)

		self.assertEqual(response.status_code, 204)

	def test_delete_unauthorized(self):
		request = self.client.delete(
			reverse('api:message-detail', kwargs={
				'slug': self.test_message.slug
			}),
		)

		delete_view = api_views.MessageViewSet.as_view(
			{'delete': 'destroy'}
		)

		response = delete_view(request, slug=self.test_message.slug)

		self.assertEqual(response.status_code, 401)
