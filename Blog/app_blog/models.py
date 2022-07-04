from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Posteos(models.Model):
    autor=models.ForeignKey(User, null=True,blank=True, on_delete=models.CASCADE)
    titulo=models.CharField(max_length=40,verbose_name="Titulo")
    fcreacion=models.DateTimeField(auto_now_add=True)
    imagen=models.ImageField(upload_to="media/",verbose_name="Imagen")
    cuerpo=models.TextField(verbose_name="Detalle",null=True)
    temporadas=models.CharField(max_length=40,verbose_name="Temporadas")
    genero=models.CharField(max_length=40,verbose_name="Genero")
    plataforma=models.CharField(max_length=40,verbose_name="Plataforma")
    enlace=models.CharField(max_length=100,verbose_name="Enlace")
    
    def __str__(self):
        fila="Titulo:" + self.titulo + " - " + "Descripcion: " + self.cuerpo
        return fila
    
    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()


class Comentarios(models.Model):
    nombre=models.CharField(max_length=40, verbose_name="Nombre",null=True)
    email=models.EmailField()
    coment=models.TextField(max_length=500)
    fcomentario=models.DateTimeField(auto_now_add=True)
    id_post=models.ForeignKey(Posteos, null=True, blank=True, on_delete=models.CASCADE)

class Plataforma(models.Model):
    nombre=models.CharField(max_length=50,verbose_name="Nombre",null=True)
    enlace=models.URLField()
    
class Avatar(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    imagen=models.ImageField(upload_to='avatares',null=True,blank=True)