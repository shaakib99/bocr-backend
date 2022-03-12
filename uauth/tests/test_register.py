from .setup import Setup
from .cases import NAME, EMAIL, PASS
from helper.util import randomStringGenerator


class TestRegistration(Setup):

    def test_name(self):
        for P in NAME['pass']:
            data = {
                'email': f'{randomStringGenerator(length=10)}@gmail.com',
                'password': 'Hello12345#',
                'name': P
            }
            response = self.client.post(self.registerURL,
                                        data=data,
                                        format='json')
            self.assertEqual(response.status_code, 201)

        for P in NAME['fail']:
            data = {
                'email': f'{randomStringGenerator(length=10)}@gmail.com',
                'password': 'Hello12345#',
                'name': P
            }
            response = self.client.post(self.registerURL,
                                        data=data,
                                        format='json')
            self.assertNotEqual(response.status_code, 201)

    def test_email(self):
        for P in EMAIL['pass']:
            data = {
                'email': P,
                'password': 'Hello12345#',
                'name': 'Wahid Sakib'
            }
            response = self.client.post(self.registerURL,
                                        data=data,
                                        format='json')
            self.assertEqual(response.status_code, 201)

        for P in EMAIL['fail']:
            data = {
                'email': P,
                'password': 'Hello12345#',
                'name': 'Wahid Sakib'
            }
            response = self.client.post(self.registerURL,
                                        data=data,
                                        format='json')
            self.assertNotEqual(response.status_code, 201)

    def test_password(self):
        for P in PASS['pass']:
            data = {
                'email': f'{randomStringGenerator(length=10)}@gmail.com',
                'password': P,
                'name': 'Wahid Sakib'
            }
            response = self.client.post(self.registerURL,
                                        data=data,
                                        format='json')
            self.assertEqual(response.status_code, 201)

        for P in PASS['fail']:
            data = {
                'email': f'{randomStringGenerator(length=10)}@gmail.com',
                'password': P,
                'name': 'Wahid Sakib'
            }
            response = self.client.post(self.registerURL,
                                        data=data,
                                        format='json')
            self.assertNotEqual(response.status_code, 201)