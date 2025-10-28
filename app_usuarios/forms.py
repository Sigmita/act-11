from django import forms
from .models import Usuario, Suscripcion

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'tipo_membresia', 'foto_perfil'] # <-- NUEVO CAMPO
        widgets = {
            'tipo_membresia': forms.Select(choices=Usuario.TIPO_MEMBRESIA_CHOICES),
        }

class SuscripcionForm(forms.ModelForm):
    # ... (sin cambios) ...
    class Meta:
        model = Suscripcion
        fields = ['usuario', 'fecha_inicio', 'fecha_fin', 'metodo_pago', 'costo_mensual']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'metodo_pago': forms.Select(choices=Suscripcion.METODO_PAGO_CHOICES),
        }