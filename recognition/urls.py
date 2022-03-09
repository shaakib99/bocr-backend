from django.urls import path
from .views import recognition

urlpatterns = [path('recognition', view=recognition, name='image-recognition')]
