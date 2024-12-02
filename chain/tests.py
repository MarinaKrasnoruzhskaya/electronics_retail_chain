from datetime import datetime

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from chain.models import ElementChain, Contacts
from users.models import User


class ChainTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test_user@test.com', is_active=True)
        # self.element_chain = ElementChain(
        #     name='Тестовая компания',
        #     supplier=None,
        #     products=None,
        #     debt=0.00,
        #     created_at=datetime.now,
        #     name_element_chain='factory',
        #     hierarchy_level=0
        # )
        # print(self.element_chain)
        # print(self.element_chain.id, self.element_chain.name, self.element_chain.name_element_chain)
        # self.contacts = Contacts.objects.create(
        #     element_chain=self.element_chain,
        #     email="test@test.com
        #     country='RU',
        #     city='Тестовый город',
        #     street='Тестовая улица',
        #     house_number='123'
        # )
        self.client.force_authenticate(user=self.user)

    def test_element_chain_list(self):
        url = reverse("chain:elementchain-list")
        print(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_element_chain_create(self):
        url = reverse("chain:elementchain-create")
        data = {
            'name': 'Тестовая компания',
            'supplier': None,
            'products': None,
            'debt': 0.00,
            'created_at': datetime.now,
            'name_element_chain': 'factory',
            'hierarchy_level': 0,
            'contacts': [
                {
                    'email': "test@test.com",
                    'country': 'RU',
                    "city": 'Тестовый город',
                    "street": 'Тестовая улица',
                    "house_number":'123'
                }
            ]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
