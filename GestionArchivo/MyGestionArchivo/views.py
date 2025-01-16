from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomUserViewSet(viewsets.ModelViewSet): 
        permission_classes = [IsAuthenticated]
        queryset = Usuario.objects.all()
        serializer_class = CustomUserSerializers

class  FileViewSet(viewsets.ModelViewSet): 
        permission_classes = [IsAuthenticated]
        queryset =  File.objects.all()
        serializer_class = FileSerializers

class FolderViewSet(viewsets.ModelViewSet): 
        permission_classes = [IsAuthenticated]
        queryset = Folder.objects.all()
        serializer_class = FolderSerializers
