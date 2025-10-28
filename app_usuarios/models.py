from django.db import models

class Usuario(models.Model):
    # Campos de tu tabla Usuarios
    nombre = models.CharField(max_length=255, help_text="Nombre del usuario")
    apellido = models.CharField(max_length=255, blank=True, null=True, help_text="Apellido del usuario")
    email = models.EmailField(unique=True, help_text="Dirección de correo electrónico (única)")
    fecha_registro = models.DateField(auto_now_add=True, help_text="Fecha en que el usuario se registró")
    TIPO_MEMBRESIA_CHOICES = [
        ('Basica', 'Básica'),
        ('Estandar', 'Estándar'),
        ('Premium', 'Premium'),
    ]
    tipo_membresia = models.CharField(
        max_length=100,
        choices=TIPO_MEMBRESIA_CHOICES,
        default='Basica',
        help_text="Tipo de membresía del usuario"
    )
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True, help_text="Foto de perfil del usuario") # <-- NUEVO CAMPO

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['fecha_registro', 'apellido', 'nombre']

class Suscripcion(models.Model):
    # ... (sin cambios) ...
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='suscripciones')
    fecha_inicio = models.DateField(help_text="Fecha de inicio de la suscripción")
    fecha_fin = models.DateField(blank=True, null=True, help_text="Fecha de fin de la suscripción (si aplica)")
    METODO_PAGO_CHOICES = [
        ('Tarjeta', 'Tarjeta de Crédito/Débito'),
        ('PayPal', 'PayPal'),
        ('Transferencia', 'Transferencia Bancaria'),
    ]
    metodo_pago = models.CharField(
        max_length=100,
        choices=METODO_PAGO_CHOICES,
        blank=True,
        null=True,
        help_text="Método de pago utilizado"
    )
    costo_mensual = models.DecimalField(max_digits=10, decimal_places=2, help_text="Costo mensual de la suscripción")

    def __str__(self):
        estado = "Activa" if not self.fecha_fin or self.fecha_fin >= models.DateField.today() else "Expirada"
        return f"Suscripción de {self.usuario.nombre} ({self.usuario.email}) - {self.fecha_inicio} a {self.fecha_fin if self.fecha_fin else 'Indefinido'} ({estado})"

    class Meta:
        verbose_name = "Suscripción"
        verbose_name_plural = "Suscripciones"
        ordering = ['-fecha_inicio']