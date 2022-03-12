import json
from .setup import Setup
from helper.util import randomStringGenerator


class TestLogin(Setup):

    def test_login_success(self):
        data = {
            'name': 'Wahid Sakib',
            'email': f'{randomStringGenerator(length=15)}@gmail.com',
            'password': 'Hello12345#'
        }
        register = self.client.post(self.registerURL, data=data, format='json')
        self.assertEqual(register.status_code, 201)

        del data['name']

        response = self.client.post(self.loginURL, data=data, format='json')
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertTrue('token' in content, msg='token is not in response')

        self.assertTrue('id' in content, msg='id is not in response')
        self.assertTrue('name' in content, msg='name is not in response')
        self.assertTrue('email' in content, msg='email is not in response')

    def test_login_fail(self):
        data = {
            'name': 'Wahid Sakib',
            'email': f'{randomStringGenerator(length=15)}@gmail.com',
            'password': 'Hello12345#'
        }

        del data['name']

        response = self.client.post(self.loginURL, data=data, format='json')
        self.assertNotEqual(response.status_code, 200)
