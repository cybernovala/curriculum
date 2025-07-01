from flask import Flask, request, send_file
from flask_cors import CORS
from generar_pdf import generar_pdf
import io

app = Flask(__name__)
CORS(app)

@app.route("/generar_poder", methods=["POST"])
def generar_poder():
    data = request.get_json()
    pdf_bytes = generar_pdf(data)
    return send_file(
        io.BytesIO(pdf_bytes),
        download_name="poder_simple.pdf",
        as_attachment=True,
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run()
