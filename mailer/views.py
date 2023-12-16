from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView

from mailer.forms import SendOptionsForm, ClientForm
from mailer.models import SendOptions, Client


class BaseTemplateView(TemplateView):
    template_name = 'mailer/base.html'


class SendOptionsListView(ListView):
    model = SendOptions


class SendOptionsCreateView(CreateView):
    model = SendOptions
    form_class = SendOptionsForm
    success_url = reverse_lazy('mailer:mailers_list')

    def form_valid(self, form):
        return super().form_valid(form)


class SendOptionsUpdateView(UpdateView):
    model = SendOptions
    form_class = SendOptionsForm
    success_url = reverse_lazy('mailer:mailers_list')


class SendOptionsDeleteView(DeleteView):
    model = SendOptions
    success_url = reverse_lazy('mailer:mailers_list')


class ClientListView(ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailer:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailer:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailer:client_list')
