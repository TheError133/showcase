from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .models import UserScript
from .processing import db
from .serializers import ScriptDetailSerializer, ScriptListSerializer, ScriptAddSerializer
from .forms import ScriptUserCreationForm


# Портал.
class ScriptDetailView(View):
    """
    Подробная информация по скриптам.
    """
    def get(self, request, *args, **kwargs):
        user_script = get_object_or_404(UserScript, pk=kwargs['pk'])
        headers, results, error = db.get_info(user_script.script)
        context = {
            'user_script': user_script,
            'headers': headers,
            'results': results,
            'error': error
        }

        return render(request, 'scripts/script_detail.html', context)


class DashboardView(View):
    """
    Информация для дашборда пользователя.
    """
    def get(self, request, *args, **kwargs):
        if request.user in User.objects.filter(is_superuser=True):
            scripts = UserScript.objects.all()
            superuser = True
        elif not request.user.is_anonymous:
            scripts = UserScript.objects.filter(author=request.user)
            superuser = False
        else:
            scripts = None
            superuser = False
        context = {
            'scripts': scripts,
            'superuser': superuser
        }

        return render(request, 'scripts/dashboard.html', context)


# Работа с пользователями.
def user_create(request):
    """
    Создание пользователя портала.
    """
    if request.method == 'GET':
        return render(request, 'scripts/user_create.html', {'form': ScriptUserCreationForm})
    if request.method == 'POST':
        form = ScriptUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = ScriptUserCreationForm()

    return render(request, 'scripts/script_list.html', {'form': form})


# API.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def api_script_list(request):
    """
    Предоставление для списка скриптов пользователей.
    """
    if request.method == 'GET':
        if request.user in User.objects.filter(is_superuser=True):
            scripts = UserScript.objects.all()
        else:
            scripts = UserScript.objects.filter(author=request.user)
        serializer = ScriptListSerializer(scripts, many=True, context={'request': request})
        
        if len(scripts) > 0:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def api_script_detail(request, pk):
    """
    Получение информации по конкретному скрипту.
    """
    if request.method == 'GET':
        script = get_object_or_404(UserScript, pk=pk)
        serializer = ScriptDetailSerializer(script)
        
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def api_script_add(request):
    """
    Добавление скрипта в список.
    """
    if request.method == 'POST':
        serializer = ScriptAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
