from django.db import models

class sqlserverconn(models.Model):
    Nombre = models.CharField(max_length=200)
    Telefono = models.CharField(max_length=200)
    DNI = models.CharField(max_length=20)
    Direccion = models.CharField(max_length=2000)
    id = models.BigIntegerField(primary_key=True)


class UsuarioAdd(models.Model):
    id = models.BigIntegerField(primary_key=True)
    Userid = models.CharField(max_length=100)
    Nombre = models.CharField(max_length=100)
    Apellido = models.CharField(max_length=100)
    Correo = models.CharField(max_length=100)
    Estado = models.CharField(max_length=10)
    RolId = models.BigIntegerField()
    Clave = models.CharField(max_length=100)
    Huellabimoetrica = models.CharField(max_length=100)
    PreguntaRecuperacion = models.CharField(max_length=100)
    RespuestaRecuperacion = models.CharField(max_length=100)
    fechaCreacion = models.DateField()