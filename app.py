from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Configuración del directorio de almacenamiento
BASE_DIR = "/var/www/cloud-storage/files"

# Asegurarse de que el directorio base existe
os.makedirs(BASE_DIR, exist_ok=True)

# Crear una carpeta
@app.route('/api/folders', methods=['POST'])
def create_folder():
    data = request.json
    folder_path = data.get('folder_path', '').strip('/')  # Ruta proporcionada por el usuario

    if not folder_path:
        return jsonify({"error": "Folder path is required"}), 400

    # Divide la ruta en partes
    sub_paths = folder_path.split('/')
    current_path = BASE_DIR

    try:
        for sub_path in sub_paths:
            # Construye la ruta acumulativa
            current_path = os.path.join(current_path, sub_path)
            # Crea la carpeta si no existe
            if not os.path.exists(current_path):
                os.mkdir(current_path)
        return jsonify({"message": f"Path '{folder_path}' created successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Error creating path: {e}"}), 500

@app.route('/api/files', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    path = request.form.get('path', '').strip('/')

    # Construir el path completo dentro de BASE_DIR
    full_path = os.path.join(BASE_DIR, path)

    # Crear las carpetas si no existen
    try:
        os.makedirs(full_path, exist_ok=True)
    except Exception as e:
        return jsonify({"error": f"Could not create path: {e}"}), 500

    # Guardar el archivo en el path especificado
    file_path = os.path.join(full_path, file.filename)
    file.save(file_path)
    return jsonify({
        "message": f"File '{file.filename}' uploaded successfully to '{path or 'root'}'",
        "path": path
    }), 201

@app.route('/api/list/files', methods=['POST'])
def list_files():
    data = request.json
    folder_path = data.get('folder_path', '').strip('/')

    if not folder_path:
        return jsonify({"error": "The 'folder_path' parameter is required"}), 400

    # Construir el path completo basado en BASE_DIR
    full_path = os.path.join(BASE_DIR, folder_path)

    if not os.path.exists(full_path):
        return jsonify({"error": f"Folder '{folder_path}' does not exist"}), 404

    if not os.path.isdir(full_path):
        return jsonify({"error": f"The path '{folder_path}' is not a folder"}), 400

    try:
        files = os.listdir(full_path)
        return jsonify({"files": files}), 200
    except Exception as e:
        return jsonify({"error": f"Error listing files: {e}"}), 500

# Descargar un archivo
@app.route('/api/descarga', methods=['POST'])
def download_file(): 
    data = request.json
    ruta = data.get('ruta')
    file_name = data.get('file_name')
    
    if not ruta or not file_name:
        return jsonify({"error": "Los parámetros 'ruta' y 'file_name' son obligatorios"}), 400

    folder_path = os.path.join(BASE_DIR, ruta)
    if not os.path.exists(folder_path):
        return jsonify({"error": f"La carpeta '{ruta}' no existe"}), 404

    file_path = os.path.join(folder_path, file_name)
    if not os.path.exists(file_path):
        return jsonify({"error": f"El archivo '{file_name}' no existe en la ruta '{ruta}'"}), 404

    return send_from_directory(folder_path, file_name, as_attachment=True)
# Ejecución de la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
