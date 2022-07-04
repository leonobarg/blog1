from django import forms
from app_blog.models import Posteos,Avatar
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields=['username','first_name','last_name','email','password1','password2']
        
class UserEditForm(UserCreationForm):
    last_name= forms.CharField(label="Nombre")
    first_name= forms.CharField(label="Apellido")
    email=forms.EmailField(label="Email")
    password1= forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2= forms.CharField(label="Repetir Contraseña", widget=forms.PasswordInput)
    
    class Meta:
        model=User
        fields=['first_name','last_name','email','password1','password2']
        
class ComentarForm(forms.Form):
    nombre = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={
                'class': 'form-floating mb-3',
                'placeholder': 'Tu nombre',
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-floating mb-3',
                'placeholder': 'Tu e-mail',
            }
        )
    )
    coment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-floating mb-3',
                'placeholder': 'Deja tu comentario',
            }
        )
    )
    
class PostForm(forms.Form):
    titulo=forms.CharField(max_length=40)
    imagen=forms.ImageField()
    cuerpo=forms.CharField(widget=forms.Textarea)
    temporadas=forms.CharField(max_length=40)
    genero=forms.CharField(max_length=40)
    plataforma=forms.CharField(max_length=40)
    enlace=forms.CharField(max_length=100)
  
    class Meta:
        model=Posteos
        fields=['autor','titulo','imagen','cuerpo','temporadas','genero','plataforma','enlace']
        
class AvatarFormulario(forms.Form):
    imagen=forms.ImageField()
    
    class Meta:
        model=Avatar
        fields=['user','imagen']