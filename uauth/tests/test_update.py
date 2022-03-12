import json
from .setup import Setup
from helper.util import randomStringGenerator
from .cases import NAME, PASS, EMAIL


class TestUpdate(Setup):

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

    def test_update_name(self):
        login = self.login()
        for P in NAME['pass']:
            response = self.client.patch(self.updateURL,
                                         data={'name': P},
                                         HTTP_Authorization=login['token'],
                                         format='json')
            self.assertEqual(response.status_code, 200)

            content = json.loads(response.content)

            self.assertTrue(content['name'] == P)

            self.assertTrue('id' in content, msg='id is not in response')
            self.assertTrue('name' in content, msg='name is not in response')
            self.assertTrue('email' in content, msg='email is not in response')
            self.assertTrue('isActive' in content,
                            msg='email is not in response')
        for P in NAME['fail']:
            response = self.client.patch(self.updateURL,
                                         data={'name': P},
                                         HTTP_Authorization=login['token'],
                                         format='json')
            self.assertNotEqual(response.status_code, 200)

    def test_update_password(self):
        login = self.login()
        for P in PASS['pass']:
            response = self.client.patch(self.updateURL,
                                         data={'password': P},
                                         HTTP_Authorization=login['token'],
                                         format='json')
            self.assertEqual(response.status_code, 200)

            content = json.loads(response.content)

            self.assertTrue('id' in content, msg='id is not in response')
            self.assertTrue('name' in content, msg='name is not in response')
            self.assertTrue('email' in content, msg='email is not in response')
            self.assertTrue('isActive' in content,
                            msg='email is not in response')
        for P in PASS['fail']:
            response = self.client.patch(self.updateURL,
                                         data={'password': P},
                                         HTTP_Authorization=login['token'],
                                         format='json')
            self.assertNotEqual(response.status_code, 200)

    def test_update_email(self):
        login = self.login()
        for P in EMAIL['pass']:
            response = self.client.patch(self.updateURL,
                                         data={'email': P},
                                         HTTP_Authorization=login['token'],
                                         format='json')
            self.assertEqual(response.status_code, 200)

            content = json.loads(response.content)

            self.assertTrue('id' in content, msg='id is not in response')
            self.assertTrue('name' in content, msg='name is not in response')
            self.assertTrue('email' in content, msg='email is not in response')
            self.assertTrue('isActive' in content,
                            msg='email is not in response')
        for P in EMAIL['fail']:
            response = self.client.patch(self.updateURL,
                                         data={'email': P},
                                         HTTP_Authorization=login['token'],
                                         format='json')
            self.assertNotEqual(response.status_code, 200)

    def test_update_active(self):
        login = self.login()

        response = self.client.patch(self.updateURL,
                                     data={'isActive': True},
                                     HTTP_Authorization=login['token'],
                                     format='json')
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)

        self.assertTrue(content['isActive'] == True)

        response = self.client.patch(self.updateURL,
                                     data={'isActive': False},
                                     HTTP_Authorization=login['token'],
                                     format='json')
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)

        self.assertTrue(content['isActive'] == False)
