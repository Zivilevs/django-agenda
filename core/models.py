from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
# Create your models here.

class Evento(models.Model):  # nome da tabela vai ser core_evento, core e nome do app.
    titulo = models.CharField(max_length=100)  
    descricao = models.TextField(blank=True, null=True) #  pode ser nullo e blank
    data_evento = models.DateTimeField(verbose_name='Data do evento')  # obrigatorio
    data_criacao = models.DateTimeField(auto_now=True)  # criado automaticamente o timestamp
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    local = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = 'evento'  # quando vc quer forcar o nome da tabela ser so 'evento'. 

    def __str__(self):
        return self.titulo  #  para pushar titulo do evento

    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y %H:%M Hrs')

    def get_data_input_evento(self):
        return self.data_evento.strftime(':%Y-%m-%d %H:%M')  # NAO FUNCIONA

    def get_evento_atrasado(self):
        if self.data_evento < datetime.now():
            return True
        else:
            return False

    def get_evento_proximo(self):
        if self.data_evento < datetime.now() +  timedelta(hours=1):
            return True
        else:
            return False

   
