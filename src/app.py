from flask import Flask, request, jsonify,render_template,url_for
import os
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import json

app = Flask(__name__)  # inicio de la aplicación

@app.route('/')
def inicio():
    return render_template('base.html')

@app.route('/datos', methods=['GET','POST'])
def obtener_datos():
    archivo_credenciales = request.files['file-select'] # obtenemos el archivo.

    # Guardar el archivo temporalmente en el servidor
    credenciales_path = os.path.join('temp', 'firebase_credentials.json')
    archivo_credenciales.save(credenciales_path)
    if not firebase_admin._apps:
        credencial = credentials.Certificate(credenciales_path) # proporcionamos la ruta del archivo
        firebase_admin.initialize_app(credencial)

    # Desinicializa la aplicación Firebase actual, si existe
    if firebase_admin._apps:
        firebase_admin.delete_app(firebase_admin.get_app())

    # Inicializa Firebase con el nuevo archivo de credenciales
    credencial = credentials.Certificate(credenciales_path)
    firebase_admin.initialize_app(credencial)

    # Inicializando la conexión con Firebase
    db = firestore.client()  # conexión a la base de datos de Firebase

    # Accediendo a una colección de Firestore
    coleccion_ref = db.collection(f'{request.form['respaldo']}')
    docs = coleccion_ref.stream()

    # Recogiendo los datos de los documentos
    datos = []
    for doc in docs:
        doc_dict = doc.to_dict()
        datos.append(doc_dict)

    # Obtener la fecha actual para crear la carpeta
    fecha_hoy = datetime.datetime.now().strftime('%d-%m-%Y')
    carpeta_destino = os.path.join(os.environ['HOME'],'Documents', 'respaldos', f"{request.form['nombre']} {fecha_hoy}")

    # Crear la carpeta si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    # Guardar los datos en un archivo JSON dentro de la carpeta
    archivo_destino = os.path.join(carpeta_destino, f'{request.form['respaldo']}.json')
    with open(archivo_destino, 'w') as f:
        json.dump(datos, f, indent=4)
    
    os.remove(credenciales_path)

    return jsonify(datos)

if __name__ == '__main__':  # corre la aplicación en caso de estar como principal
    app.run()