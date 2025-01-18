from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from MyGestionArchivo.views import *
from MyGestionArchivo import views
from MyGestionArchivo.Vista.subirDocumento import subir
from MyGestionArchivo.Vista.DescarArchivo import Descargar
from MyGestionArchivo.Vista.ListarArchivos import listarArchivos
from MyGestionArchivo.Vista.login import LoginAPIView ,RefreshTokenAPIView
from MyGestionArchivo.Vista.detalleArchivo import deteallesArchivo

#GroupViewSet deteallesArchivo
router = DefaultRouter()
router.register(r'CustomUser', CustomUserViewSet, basename='usuarios')
router.register(r'File', FileViewSet, basename='archivos')
router.register(r'Folder', FolderViewSet, basename='carpetas')

urlpatterns = [
    path('', include(router.urls)),
   path('subir/file/<int:user_id>/', subir.as_view(), name='subirView'),
   path('descargar/file/<int:user_id>/', Descargar.as_view(), name='descargarView'),
   path('listar/archivos/<int:user_id>/', listarArchivos.as_view(), name='listarArchivosView'),
   path('login/', LoginAPIView.as_view(), name='login'),
   path('token/refresh/', RefreshTokenAPIView.as_view(), name='token_refresh'),
      path('detalle/archivo/<int:user_id>/', deteallesArchivo.as_view(), name='detalle_Archivo'),

]