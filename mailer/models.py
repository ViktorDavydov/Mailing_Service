from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}
send_period_CHOICES = (
    ('Ежедневно', 'Ежедневно'),
    ('Еженедельно', 'Еженедельно'),
    ('Ежемесячно', 'Ежемесячно')
)

send_status_CHOICES = (
    ('Создана', 'Создана'),
    ('Запущена', 'Запущена'),
    ('Завершена', 'Завершена')
)


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='тема письма', unique=True)
    text = models.TextField(verbose_name='текст письма')
    message_owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь',
                                      on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class SendOptions(models.Model):
    send_name = models.CharField(max_length=200, verbose_name='наименование рассылки',
                                 default=None)
    send_start = models.DateTimeField(verbose_name='время начала рассылки', default=None)
    send_finish = models.DateTimeField(verbose_name='время окончания рассылки', default=None)
    next_try = models.DateTimeField(verbose_name='следующая попытка', **NULLABLE)
    send_period = models.CharField(max_length=20, verbose_name='периодичность',
                                   choices=send_period_CHOICES, default='')
    mail_title = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='тема рассылки',
                                   default=None)
    send_status = models.CharField(max_length=20, verbose_name='статус рассылки',
                                   choices=send_status_CHOICES, default='Создана')
    client_email = models.ManyToManyField('Client', verbose_name="контактный email")

    options_owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь',
                                      on_delete=models.SET_NULL, **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='активность')

    def __str__(self):
        return f"{self.send_name}"

    class Meta:
        verbose_name = 'настройка'
        verbose_name_plural = 'настройки'
        ordering = ('send_start',)


class Client(models.Model):
    client_email = models.CharField(max_length=150, verbose_name="контактный email", unique=True)
    client_name = models.CharField(max_length=150, verbose_name="ФИО")
    comment = models.TextField(verbose_name="комментарий", **NULLABLE)
    client_owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь',
                                     on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f"{self.client_email}"

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ('client_name',)


class Logs(models.Model):
    last_try = models.DateTimeField(auto_now=False, auto_now_add=False,
                                    verbose_name='дата и время последней попытки')
    status_try = models.CharField(max_length=20, verbose_name='статус попытки')
    server_answer = models.TextField(verbose_name='ответ сервера', **NULLABLE, default='')
    send_name = models.CharField(max_length=200, verbose_name='наименование рассылки',
                                 default=None)
    logs_owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь',
                                   on_delete=models.SET_NULL, **NULLABLE)
    send_email = models.EmailField(max_length=150, verbose_name='почта отправки', **NULLABLE)

    def __str__(self):
        return f"{self.status_try}: {self.last_try}"

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
        ordering = ('-last_try',)
