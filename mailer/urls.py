from django.urls import path

from mailer.apps import MailerConfig
from mailer.views import SendOptionsListView, SendOptionsCreateView, \
    SendOptionsUpdateView, SendOptionsDeleteView, ClientListView, ClientCreateView, \
    ClientUpdateView, ClientDeleteView, MessageCreateView, LogsListView, MessageListView, \
    MessageUpdateView, MessageDeleteView, BaseTemplateView, UsersListView, UsersUpdateView

app_name = MailerConfig.name

urlpatterns = [
    path('', BaseTemplateView.as_view(), name='home'),
    path('mailers_list/', SendOptionsListView.as_view(), name='mailers_list'),
    path('create_mailer/', SendOptionsCreateView.as_view(), name='create_mailer'),
    path('edit_mailer/<int:pk>', SendOptionsUpdateView.as_view(), name='edit_mailer'),
    path('delete_mailer/<int:pk>', SendOptionsDeleteView.as_view(), name='delete_mailer'),

    path('logs/', LogsListView.as_view(), name='logs'),
    path('users_table/', UsersListView.as_view(), name='users_table'),
    path('edit_user/<int:pk>', UsersUpdateView.as_view(), name='edit_user'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('update_message/<int:pk>', MessageUpdateView.as_view(), name='edit_message'),
    path('delete_message/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),

    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('edit_client/<int:pk>', ClientUpdateView.as_view(), name='edit_client'),
    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
]
