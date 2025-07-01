from flask import Flask, request, send_file
from flask_cors import CORS
from generar_pdf import generar_pdf
import io

app = Flask(__name__)
CORS(app)

@app.route('/generar_pdf', methods=['POST'])
def generar():
    datos = request.get_json()
    pdf_bytes = generar_pdf(datos)
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='curriculum_cybernova.pdf'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
