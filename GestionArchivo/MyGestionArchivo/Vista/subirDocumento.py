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
class subir(APIView):
    def post(self, request, user_id):
        file = request.FILES.get('file')
        carpeta = request.data.get('carpeta')
        
        if not file or not carpeta:
            return Response({'error': 'Se debe proporcionar un archivo o la ruta'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar que el usuario exista
        usuario = Usuario.objects.filter(id=user_id).first()
        if not usuario:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la clave de encriptación del usuario
        encryption_key = usuario.encryption_key
        fernet = Fernet(encryption_key)

        # Encriptar el archivo
        encrypted_file = self.encrypt_file(file, fernet)

        # Obtener la URL de la API
        load_dotenv()
        API_URL = os.getenv('API_URL')
        if not API_URL:
            return Response({'error': 'No se encontró la configuración de API_URL en el archivo .env'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Preparar los datos y el archivo encriptado para la solicitud
        new_data = {
            "path": f"{usuario.name_folder}/{carpeta}"
        }
        files = {
            'file': ( file.name, encrypted_file, 'application/octet-stream')
        }
        
        
        try:
            # Enviar la solicitud a la API externa
            post_response = requests.post(f"{API_URL}files", data=new_data, files=files)

            post_response.raise_for_status()
        except requests.RequestException as e:
            return Response({'error': f'Error al conectar con la API: {str(e)}'}, status=status.HTTP_502_BAD_GATEWAY)
        
        folder=Folder(
            user=usuario,
            nombre=carpeta,
            ruta= f"{usuario.name_folder}/{carpeta}"
        )
        folder.save()
        archivo_existente = File.objects.filter(
            nombre='encrypted_' + file.name,  
            ruta_flask=f"{usuario.name_folder}/{carpeta}"  
        ).exists()
        if archivo_existente:
            return Response({
                "Error":"Archivo duplicado ya hay un arribo von ese nombre en la ruta "+ f"{usuario.name_folder}/{carpeta}" 
            }, status=status.HTTP_502_BAD_GATEWAY)
        else:
            nuevo_archivo = File(
                nombre='encrypted_' + file.name,  
                carpeta=folder,  
                ruta_flask= f"{usuario.name_folder}/{carpeta}", 
                subido_el=timezone.now()  
            )
            nuevo_archivo.save()
        return Response({
            'file': file.name,
            'ruta': f"{usuario.name_folder}/{carpeta}",
            'Usuario': usuario.username,
            'response_from_api': post_response.json()  # Respuesta de Flask
        }, status=status.HTTP_200_OK)

    def encrypt_file(self, file, fernet):
        """
        Encripta el archivo recibido usando la clave Fernet proporcionada.
        """
        # Crear un buffer en memoria para el archivo encriptado
        encrypted_file = io.BytesIO()

        # Leer el archivo en bloques y encriptar
        for chunk in file.chunks():
            encrypted_chunk = fernet.encrypt(chunk)
            encrypted_file.write(encrypted_chunk)

        # Volver al principio del archivo encriptado para que se pueda leer
        encrypted_file.seek(0)
        return encrypted_file
