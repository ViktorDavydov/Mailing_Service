from django.urls import path

from mailer.apps import MailerConfig
from mailer.views import SendOptionsListView, BaseTemplateView, SendOptionsCreateView, \
    SendOptionsUpdateView, SendOptionsDeleteView, ClientListView, ClientCreateView, \
    ClientUpdateView, ClientDeleteView

app_name = MailerConfig.name

urlpatterns = [
    path('', BaseTemplateView.as_view(), name='home'),
    path('mailers_list/', SendOptionsListView.as_view(), name='mailers_list'),
    path('create_mailer/', SendOptionsCreateView.as_view(), name='create_mailer'),
    path('edit_mailer/<int:pk>', SendOptionsUpdateView.as_view(), name='edit_mailer'),
    path('delete_mailer/<int:pk>', SendOptionsDeleteView.as_view(), name='delete_mailer'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('edit_client/<int:pk>', ClientUpdateView.as_view(), name='edit_client'),
    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
]
