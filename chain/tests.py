from datetime import datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from chain.models import ElementChain, Contacts, Product
from users.models import User


class ChainTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test_user@test.com', is_active=True)
        self.element_chain = ElementChain.objects.create(
            name='Тестовая компания',
            supplier=None,
            # products=None,
            debt=0.00,
            created_at=datetime.now,
            name_element_chain='factory',
            hierarchy_level=0
        )
        self.contact = Contacts.objects.create(
            element_chain=self.element_chain,
            email="test@test.com",
            country='RU',
            city='Тестовый город',
            street='Тестовая улица',
            house_number='123'
        )
        self.product = Product.objects.create(
            name='Тестовый продукт',
            model='Тестовая модель',
            product_launch_date="2024-12-03"
        )
        self.element_chain.products.add(self.product)
        self.client.force_authenticate(user=self.user)

    def test_element_chain_list(self):
        url = reverse("chain:elementchain-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            ElementChain.objects.all().count(),
            1
        )

    def test_element_chain_create(self):
        url = reverse("chain:elementchain-list")
        data = {
            'contacts': [
                {
                    'email': "test@test.com",
                    'country': 'RU',
                    "city": 'Тестовый город',
                    "street": 'Тестовая улица',
                    "house_number": '123',
                },
            ],
            'name': 'Тестовая компания',
            'debt': 0.00,
            'name_element_chain': 'розничная сеть',
            'hierarchy_level': 0
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ElementChain.objects.all().count(), 2)

    def test_element_chain_retrieve(self):
        url = reverse("chain:elementchain-detail", args=(self.element_chain.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'),
            self.element_chain.name
        )

    def test_element_chain_update(self):
        url = reverse("chain:elementchain-detail", args=(self.element_chain.pk,))
        data = {
            'name': 'Тестовая компания 2',
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'),
            'Тестовая компания 2'
        )

    def test_element_chain_update_contacts(self):
        url = reverse("chain:elementchain-detail", args=(self.element_chain.pk,))
        data = {
            'contacts':
                [
                    {
                        'id': self.contact.id,
                        'city': 'Новый тестовый город'
                    }
                ]
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Contacts.objects.get(id=self.contact.id).city, 'Новый тестовый город')

    def test_element_chain_delete(self):
        url = reverse("chain:elementchain-detail", args=(self.element_chain.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(ElementChain.objects.all().count(), 0)

    def test_contact_delete(self):
        url = reverse("chain:contact-delete", args=(self.element_chain.pk, self.contact.pk))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Contacts.objects.all().count(),
            0
        )

    def test_element_chain_product_list(self):
        url = reverse('chain:products-list')
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                'pk': self.element_chain.pk,
                'products': [
                    {
                        'id': self.product.pk,
                        'name': self.product.name,
                        'model': self.product.model,
                        'product_launch_date': self.product.product_launch_date
                    }
                ]
            }
        ]
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data,
            result
        )

    def test_element_chain_product_create(self):
        url = reverse("chain:products-create")
        data = {
            "pk": self.element_chain.pk,
            "products": [
                {
                    "name": "test product",
                    "model": "test model",
                    "product_launch_date": "2024-12-03"
                }
            ]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.all().count(), 2)
