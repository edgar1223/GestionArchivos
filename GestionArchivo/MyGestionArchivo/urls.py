from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from MyGestionArchivo.views import *
from MyGestionArchivo import views
from MyGestionArchivo.Vista.subirDocumento import subir
from MyGestionArchivo.Vista.DescarArchivo import Descargar
from MyGestionArchivo.Vista.ListarArchivos import listarArchivos

router = routers.DefaultRouter()
router.register(r'CustomUser', views.CustomUserViewSet)
router.register(r'File', views.FileViewSet)
router.register(r'Folder', views.FolderViewSet)


#GroupViewSet listarArchivos


urlpatterns = [
   path('', include(router.urls)),
   path('subir/file/<int:user_id>/', subir.as_view(), name='subirView'),
   path('descargar/file/<int:user_id>/', Descargar.as_view(), name='descargarView'),
   path('listar/archivos/<int:user_id>/', listarArchivos.as_view(), name='listarArchivosView')

]