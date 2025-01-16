from rest_framework import serializers
from .models import *
import re
from django.utils import timezone
from django.contrib.auth.models import User , Group


class CustomUserSerializers (serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class FileSerializers (serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class FolderSerializers (serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'

