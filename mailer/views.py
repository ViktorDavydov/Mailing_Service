from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from mailer.forms import SendOptionsForm, ClientForm
from mailer.models import SendOptions, Client
from mailer.scheduler import job


class BaseTemplateView(TemplateView):
    template_name = 'mailer/base.html'


class SendOptionsListView(ListView):
    model = SendOptions


class SendOptionsCreateView(CreateView):
    model = SendOptions
    form_class = SendOptionsForm
    success_url = reverse_lazy('mailer:mailers_list')

    def form_valid(self, form):
        send_params = form.save()

        def job_sender():
            send_mail(
                subject=send_params.mail_title,
                message=send_params.mail_text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[send_params.client_email]
            )

        scheduler = BackgroundScheduler()
        scheduler.add_job(job_sender, 'interval', seconds=60)
        scheduler.start()
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
