import os
import datetime
import json
from flask import Flask, request, redirect, render_template, url_for, flash
import firebase_admin
from firebase_admin import credentials, firestore
from google.protobuf.timestamp_pb2 import Timestamp
from google.cloud.firestore_v1._helpers import DatetimeWithNanoseconds

# Función para convertir Timestamps a ISO 8601
def convert_timestamp(doc_dict):
    for key, value in doc_dict.items():
        if isinstance(value, Timestamp):
            doc_dict[key] = value.ToDatetime().isoformat()
    return doc_dict

# Custom JSON serializer for DatetimeWithNanoseconds
def custom_serializer(obj):
    if isinstance(obj, DatetimeWithNanoseconds):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

app = Flask(__name__)  # inicio de la aplicación
app.secret_key = "nota_poner_clave_sifrada"

@app.route('/')
def inicio():
    return render_template('descarga.html')

@app.route('/ingresar_datos')
def ingresar():
    return render_template('ingreso.html')

@app.route('/mandar_datos', methods= ['GET','POST'])
def mandar():
    if request.method == 'POST':
        archivo_credenciales = request.files['credenciales']  # obtenemos el archivo de las credenciales.
        archivo_db = request.files['backup'] # obtenenmos el archivo del backup
        try:
            # Guardar el archivo de las credenciales temporalmente en el servidor
            credenciales_path = os.path.join('temp', 'firebase_credentials.json')
            archivo_credenciales.save(credenciales_path)
            
            # Guarda el back temporamlente en el servidor
            backup_path = os.path.join('temp', 'backup.json')
            archivo_db.save(backup_path)

            # Si no hay aplicaciones de Firebase inicializadas, inicializamos una
            if not firebase_admin._apps:
                credencial = credentials.Certificate(credenciales_path)  # proporcionamos la ruta del archivo
                firebase_admin.initialize_app(credencial)

            # Desinicializa la aplicación Firebase actual, si existe
            if firebase_admin._apps:
                firebase_admin.delete_app(firebase_admin.get_app())

            # Inicializa Firebase con el nuevo archivo de credenciales
            credencial = credentials.Certificate(credenciales_path)
            firebase_admin.initialize_app(credencial)
            
            with open(backup_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # 🔍 Verifica que el JSON tenga el formato correcto
            if not isinstance(data, dict):
                flash("❌ Error: El archivo JSON debe contener un diccionario con colecciones y documentos", "danger")
                return redirect(url_for('ingresar'))

            db = firestore.client()  # Conectar a Firestore

            for collection, documents in data.items():
                if isinstance(documents, list):  #  Si es una lista, generamos IDs automáticos
                    for doc_data in documents:
                        db.collection(collection).add(doc_data)  #  Se usa 'add()' en lugar de 'set()'
                elif isinstance(documents, dict):  # Si es un diccionario, usamos las claves como IDs
                    for doc_id, doc_data in documents.items():
                        db.collection(collection).document(doc_id).set(doc_data)
                else:
                    flash(f"❌ Error: La colección '{collection}' tiene un formato incorrecto", "danger")
                    return redirect(url_for('ingresar'))
            
            os.remove(backup_path)
            os.remove(credenciales_path)

        except Exception as e:
                flash(f"❌ Error: {e}", "danger")

        return redirect(url_for('ingresar'))

@app.route('/datos_completos', methods=['POST'])
def obtener_datos2():
    archivo_credenciales = request.files['file-select']  # obtenemos el archivo.

    # Guardar el archivo temporalmente en el servidor
    credenciales_path = os.path.join('temp', 'firebase_credentials.json')
    archivo_credenciales.save(credenciales_path)
    
    # Si no hay aplicaciones de Firebase inicializadas, inicializamos una
    if not firebase_admin._apps:
        credencial = credentials.Certificate(credenciales_path)  # proporcionamos la ruta del archivo
        firebase_admin.initialize_app(credencial)

    # Desinicializa la aplicación Firebase actual, si existe
    if firebase_admin._apps:
        firebase_admin.delete_app(firebase_admin.get_app())

    # Inicializa Firebase con el nuevo archivo de credenciales
    credencial = credentials.Certificate(credenciales_path)
    firebase_admin.initialize_app(credencial)

    # Inicializando la conexión con Firebase
    db = firestore.client()  # conexión a la base de datos de Firebase

    # Obtener todas las colecciones de la base de datos
    colecciones = db.collections()

    # Recoger todos los documentos de todas las colecciones
    datos = {}
    for coleccion in colecciones:
        # Almacenamos los documentos de la colección en una lista
        docs = coleccion.stream()
        coleccion_data = []
        
        for doc in docs:
            doc_dict = doc.to_dict()
            convert_timestamp(doc_dict)
            coleccion_data.append(doc_dict)
        
        # Solo agregar la colección si tiene documentos
        if coleccion_data:
            datos[coleccion.id] = coleccion_data  # coleccion.id contiene el nombre de la colección

    # Obtener la fecha actual para crear la carpeta (solo funciona en mac)
    fecha_hoy = datetime.datetime.now().strftime('%d-%m-%Y')
    carpeta_destino = os.path.join(os.environ['HOME'], 'Documents', 'respaldos', f"{request.form['nombre']} {fecha_hoy}")

    # Crear la carpeta si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    # Guardar los datos en un archivo JSON dentro de la carpeta
    archivo_destino = os.path.join(carpeta_destino, f"{request.form['nombre_ar']} {fecha_hoy}.json")
    with open(archivo_destino, 'w') as f:
        json.dump(datos, f, indent=4, default=custom_serializer)

    os.remove(credenciales_path)

    return redirect(url_for('inicio'))

@app.route('/datos_coleccion', methods=['POST'])
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
    coleccion_ref = db.collection(f"{request.form['respaldo']}")
    docs = coleccion_ref.stream()

    # Recogiendo los datos de los documentos
    datos = []
    for doc in docs:
        doc_dict = doc.to_dict()
        convert_timestamp(doc_dict)

        datos.append(doc_dict)

    # Obtener la fecha actual para crear la carpeta en este caso solo funciona en mac.
    fecha_hoy = datetime.datetime.now().strftime('%d-%m-%Y')
    carpeta_destino = os.path.join(os.environ['HOME'], 'Documents', 'respaldos', f"{request.form['nombre']} {fecha_hoy}")

    # Crear la carpeta si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    # Guardar los datos en un archivo JSON dentro de la carpeta
    archivo_destino = os.path.join(carpeta_destino, f"{request.form['respaldo']}.json")
    with open(archivo_destino, 'w') as f:
        json.dump(datos, f, indent=4, default=custom_serializer)
    
    os.remove(credenciales_path)

    return redirect(url_for('inicio'))

if __name__ == '__main__':  # corre la aplicación en caso de estar como principal
    app.run()

    # HM Info202401.
