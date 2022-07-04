from ast import Not
from django.shortcuts import render,redirect
from .models import Posteos, Comentarios,User,Avatar
from django.core.paginator import Paginator
from django.http import Http404
from .forms import ComentarForm,PostForm,CustomUserCreationForm,UserEditForm,AvatarFormulario
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

def home(request):
        return render(request, 'index.html')
    
def buscar_post(request):
    busqueda=request.GET.get("buscar")
    page=request.GET.get("page",1)
    posteos=""
    print(busqueda)
    if busqueda:
        posteos= Posteos.objects.filter(
            Q(titulo__icontains = busqueda) |
            Q(plataforma__icontains = busqueda)
        ).distinct()
        if not posteos:
            posteos=Posteos.objects.all()
            messages.error(request,"No se encontraron coincidencias")
        try: 
            paginator=Paginator(posteos,5)
            posteos=paginator.page(page)
        except:
            raise Http404           
        dicc={
            "entity" : posteos,
            "paginator" : paginator 
        }

    return render(request, 'blog.html',dicc)

def inicio(request):
    posteos=Posteos.objects.all()
    page=request.GET.get("page",1)

    try: 
        paginator=Paginator(posteos,5)
        posteos=paginator.page(page)
    except:
        raise Http404
    dicc={
        "entity" : posteos,
        "paginator" : paginator 
    }
    return render(request, 'blog.html',dicc)

def ver(request,id):
    post = Posteos.objects.get(id=id)
    comentarios = Comentarios.objects.filter(id_post=post)
    cantidad=comentarios.count()
    form = ComentarForm()
    if request.method == 'POST':
        form = ComentarForm(request.POST)
        if form.is_valid():
            comentario = Comentarios(
                nombre=form.cleaned_data['nombre'],
                email=form.cleaned_data['email'],
                coment=form.cleaned_data['coment'],
                id_post=post
            )
            comentario.save()
            form = ComentarForm()
            cantidad=comentarios.count()
    context = {
        'post': post,
        'comentarios': comentarios,
        'form': form,
        'cantidad':cantidad
    }
    return render(request, 'blog_detalle.html', context)    

@login_required
def tus_post(request,id):
    posteos=Posteos.objects.filter(autor=id)
    page=request.GET.get("page",1)

    try: 
        paginator=Paginator(posteos,3)
        posteos=paginator.page(page)
    except:
        raise Http404
    return render(request,'posts/tus_posts.html',{"entity" : posteos,"paginator" : paginator,"url":buscar_url_avatar(request.user)})

@login_required
def eliminar_post(request,id,autor):
    posteo=Posteos.objects.get(id=id)
    posteo.delete()
    messages.success(request,"El post se elimino correctamente")
    return redirect ("tus_post",autor)

@login_required
def editar_post(request,id,autor):
    posteo=Posteos.objects.get(id=id)
    if request.method == "POST":
        formulario=PostForm(request.POST or None, request.FILES or None)
        if formulario.is_valid():
            info=formulario.cleaned_data
            posteo.titulo=info['titulo']
            posteo.imagen=info['imagen']
            posteo.cuerpo=info['cuerpo']
            posteo.temporadas=info['temporadas']
            posteo.genero=info['genero']
            posteo.plataforma=info['plataforma']
            posteo.enlace=info['enlace']
            posteo.save()
            messages.success(request,"El post se modifico correctamente.")
            return redirect ("tus_post",autor)
    else:
        formulario=PostForm(initial={'titulo': posteo.titulo,'imagen':posteo.imagen,'cuerpo':posteo.cuerpo,'temporadas':posteo.temporadas,'genero':posteo.genero,'plataforma':posteo.plataforma,'enlace':posteo.enlace})
    return render (request, "posts/edit_post.html", {'formulario':formulario, 'id':id,"url":buscar_url_avatar(request.user)}) 

@login_required
def crear_post(request,id):
    usuario=request.user
    if request.method=="POST":
        formulario=PostForm(request.POST or None, request.FILES or None)
        if formulario.is_valid():
            info=formulario.cleaned_data
            post=Posteos(autor=usuario,titulo=info['titulo'],imagen=info['imagen'],cuerpo=info['cuerpo'],temporadas=info['temporadas'],
                         genero=info['genero'],plataforma=info['plataforma'],enlace=info['enlace'])
            post.save()
            messages.success(request,"El post se guardo correctamente.")
            return redirect("tus_post",id)
    else:
        formulario=PostForm()   
    return render (request,"posts/crear_post.html", {'formulario':formulario,"url":buscar_url_avatar(request.user)})

def login_request(request):
    if request.method == "POST":
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario=form.cleaned_data.get("username")
            contra=form.cleaned_data.get("password")
            user=authenticate(username=usuario , password=contra)
            if user is not None:
                login(request,user)
                messages.success(request, f"{usuario}, pudiste logearte con exito")
                return redirect("tus_post",user.id)
            else:
                messages.error(request,"Usuario o contraseña incorrectos")
                return render(request,"user/login.html",{"messages":f"Datos incorrectos"})
        else:
            messages.warning(request,"Usuario o contraseña incorrectos")
    form=AuthenticationForm()
    return render(request,"user/login.html", {'form':form})

@login_required
def logout_user(request):
    logout(request)
    return redirect ('blog')

def register(request):
    if request.method == "POST":
        formulario=CustomUserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            user=authenticate(username=formulario.cleaned_data["username"] , password=formulario.cleaned_data["password1"])
            login(request,user)
            messages.success(request,"Te pudiste registrar con exito")
            return redirect("tus_post",user.id)
        else:
            messages.warning(request,"cuidado")
    return render(request, "user/registro.html")

@login_required
def editarPerfil(request,id):
    usuario=User.objects.get(id=id)
    if request.method == "POST":
        formulario=UserEditForm(request.POST)
        if formulario.is_valid():
            informacion=formulario.cleaned_data
            usuario.email=informacion['email']
            usuario.password1=informacion['password1']
            usuario.last_name=informacion['last_name']
            usuario.first_name=informacion['first_name']
            usuario.password2=informacion['password1']
            usuario.save()
            messages.success(request,"Modificaste tu perfil con exito")
            return render(request,"user/panel.html")
    else:
        formulario=UserEditForm(initial={'email':usuario.email,'first_name':usuario.first_name,'last_name':usuario.last_name})
    return render(request,"user/editar_perfil.html",{'formulario':formulario,'usuario':usuario,"url":buscar_url_avatar(request.user)})


def buscar_url_avatar(user):
    avatares=Avatar.objects.filter(user=user)
    if avatares.exists():
        # Se usa first() para obtener el primer objeto
        if avatares.first().imagen:
            return avatares.first().imagen.url
        else:
            # Existe el avatar pero no tiene imagen
            return None
    # Si no existe el avatar regresar un None
    return None

@login_required
def agregarAvatar(request,id):
    usuario=request.user
    if request.method=="POST":
        form=AvatarFormulario(request.POST or None, request.FILES or None)
        if form.is_valid():
            info=form.cleaned_data
            avatar=Avatar(user=usuario,imagen=info['imagen'])
            avatar.save()
            messages.success(request,"La imagen se guardo correctamente.")
            return redirect("tus_post",id)
    else:
        form=AvatarFormulario()
    return render (request,"user/avatar.html",{"form":form,"url":buscar_url_avatar(request.user)})