import uuid

from django.db import models
from decimal import Decimal


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def increase_debt(self, value, observation=""):
        self.debt += Decimal(value)
        self.save()
        Historical.objects.create(client=self, value=value, observation=observation)

    def reduce_debt(self, value, observation=""):
        self.debt -= Decimal(value)
        self.save()
        Historical.objects.create(client=self, value=-value, observation=observation)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Historical(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='historicos')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    observation = models.TextField(max_length=255, blank=True, null=True)
