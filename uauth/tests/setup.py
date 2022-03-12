from django.urls import reverse
from rest_framework.test import APITestCase

class Setup(APITestCase):
    registerURL = reverse('register')
    loginURL = reverse('login')
    updateURL = reverse('update')
    generateNewVerificationTokenURL = reverse('generate-verification-token',
                                              kwargs={'verifyToken': None})
    verifyAccountURL = reverse('verify-account')
    forgotPasswordURL = reverse('forgot-password', kwargs={'email': None})
    resetPassURL = reverse('reset-password')

