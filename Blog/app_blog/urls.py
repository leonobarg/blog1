from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from app_blog.views import home

urlpatterns = [
    path("",home,name="home"),
    path('blog',views.inicio, name='blog'),
    path('ver/<int:id>', views.ver ,name='ver'),
    path('tus_posts/<int:id>', views.tus_post, name='tus_post'),
    path('posts/edit_post/<int:id><int:autor>', views.editar_post, name='editar_post'),
    path('posts/crear_post/<int:id>', views.crear_post, name='crear_post'),
    path('posts/delete_post/<int:id><int:autor>', views.eliminar_post, name='eliminar_post'),    
    path('login',views.login_request, name='login'),
    path('logout', views.logout_user ,name='logout'),
    path('register',views.register, name='register'),
    path('editarperfil/<int:id>',views.editarPerfil, name="editar"),
    path('agregarAvatar/<int:id>',views.agregarAvatar, name="avatar"),
    path("buscar_post", views.buscar_post, name="buscar_post"),
]