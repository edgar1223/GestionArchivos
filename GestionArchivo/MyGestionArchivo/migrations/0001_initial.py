# Generated by Django 5.1.4 on 2025-01-15 06:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('password', models.CharField(max_length=128)),
                ('encryption_key', models.CharField(editable=False, help_text='Clave única para encriptar archivos del usuario', max_length=64)),
                ('name_folder', models.CharField(editable=False, help_text='Nombre de la carpeta designa para el usuario', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('ruta', models.TextField(editable=False, help_text='Ruta completa en el servicio Flask')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folders', to='MyGestionArchivo.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('ruta_flask', models.TextField(editable=False, help_text='Ruta completa del archivo en Flask')),
                ('subido_el', models.DateTimeField(auto_now_add=True)),
                ('carpeta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='MyGestionArchivo.folder')),
                ('compartido_con', models.ManyToManyField(blank=True, related_name='shared_files', to='MyGestionArchivo.usuario')),
            ],
        ),
    ]
