from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime
import io

def generar_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)

    pdf.set_xy(10, 20)
    pdf.cell(0, 10, "PODER SIMPLE", ln=True, align="C")

    pdf.set_font("Arial", "", 14)
    pdf.ln(10)

    texto = f"""
YO, {data['autorizador']}, RUT {data['rut_autorizador']}, 
AUTORIZO A {data['autorizado']}, RUT {data['rut_autorizado']}, 
PARA REALIZAR EL SIGUIENTE TRÁMITE: {data['tramite']}.
"""

    for line in texto.strip().split('\n'):
        pdf.multi_cell(0, 10, line.strip())

    # Fecha final
    pdf.ln(20)
    fecha_actual = datetime.now().strftime("LOS ÁNGELES, %-d DE %B DE %Y").upper()
    pdf.cell(0, 10, fecha_actual, ln=True, align="R")

    # Guardar en buffer
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    # Aplicar contraseña
    reader = PdfReader(buffer)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt("@@1234@@")

    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()
