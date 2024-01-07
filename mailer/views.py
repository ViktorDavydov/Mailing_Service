import random
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.urls import reverse_lazy

from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView

from blog.models import Blog
from mailer.forms import SendOptionsForm, ClientForm, MessageForm, UsersForm, \
    SendOptionsManagerForm
from mailer.models import SendOptions, Client, Message, Logs
from mailer.scheduler.scheduler import set_scheduler
from mailer.services import set_period
from users.models import User


class BaseTemplateView(TemplateView):
    template_name = 'mailer/statistics.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['full_list'] = SendOptions.objects.all().count()
        context_data['active_list'] = SendOptions.objects.filter(is_active=True).count()
        context_data['unique_clients_list'] = Client.objects.all().count()
        articles_count = Blog.objects.all().count()
        if settings.CASH_ENABLE:
            key = f'random_articles'
            article_list = cache.get(key)
            if article_list is None:
                article_list = random.sample(list(Blog.objects.all()), articles_count)
                cache.set(key, article_list)
        else:
            article_list = random.sample(list(Blog.objects.all()), articles_count)

        context_data['random_articles'] = article_list

        return context_data


class SendOptionsListView(LoginRequiredMixin, ListView):
    model = SendOptions

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='manager'):
            queryset = queryset.all()
        else:
            queryset = queryset.filter(options_owner=self.request.user)
        return queryset


class SendOptionsCreateView(LoginRequiredMixin, CreateView):
    model = SendOptions
    form_class = SendOptionsForm
    success_url = reverse_lazy('mailer:mailers_list')

    def form_valid(self, form):
        send_params = form.save()
        send_params.options_owner = self.request.user
        send_params.next_try = set_period()
        send_params.save()

        set_scheduler()

        return super().form_valid(form)


class SendOptionsUpdateView(LoginRequiredMixin, UpdateView):
    model = SendOptions
    form_class = SendOptionsForm
    success_url = reverse_lazy('mailer:mailers_list')

    def form_valid(self, form):
        send_params = form.save()
        self.model.send_status = send_params.send_status
        send_params.next_try = set_period()
        send_params.save()

        set_scheduler()

        return super().form_valid(form)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(id=self.kwargs.get('pk'))
        return queryset

    def get_form_class(self):
        if self.request.user.groups.filter(name='manager'):
            return SendOptionsManagerForm
        return SendOptionsForm


class SendOptionsDeleteView(LoginRequiredMixin, DeleteView):
    model = SendOptions
    success_url = reverse_lazy('mailer:mailers_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(message_owner=self.request.user)
        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailer:message_list')

    def form_valid(self, form):
        message_params = form.save()
        message_params.message_owner = self.request.user
        message_params.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailer:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailer:message_list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(client_owner=self.request.user)
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailer:client_list')

    def form_valid(self, form):
        send_params = form.save()
        send_params.client_owner = self.request.user
        send_params.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailer:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailer:client_list')


class LogsListView(LoginRequiredMixin, ListView):
    model = Logs

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(logs_owner=self.request.user)
        return queryset


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'mailer/users_table.html'


class UsersUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UsersForm
    template_name = 'mailer/user_activity_form.html'
    success_url = reverse_lazy('mailer:users_table')
