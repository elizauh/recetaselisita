from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from apps.recetas.models import Receta
from .validacoes import *

def create(request):
    if request.method == 'POST':
        nombre                  = request.POST['nombre']
        email                 = request.POST['email']
        password              = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        
        erros = 0
        if campo_vazio(nombre):
            messages.error(request, 'Campo obligatorio!')
            erros += 1
        if campo_vazio(email):
            messages.error(request, 'Campo obligatorio!')
            erros += 1
        if usuario_cadastrado(nombre, email):
            messages.error(request, 'Usuario ya esta registrado!')
            erros += 1
        if campo_vazio(password):
            messages.error(request, 'Campo obligatorio!')
            erros += 1
        if senhas_diferentes(password, password_confirmation):
            messages.error(request, 'Las claves deben ser iguales!')
            erros += 1
        if erros > 0:
            return redirect('registro')
        
        user = User.objects.create_user(username=nombre, email=email, password=password)
        user.save()
        messages.success(request, f"Usuario {user.username} registrado con exito!")

        return redirect('usuarios.login')
    
    return render(request, 'usuarios/registro.html')

def login(request):
    if request.method == 'POST':
        email    = request.POST['email']
        password = request.POST['password']
        
        if campo_vazio(email) or campo_vazio(password):
            messages.error(request, 'Todos los campos son obligatorios!')
            return redirect('usuarios.login')
    
        if User.objects.filter(email=email).exists():
            nombre = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request=request, username=nombre, password=password)
            
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Inicio de sesion realizado con exito!')
                
                return redirect('usuarios.dashboard')
        
    return render(request, 'usuarios/login.html')

def dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Inicie sesion para acceder a la pagina \'Mis recetas\'!')
        return redirect('login')
    
    recetas = Receta.objects.filter(persona=request.user.id).order_by('data_criacao')
    
    return render(request, 'usuarios/dashboard.html', {'recetas': recetas})

def logout(request):
    auth.logout(request)
    return redirect('recetas.index')
