from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    client_email = models.CharField(max_length=30, verbose_name="контактный email")
    client_name = models.CharField(max_length=50, verbose_name="ФИО")
    comment = models.TextField(verbose_name="комментарий", **NULLABLE)

    def __str__(self):
        return f"{self.client_name} ({self.client_email})"

    class META:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ('client_name',)

