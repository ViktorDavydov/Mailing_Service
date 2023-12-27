from datetime import datetime, timedelta

from django import forms
from django.utils import timezone

from mailer.models import SendOptions, Client, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in ['send_period', 'send_status', 'client_email']:
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'


class SendOptionsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = SendOptions
        exclude = ('send_next_try', 'options_owner', 'send_status',)

    def clean_send_start(self):
        cleaned_data = self.cleaned_data.get('send_start', )
        now = datetime.now()
        now = timezone.make_aware(now, timezone.get_current_timezone())
        if cleaned_data < now:
            raise forms.ValidationError('Время начала не может быть меньше текущего')
        return cleaned_data

    def clean_send_finish(self):
        cleaned_data = self.cleaned_data.get('send_finish', )
        now = datetime.now()
        now = timezone.make_aware(now, timezone.get_current_timezone())
        if cleaned_data < now + timedelta(days=1):
            raise forms.ValidationError('Время окончания не может быть меньше текущего + сутки')
        return cleaned_data


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('client_owner',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('message_owner',)
