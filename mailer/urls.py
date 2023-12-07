from django.urls import path

from mailer.views import index

urlpatterns = [
    path('', index, name='index')
]
