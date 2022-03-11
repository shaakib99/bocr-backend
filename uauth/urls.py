from django.urls import path
from .views import register, login, update, generateNewVerificationToken, generateNewPasswordResetToken, resetPassword, verifyAccount

urlpatterns = [
    path('register', view=register, name='registration'),
    path('login', view=login, name='login'),
    path('update', view=update, name='update'),
    path('generate-verification-token/<str:verifyToken>',
         view=generateNewVerificationToken,
         name='generate-verification-token'),
    path('verify-account/', view=verifyAccount, name='verify-account'),
    path('forgot-password/<str:email>',
         view=generateNewPasswordResetToken,
         name='forgot-password'),
    path('reset-password/', view=resetPassword, name='reset-password')
]