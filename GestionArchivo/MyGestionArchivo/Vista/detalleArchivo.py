from cryptography.fernet import Fernet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from MyGestionArchivo.models import *
from dotenv import load_dotenv
import os
import requests
import io
from django.utils import timezone

class deteallesArchivo(APIView):
    def post(self, request, user_id):
        carpeta = request.data.get('carpeta')
        file_name = request.data.get('file_name')
        usuario = Usuario.objects.filter(id=user_id).first()
        load_dotenv()
        API_URL = os.getenv('API_URL')
        new_data = {
            "ruta": f"{usuario.name_folder}/{carpeta}",
            "file_name": file_name
        }

        # Realizar la petición a la API
        post_response = requests.post(f"{API_URL}detalle/archivo", json=new_data)

        # Obtener los datos JSON de la respuesta
        response_json = post_response.json()

        # Acceder a los valores del JSON
        fecha_creacion = response_json.get("fecha_creacion")
        nombre = response_json.get("nombre")
        peso = response_json.get("peso")
        ruta_completa = response_json.get("ruta_completa")

        # Combinar los archivos y carpetas en un solo diccionario para devolver
        resultado = {
            "fecha_creacion": fecha_creacion,
            "nombre": nombre,
            "peso": peso,
            "ruta_completa": ruta_completa,
            "Propietario": usuario.username
        }

        return Response(resultado, status=status.HTTP_200_OK)
