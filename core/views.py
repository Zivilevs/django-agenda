from django.shortcuts import redirect, render, HttpResponse
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
from django.contrib.auth.models import User
# Create your views here.

# another way of redirect
#def index(request):
 #   return redirect('/agenda/')  

def login_user(request):
     return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuario ou senha invalidos")
    return redirect('/')

def Local_evento(request, titulo_evento):
    entry_evento = Evento.objects.get(titulo = titulo_evento)
    local_evento = entry_evento.local
    return HttpResponse('<h1>{} acontece nesse local: {}.</h1>'.format(titulo_evento,local_evento))

@login_required(login_url='/login/')  # se nao autenticado, vai nesse url
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario,
                                    data_evento__gt=data_atual)  # __gt is greater than!
    if evento:
        dados = {'eventos': evento}
        return render(request, 'agenda.html', dados)
    else:
        return render(request, 'agenda.html')

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        local = request.POST.get('local')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()
            #Evento.objects.filter(id=id_evento).update(titulo=titulo, data_evento=data_evento, descricao=descricao)
        else:
            Evento.objects.create(titulo=titulo,data_evento=data_evento, descricao=descricao,local=local,usuario=usuario)
    return redirect('/') 


@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()  # Not Found
    if usuario == evento.usuario:  # para nao deletar o que nao e do usuario(seguranca)
        evento.delete()
    else:
        raise Http404()
    return redirect('/')

# @login_required(login_url='/login/')  esse nao e necessario se for para api
def jason_lista_evento(request, id_usuario):
    try:
        usuario = User.objects.get(id=id_usuario)
    except Exception:
        raise Http404()
    #usuario = request.user quando nao api
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo', 'local')
    return JsonResponse(list(evento), safe=False)

@login_required(login_url='/login/')
def eventos_passados(request):
    usuario = request.user
    actual_date = datetime.now()
    eventa = Evento.objects.filter(usuario=usuario, data_evento__lt=actual_date)
    dados = {'eventos': eventa}
    print("PRINTAS",dados)
    return render(request, 'historico.html', dados)