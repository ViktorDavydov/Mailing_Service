
from django.urls import reverse_lazy

from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from mailer.forms import SendOptionsForm, ClientForm, MessageForm
from mailer.models import SendOptions, Client, Message
from mailer.services import set_mailer


class BaseTemplateView(TemplateView):
    template_name = 'mailer/statistics.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['full_list'] = SendOptions.objects.all().count()
        context_data['active_list'] = SendOptions.objects.filter(send_status='Запущена').count()
        context_data['unique_clients_list'] = Client.objects.all().count()
        return context_data


class SendOptionsListView(ListView):
    model = SendOptions

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(options_owner=self.request.user)
        return queryset


class SendOptionsCreateView(CreateView):
    model = SendOptions
    form_class = SendOptionsForm
    success_url = reverse_lazy('mailer:mailers_list')

    def form_valid(self, form):
        send_params = form.save()
        send_params.options_owner = self.request.user
        send_params.save()

        set_mailer(send_params)

        return super().form_valid(form)


class SendOptionsUpdateView(UpdateView):
    model = SendOptions
    form_class = SendOptionsForm
    success_url = reverse_lazy('mailer:mailers_list')

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(options_owner=self.request.user)
    #     queryset['client_email'] = queryset.filter(client_email=SendOptions.objects.client_email)
    #     return queryset


class SendOptionsDeleteView(DeleteView):
    model = SendOptions
    success_url = reverse_lazy('mailer:mailers_list')


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailer:mailers_list')


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(client_owner=self.request.user)
        return queryset


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailer:client_list')

    def form_valid(self, form):
        send_params = form.save()
        send_params.client_owner = self.request.user
        send_params.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailer:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailer:client_list')
