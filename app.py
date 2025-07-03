@app.route("/borrar_usuario", methods=["POST"])
def borrar_usuario():
    datos = request.json
    clave = datos.get("clave")
    marca = datos.get("marca")

    if clave != "@@ADMIN123@@":
        return jsonify({"error": "Clave incorrecta"}), 403

    if not marca:
        return jsonify({"error": "Falta la marca del usuario"}), 400

    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            lista_datos = json.load(f)

        nueva_lista = [item for item in lista_datos if item.get("marca") != marca]

        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(nueva_lista, f, indent=4, ensure_ascii=False)

        return jsonify({"mensaje": f"✅ Usuario con marca '{marca}' borrado correctamente."})
    else:
        return jsonify({"mensaje": "No hay datos guardados."})
