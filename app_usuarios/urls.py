from django.urls import path
from . import views

app_name = 'app_usuarios' # Define el namespace de la aplicación

urlpatterns = [
    path('', views.listar_usuarios, name='listar_usuarios'),
    path('usuario/<int:usuario_id>/', views.detalle_usuario, name='detalle_usuario'),
    path('usuario/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuario/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuario/borrar/<int:usuario_id>/', views.borrar_usuario, name='borrar_usuario'),

    path('usuario/<int:usuario_id>/suscripcion/crear/', views.crear_suscripcion, name='crear_suscripcion'),
    path('suscripcion/editar/<int:suscripcion_id>/', views.editar_suscripcion, name='editar_suscripcion'),
    path('suscripcion/borrar/<int:suscripcion_id>/', views.borrar_suscripcion, name='borrar_suscripcion'),

    # URLs de autenticación
    path('login/', views.inicio_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
]