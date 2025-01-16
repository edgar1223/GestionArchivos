from django.contrib.auth.models import AbstractUser
from django.db import models
from cryptography.fernet import Fernet

from django.db import models
from cryptography.fernet import Fernet
from django.contrib.auth.hashers import make_password
from dotenv import load_dotenv
import os  # Importar os para manejar variables de entorno
import requests
from rest_framework_simplejwt.tokens import RefreshToken

class Usuario(models.Model):
    """
    Modelo de usuario completamente personalizado sin los campos de grupos ni permisos.
    """

    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True,unique=True)
    password = models.CharField(max_length=128)  # Para almacenar la contraseña de forma segura
    is_active = models.BooleanField(default=True)
    encryption_key = models.CharField(
        max_length=64,
        editable=False,
        help_text="Clave única para encriptar archivos del usuario"
    )
    name_folder =models.CharField(
        max_length=64,
        editable=False,
        help_text="Nombre de la carpeta designa para el usuario")
    def save(self, *args, **kwargs):
        # Generar clave única al crear un usuario
        if not self.encryption_key:
            self.encryption_key = self.generate_encryption_key()
        
        # Si no se ha establecido una contraseña, usar una contraseña por defecto o cifrada
        if self.password:
            self.password = make_password(self.password)  # Cifra la contraseña de manera segura

        if not self.name_folder:
            load_dotenv()
            API_URL = os.getenv('API_URL')
            new_data  = {
                "folder_path": self.username+"_"+self.first_name+"_"+self.email
            }
            post_response = requests.post(API_URL+"folders", json=new_data)

            # Print the response
            post_response_json = post_response.json()
            
            if post_response_json:
                print(post_response_json)
                # Si tiene contenido, realizar alguna acción
                self.name_folder = self.username + "_" + self.first_name + "_" + self.email
        super().save(*args, **kwargs)
    @property
    def is_authenticated(self):
        return True
    
    @staticmethod
    def generate_encryption_key():
        """Genera una clave aleatoria para encriptar archivos."""
        return Fernet.generate_key().decode()

    # Personalizar el payload del token
    def get_token(self):
        token = RefreshToken.for_user(self)
        # Agregar datos personalizados al token
        token['username'] = self.username
        token['email'] = self.email
        token['first_name'] = self.first_name
        token['last_name'] = self.last_name
        token['id']=self.id
        return token
    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

class Folder(models.Model):
    """
    Modelo para gestionar carpetas de usuario.
    """
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="folders")
    nombre  = models.CharField(max_length=255)
    ruta  = models.TextField(editable=False, help_text="Ruta completa en el servicio Flask")

    def save(self, *args, **kwargs):
        # Generar ruta lógica al guardar
        if not self.ruta:
            load_dotenv()
            API_URL = os.getenv('API_URL')
            new_data  = {
                "folder_path":self.user.name_folder+"/"+self.nombre
            }
            post_response = requests.post(API_URL+"folders", json=new_data)

            # Print the response
            post_response_json = post_response.json()
            
            if post_response_json:
                # Si tiene contenido, realizar alguna acción
                self.ruta = self.user.name_folder+"/"+self.nombre
        
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.ruta

class File(models.Model):
    """
    Modelo para gestionar archivos subidos.
    """
    nombre = models.CharField(max_length=150)
    carpeta  = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="files")
    ruta_flask  = models.TextField(editable=False, help_text="Ruta completa del archivo en Flask")
    compartido_con  = models.ManyToManyField(Usuario, blank=True, related_name="shared_files")
    subido_el = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return self.flask_path
