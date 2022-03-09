from django.urls import path
from .views import register, login, update, generateNewVerificationToken, generateNewPasswordResetToken, resetPassword, verifyAccount

urlpatterns = [
    path('register', view=register, name='registration'),
    path('login', view=login, name='login'),
    path('update', view=update, name='update'),
    path('generate-verification-token',
         view=generateNewVerificationToken,
         name='generate-verification-token'),
    path('verify-account/<str:token>',
         view=verifyAccount,
         name='verify-account'),
    path('reset-password/<str:email>',
         view=resetPassword,
         name='forgot-password')
]