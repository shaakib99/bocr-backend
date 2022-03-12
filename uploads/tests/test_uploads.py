import json
from .setup import Setup
from helper.util import randomStringGenerator


class TestUploads(Setup):

    def login(self):
        data = {
            'name': 'Wahid Sakib',
            'email': f'{randomStringGenerator(length=15)}@gmail.com',
            'password': 'Hello12345#'
        }
        register = self.client.post(self.registerURL, data=data, format='json')
        self.assertEqual(register.status_code, 201)

        del data['name']

        login = self.client.post(self.loginURL, data=data, format='json')
        self.assertEqual(login.status_code, 200)

        return json.loads(login.content)

    def test_upload(self):
        login = self.login()

        response = self.client.get(self.url, HTTP_Authorization=login['token'])
        self.assertEqual(response.status_code, 200)
