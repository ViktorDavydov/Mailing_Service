from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView

from mailer.models import SendOptions


class BaseTemplateView(TemplateView):
    template_name = 'mailer/base.html'


class SendOptionsListView(ListView):
    model = SendOptions


class SendOptionsCreateView(CreateView):
    model = SendOptions
    fields = (
        'send_name',
        'send_time',
        'send_period',
        'send_status',
    )
    success_url = reverse_lazy('mailer:mailers_list')

    def form_valid(self, form):
        
        return super().form_valid(form)


class SendOptionsUpdateView(UpdateView):
    model = SendOptions
    fields = (
        'send_name',
        'send_time',
        'send_period',
        'send_status',
    )
    success_url = reverse_lazy('mailer:mailers_list')


class SendOptionsDeleteView(DeleteView):
    model = SendOptions
    success_url = reverse_lazy('mailer:mailers_list')
