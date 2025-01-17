from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny  # Para permitir POST sin autenticación
class CustomUserViewSet(viewsets.ModelViewSet): 
        queryset = Usuario.objects.all()
        serializer_class = CustomUserSerializers
        
        def get_permissions(self):
                # Si el método es POST (registro de usuario), permitimos acceso sin autenticación
                if self.action == 'create':
                  return [AllowAny()]  # No requiere autenticación para crear
                # Para las otras acciones (GET, PUT, PATCH, DELETE), se requiere autenticación
                return [IsAuthenticated()]

class  FileViewSet(viewsets.ModelViewSet): 
        permission_classes = [IsAuthenticated]
        queryset =  File.objects.all()
        serializer_class = FileSerializers

class FolderViewSet(viewsets.ModelViewSet): 
        permission_classes = [IsAuthenticated]
        queryset = Folder.objects.all()
        serializer_class = FolderSerializers
