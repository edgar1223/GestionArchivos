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

class listarArchivos(APIView):
    def post(self, request, user_id):
        try:
            # Obtener carpeta y usuario
            carpeta = request.data.get('carpeta')
            usuario = Usuario.objects.filter(id=user_id).first()
            if not usuario:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            # Cargar variables de entorno
            load_dotenv()
            API_URL = os.getenv('API_URL')
            if not API_URL:
                return Response({"error": "API_URL no está configurado"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Crear los datos para la petición
            new_data = {
                "folder_path": f"{usuario.name_folder}/{carpeta}"
            }

            # Realizar la petición a la API
            post_response = requests.post(f"{API_URL}list/files", json=new_data)
            print(f"{API_URL}list/files")
            print(new_data)
            # Verificar el código de estado de la respuesta
            print(post_response)
            # Intentar obtener la respuesta JSON
            try:
                response_json = post_response.json()
            except requests.exceptions.JSONDecodeError:
                return Response({
                    "error": "La API devolvió una respuesta no válida",
                    "detalle": post_response.text
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Procesar y devolver la lista de archivos
            archivos = response_json.get("files", [])
            return Response({"archivos": archivos}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": "Error inesperado",
                "detalle": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
