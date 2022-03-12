from django.urls import path
from .views import userImages

urlpatterns = [
  path('images/', view=userImages, name='user-images')
]