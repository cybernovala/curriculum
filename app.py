from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from generar_pdf import generar_pdf
import io
import json
import os

app = Flask(__name__)
CORS(app)

DB_FILE = "datos_guardados.json"
LOG_FILE = "datos_legibles.txt"

def guardar_o_actualizar_datos(data):
    marca = data.get("marca")
    if not marca:
        return

    # Leer JSON actual
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = []

    actualizado = False

    # Buscar por marca
    for i, item in enumerate(datos):
        if item.get("marca") == marca:
            datos[i] = data
            actualizado = True
            break

    if not actualizado:
        datos.append(data)

    # Guardar archivo JSON normal
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

    # Guardar archivo legible con bloques separados
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        for item in datos:
            f.write("============================\n")
            f.write(f"Usuario: {item.get('marca', 'sin_marca')}\n")
            f.write(json.dumps(item, indent=4, ensure_ascii=False))
            f.write("\n\n")

@app.route("/generar_pdf", methods=["POST"])
def generar_pdf_route():
    data = request.json

    # Guardar o actualizar
    guardar_o_actualizar_datos(data)

    # Preparar listas
    if isinstance(data.get("fecha_formacion"), str):
        data["fecha_formacion"] = [data["fecha_formacion"]]
    if isinstance(data.get("establecimiento"), str):
        data["establecimiento"] = [data["establecimiento"]]
    if isinstance(data.get("grado"), str):
        data["grado"] = [data["grado"]]
    
    if isinstance(data.get("fecha_experiencia"), str):
        data["fecha_experiencia"] = [data["fecha_experiencia"]]
    if isinstance(data.get("empresa"), str):
        data["empresa"] = [data["empresa"]]
    if isinstance(data.get("cargo"), str):
        data["cargo"] = [data["cargo"]]

    pdf_bytes = generar_pdf(data, admin=False)

    return send_file(io.BytesIO(pdf_bytes), as_attachment=True, download_name="curriculum_cybernova.pdf", mimetype="application/pdf")

@app.route("/generar_pdf_admin", methods=["POST"])
def generar_pdf_admin_route():
    datos = request.json
    clave = datos.get("clave")
    if clave != "@@ADMIN123@@":
        return jsonify({"error": "Clave incorrecta"}), 403

    data_cv = datos.get("data")
    if not data_cv:
        return jsonify({"error": "Faltan datos"}), 400

    pdf_bytes = generar_pdf(data_cv, admin=True)
    return send_file(io.BytesIO(pdf_bytes), as_attachment=True, download_name="curriculum_sin_marca.pdf", mimetype="application/pdf")

@app.route("/ver_datos", methods=["GET"])
def ver_datos():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return jsonify(datos)
    else:
        return jsonify([])

@app.route("/borrar_datos", methods=["POST"])
def borrar_datos():
    datos = request.json
    clave = datos.get("clave")
    if clave != "@@ADMIN123@@":
        return jsonify({"error": "Clave incorrecta"}), 403

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    return jsonify({"mensaje": "✅ Datos borrados correctamente."})

if __name__ == "__main__":
    app.run(debug=True)
