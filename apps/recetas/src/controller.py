from django.shortcuts import render, get_object_or_404, redirect
from apps.recetas.models import Receta
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    recetas = Receta.objects.filter(publicada=True)
    
    if 'procurar' in request.GET and request.GET['procurar']:
        recetas = recetas.filter(nome__icontains=request.GET['procurar'])
    
    recetas   = recetas.order_by('-data_criacao')
    paginadas  = Paginator(recetas, 6)
    pagina     = request.GET.get('pag')
    por_pagina = paginadas.get_page(pagina)
    
    return render(request, 'recetas/index.html', {'recetas': por_pagina})

def create(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Inicie sesion para registrar una receta!')
        return redirect('recetas.index')
    
    if request.method == 'POST':
        nombre          = request.POST['nombre']
        ingredientes  = request.POST['ingredientes']
        modo_preparacion  = request.POST['modo_preparacion']
        tiempo_preparacion = request.POST['tiempo_preparacion']
        rendimento    = request.POST['rendimento']
        categoria     = request.POST['categoria']
        foto          = request.FILES['foto']
        # user          = request.user # porque nao assim?
        user          = get_object_or_404(User, pk=request.user.id)
        
        receta = Receta.objects.create(
            persona=user,
            nombre=nombre,
            ingredientes=ingredientes,
            modo_preparacion=modo_preparacion,
            tiempo_preparacion=tiempo_preparacion,
            rendimento=rendimento,
            categoria=categoria,
            foto=foto
        )
        receta.save()
        messages.success(request, 'Receta registrada con exito!')
        
        return redirect('usuarios.dashboard')
    
    return render(request, 'recetas/create.html')

def show(request, receta_id):
    return render(request, 'recetas/show.html', {'receta': get_object_or_404(Receta, pk=receta_id)})

def edit(request, receta_id):
    if request.method == 'POST':
        receta = Receta.objects.get(pk=receta_id)
        receta.nombre          = request.POST['nombre']
        receta.ingredientes  = request.POST['ingredientes']
        receta.modo_preparacion  = request.POST['modo_preparacion']
        receta.tiempo_preparacion = request.POST['tiempo_preparacion']
        receta.rendimento    = request.POST['rendimento']
        receta.categoria     = request.POST['categoria']
        receta.foto          = request.FILES['foto'] if 'foto' in request.FILES else receta.foto
        receta.save()
        
        return redirect('usuarios.dashboard') # redirecionar para show
    
    return render(request, 'recetas/edit.html', {'receta': get_object_or_404(Receta, pk=receta_id)})

def destroy(request, receta_id):
    # abstrair isso para um metodo que da um retorno mais adequado no caso de nao existir
    # ou usar algo que de pra verificar se nao existe
    receta = get_object_or_404(Receta, pk=receta_id)
    receta.delete()
    
    return redirect('usuarios.dashboard')
