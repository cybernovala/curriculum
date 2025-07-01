from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from generar_pdf import generar_pdf
import io
import json
import os

app = Flask(__name__)
CORS(app)

DB_FILE = "datos_guardados.json"

def guardar_datos(data):
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = []

    datos.append(data)

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

@app.route("/generar_pdf", methods=["POST"])
def generar_pdf_route():
    data = request.json

    guardar_datos(data)

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

if __name__ == "__main__":
    app.run(debug=True)
