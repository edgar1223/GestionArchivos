# GestionArchivos

Este proyecto implementa un sistema de almacenamiento en la nube utilizando Flask para la manipulación de archivos en un servidor Ubuntu y Django para la gestión de usuarios y permisos.

## Instalación y Configuración

### Instalar Nginx

```bash
sudo apt update
sudo apt install nginx
```

### Configuración de Directorios y Nginx

1. Crear directorios necesarios y mover archivos:
```bash
sudo mkdir -p /var/www/cloud-storage/files
sudo mv /var/www/cloud-storage/test.txt /var/www/cloud-storage/files/
ls -l /var/www/cloud-storage/files/
```

2. Crear el archivo de configuración de Nginx:
```bash
sudo nano /etc/nginx/sites-available/cloud-storage
```

3. Contenido del archivo:
```bash
  GNU nano 7.2                                                            /etc/nginx/sites-available/cloud-storage                                                                      
server {
    listen 80;
    server_name 192.168.50.96;

    location /files/ {
        root /var/www/cloud-storage;
        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;
    }
 # Configuración para redirigir al backend
    location /api/ {
        proxy_pass http://127.0.0.1:5000;  # Dirección donde corre tu servicio Django/Flask
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 500M;
    }
}
```

4. Habilitar la configuración de Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/cloud-storage /etc/nginx/sites-enabled/
```

5. Establecer permisos adecuados y recargar Nginx:
```bash
sudo chown -R www-data:www-data /var/www/cloud-storage/files
sudo chmod -R 755 /var/www/cloud-storage/files
sudo systemctl reload nginx
```

## Flask para Manipulación de Archivos

Este proyecto implementa un sistema de almacenamiento en la nube utilizando Flask para la manipulación de archivos en un servidor Ubuntu y Django para la gestión de usuarios y permisos.

1. Instala Flask en tu entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  
pip install flask
```

2. Ejecuta la aplicación Flask:
```bash
python app.py
```

## Django para Gestión de Usuarios y Archivos

Django se encarga de manejar la lógica de negocio y la interacción con los usuarios:

1. Configura un entorno virtual e instala las dependencias
```bash
python3 -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
pip install django djangorestframework cryptography python-dotenv
```

2. Se agregaron migraciones si es que se cambia los modelos
```bash
python manage.py makemigrations
```

3. Aplica las migraciones iniciales:
```bash
python manage.py migrate
```

4. Ejecuta el servidor de desarrollo para probar:
```bash
python manage.py runserver
```
## Diagrama de secuencia de la aplicacion  de giestion de archivo

![diagrama de secuencia](https://github.com/user-attachments/assets/e75f74bd-469e-47c9-b5eb-69028b0316f1)

