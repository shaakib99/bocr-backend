from django.urls import reverse
from uauth.tests.setup import Setup


class Setup(Setup):
    url = reverse('user-images')
