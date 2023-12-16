from django.db import models

NULLABLE = {'null': True, 'blank': True}


class SendOptions(models.Model):
    send_name = models.CharField(max_length=200, verbose_name='наименование рассылки', **NULLABLE)
    send_time = models.TimeField(auto_now=False, auto_now_add=False,
                                 verbose_name='время рассылки')
    send_period = models.CharField(max_length=20, verbose_name='периодичность')
    mail_title = models.CharField(max_length=100, verbose_name='тема',
                                  default='Сообщение от Invest Store!')
    mail_text = models.TextField(verbose_name='сообщение', default='Добрый день!')
    send_status = models.CharField(max_length=20, verbose_name='статус рассылки')
    client_email = models.ForeignKey('Client', on_delete=models.CASCADE,
                                     verbose_name="контактный email", null=True)

    def __str__(self):
        return f"{self.send_name}"

    class Meta:
        verbose_name = 'настройка'
        verbose_name_plural = 'настройки'
        ordering = ('send_time',)


class Client(models.Model):
    client_email = models.CharField(max_length=30, verbose_name="контактный email", unique=True)
    client_name = models.CharField(max_length=50, verbose_name="ФИО")
    comment = models.TextField(verbose_name="комментарий", **NULLABLE)

    def __str__(self):
        return f"{self.client_email}"

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ('client_name',)


class Logs(models.Model):
    last_try = models.DateTimeField(auto_now=False, auto_now_add=False,
                                    verbose_name='дата и время последней попытки')
    status_try = models.BooleanField(verbose_name='статус попытки')
    server_answer = models.TextField(verbose_name='ответ сервера', **NULLABLE)

    def __str__(self):
        return f"{self.status_try}: {self.last_try}"

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
        ordering = ('last_try',)
