from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from mailer.forms import SendOptionsForm, ClientForm, MessageForm
from mailer.models import SendOptions, Client, Message
from mailer.scheduler import job
from datetime import datetime, timedelta


class BaseTemplateView(TemplateView):
    template_name = 'mailer/base.html'


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

        mail_text = Message.objects.get(title=send_params.mail_title).text

        def job_sender():
            send_mail(
                subject=send_params.mail_title,
                message=mail_text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[send_params.client_email]
            )

        now = datetime.now()
        now = timezone.make_aware(now, timezone.get_current_timezone())
        scheduler = BackgroundScheduler()
        if send_params.send_start > now:
            send_params.send_next_try = send_params.send_start
            if send_params.send_period == 'Ежедневно':
                scheduler.add_job(job_sender, 'interval', minutes=1,
                                  start_date=send_params.send_next_try)
                scheduler.start()
            if send_params.send_period == 'Еженедельно':
                scheduler.add_job(job_sender, 'interval', days=7,
                                  start_date=send_params.send_next_try)
                scheduler.start()
            if send_params.send_period == 'Ежемесячно':
                scheduler.add_job(job_sender, 'interval', days=30,
                                  start_date=send_params.send_next_try)
                scheduler.start()

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
