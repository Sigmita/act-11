from django.contrib import admin
from .models import Usuario, Suscripcion

# Registra tus modelos para que aparezcan en el panel de administración de Django
admin.site.register(Usuario)
admin.site.register(Suscripcion)