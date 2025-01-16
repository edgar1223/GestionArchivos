from cryptography.fernet import Fernet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from MyGestionArchivo.models import Usuario
from dotenv import load_dotenv
import os
import requests
import io
from django.http import HttpResponse
from mimetypes import guess_type

class Descargar(APIView):
    def post(self, request, user_id):
        # Obtener los datos necesarios
        ruta = request.data.get('ruta')
        file_name = request.data.get('file_name')

        if not ruta or not file_name:
            return Response({'error': "Los parámetros 'ruta' y 'file_name' son obligatorios"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el usuario existe
        usuario = Usuario.objects.filter(id=user_id).first()
        if not usuario:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la URL de la API para descargar el archivo
        load_dotenv()
        API_URL = os.getenv('API_URL')
        if not API_URL:
            return Response({'error': 'No se encontró la configuración de API_URL en el archivo .env'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Preparar datos para la API Flask
        new_data = {
            "ruta": ruta,
            "file_name": file_name
        }

        try:
            # Hacer la solicitud a la API de Flask
            post_response = requests.post(f"{API_URL}descarga", json=new_data)
            post_response.raise_for_status()
        except requests.RequestException as e:
            return Response({'error': f'Error al conectar con la API: {str(e)}'}, status=status.HTTP_502_BAD_GATEWAY)

        # Obtener el archivo descargado desde Flask
        encrypted_file_content = io.BytesIO(post_response.content)

        # Desencriptar el archivo
        encryption_key = usuario.encryption_key
        fernet = Fernet(encryption_key)
        decrypted_file = self.decrypt_file(encrypted_file_content, fernet)

        # Determinar el tipo MIME del archivo a partir de su nombre
        mime_type, _ = guess_type(file_name)
        content_type = mime_type if mime_type else 'application/octet-stream'

        # Preparar el archivo desencriptado para enviarlo como respuesta
        response = HttpResponse(decrypted_file, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response

    def decrypt_file(self, encrypted_file, fernet):
        """
        Desencripta el contenido del archivo utilizando la clave Fernet proporcionada.
        """
        decrypted_file = io.BytesIO()
        encrypted_file.seek(0)  # Asegurarse de estar al principio del archivo

        # Leer el archivo en bloques y desencriptar
        for chunk in encrypted_file:
            decrypted_chunk = fernet.decrypt(chunk)
            decrypted_file.write(decrypted_chunk)

        # Volver al principio del archivo desencriptado
        decrypted_file.seek(0)
        return decrypted_file
