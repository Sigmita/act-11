from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Usuario, Suscripcion
from .forms import UsuarioForm, SuscripcionForm
from django.contrib import messages
from django.utils import timezone

def listar_usuarios(request):
    # ... (sin cambios) ...
    usuarios = Usuario.objects.all().order_by('apellido', 'nombre')
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

def detalle_usuario(request, usuario_id):
    # ... (sin cambios) ...
    usuario = get_object_or_404(Usuario, id=usuario_id)
    suscripciones = usuario.suscripciones.all().order_by('-fecha_inicio')
    return render(request, 'detalle_usuario.html', {
        'usuario': usuario,
        'suscripciones': suscripciones,
    })

@login_required
def crear_usuario(request):
    """Permite crear un nuevo usuario."""
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES) # <-- AÑADIR request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado exitosamente.")
            return redirect('app_usuarios:listar_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'formulario_usuario.html', {'form': form, 'titulo': 'Agregar Nuevo Usuario'})
# ... (otras importaciones y vistas) ...

@login_required # Solo usuarios autenticados pueden crear suscripciones
def crear_suscripcion(request, usuario_id): # <-- ASEGÚRATE DE QUE ESTA FUNCIÓN EXISTA
    """Permite crear una nueva suscripción para un usuario."""
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = SuscripcionForm(request.POST)
        if form.is_valid():
            suscripcion = form.save(commit=False)
            suscripcion.usuario = usuario
            suscripcion.save()
            messages.success(request, "Suscripción agregada exitosamente.")
            return redirect('app_usuarios:detalle_usuario', usuario_id=usuario.id)
    else:
        # Pre-llenar el campo de usuario en el formulario
        form = SuscripcionForm(initial={'usuario': usuario})
    return render(request, 'formulario_suscripcion.html', {'form': form, 'usuario': usuario, 'titulo': f'Agregar Suscripción a {usuario.nombre}'})

# ... (el resto de tus vistas) ...S

@login_required
def editar_usuario(request, usuario_id):
    """Permite editar un usuario existente."""
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=usuario) # <-- AÑADIR request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado exitosamente.")
            return redirect('app_usuarios:detalle_usuario', usuario_id=usuario.id)
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'formulario_usuario.html', {'form': form, 'titulo': f'Editar Usuario: {usuario.nombre}'})
# ... (otras importaciones y vistas) ...

@login_required # Solo usuarios autenticados pueden borrar usuarios
def borrar_usuario(request, usuario_id): # <-- ASEGÚRATE DE QUE ESTA FUNCIÓN EXISTA
    """Permite borrar un usuario existente."""
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, "Usuario eliminado exitosamente.")
        return redirect('app_usuarios:listar_usuarios')
    return render(request, 'confirmar_borrar_usuario.html', {'usuario': usuario})
# ... (otras importaciones y vistas, incluyendo las que ya corregiste) ...

@login_required # Solo usuarios autenticados pueden editar suscripciones
def editar_suscripcion(request, suscripcion_id): # <-- ASEGÚRATE DE QUE ESTA FUNCIÓN EXISTA
    """Permite editar una suscripción existente."""
    suscripcion = get_object_or_404(Suscripcion, id=suscripcion_id)
    usuario = suscripcion.usuario # Para redireccionar al detalle del usuario después
    if request.method == 'POST':
        form = SuscripcionForm(request.POST, instance=suscripcion)
        if form.is_valid():
            form.save()
            messages.success(request, "Suscripción actualizada exitosamente.")
            return redirect('app_usuarios:detalle_usuario', usuario_id=usuario.id)
    else:
        form = SuscripcionForm(instance=suscripcion)
    return render(request, 'formulario_suscripcion.html', {'form': form, 'usuario': usuario, 'titulo': f'Editar Suscripción de {usuario.nombre}'})

@login_required # Solo usuarios autenticados pueden borrar suscripciones
def borrar_suscripcion(request, suscripcion_id): # <-- ASEGÚRATE DE QUE ESTA FUNCIÓN EXISTA
    """Permite borrar una suscripción existente."""
    suscripcion = get_object_or_404(Suscripcion, id=suscripcion_id)
    usuario = suscripcion.usuario # Para redireccionar al detalle del usuario después

    if request.method == 'POST':
        suscripcion.delete()
        messages.success(request, "Suscripción eliminada exitosamente.")
        return redirect('app_usuarios:detalle_usuario', usuario_id=usuario.id)

    return render(request, 'confirmar_borrar_suscripcion.html', {'suscripcion': suscripcion, 'usuario': usuario, 'titulo': 'Confirmar Eliminación'})
def inicio_sesion(request): # <-- ASEGÚRATE DE QUE ESTA FUNCIÓN EXISTA
    """Permite a los usuarios iniciar sesión."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"¡Bienvenido, {username}!")
                return redirect('app_usuarios:lista_usuarios') # O a donde quieras redireccionar después del login
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Error en el formulario de inicio de sesión.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'titulo': 'Iniciar Sesión'})


# ... (el resto de tus vistas) ...

# ... (el resto de tus vistas) ...

# ... (el resto de las vistas sin cambios) ...

@login_required
def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('app_usuarios:listar_usuarios')