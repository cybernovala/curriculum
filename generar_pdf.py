from fpdf import FPDF
import io
from PyPDF2 import PdfReader, PdfWriter

class PDFWithFooter(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "BI", 18)
        self.set_text_color(200, 200, 200)
        self.cell(0, 10, "Curriculum vitae", 0, 0, "R")

def generar_pdf(data, admin=False):
    pdf = PDFWithFooter()
    pdf.add_page()

    # Título: Nombre
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(40, 40, 80)
    nombre = data.get("nombre", "").upper()
    pdf.cell(0, 12, nombre, ln=1, align="C")

    # Email y Teléfono debajo
    pdf.set_font("Arial", "", 12)
    email = data.get("email", "").upper()
    telefono = data.get("telefono", "").upper()
    if email:
        pdf.cell(0, 6, email, ln=1, align="C")
    if telefono:
        pdf.cell(0, 6, telefono, ln=1, align="C")

    y_actual = pdf.get_y() + 5

    # Columna lateral decorativa
    pdf.set_fill_color(230, 230, 230)
    pdf.rect(10, y_actual, 40, 250 - y_actual, 'F')

    # Línea horizontal decorativa
    pdf.set_draw_color(50, 50, 150)
    pdf.set_line_width(0.8)
    pdf.line(10, y_actual, 200, y_actual)
    pdf.ln(8)

    # Datos personales
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "DATOS PERSONALES", ln=1)
    pdf.set_font("Arial", "", 12)

    campos = [
        ("RUT", data.get("rut", "")),
        ("FECHA DE NACIMIENTO", data.get("fecha_nacimiento", "")),
        ("DIRECCIÓN", data.get("direccion", "")),
        ("NACIONALIDAD", data.get("nacionalidad", "")),
        ("ESTADO CIVIL", data.get("estado_civil", "")),
        ("SISTEMA DE SALUD", data.get("sistema_salud", "")),
        ("AFP", data.get("afp", "")),
        ("LICENCIA DE CONDUCIR", data.get("licencia_conducir", ""))
    ]

    for label, valor in campos:
        if valor:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(60, 8, f"{label}:", border=0)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 8, valor.upper(), border=0)
    pdf.ln(3)

    # Línea divisoria
    pdf.set_draw_color(150, 150, 150)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Formación académica
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "FORMACIÓN ACADÉMICA", ln=1)

    fechas = data.get("fecha", [])
    establecimientos = data.get("establecimiento", [])
    grados = data.get("grado", [])

    if not isinstance(fechas, list):
        fechas = [fechas]
    if not isinstance(establecimientos, list):
        establecimientos = [establecimientos]
    if not isinstance(grados, list):
        grados = [grados]

    pdf.set_font("Arial", "", 12)
    for f, e, g in zip(fechas, establecimientos, grados):
        pdf.cell(0, 8, f"{g} - {e} ({f})", ln=1)

    # Experiencia Laboral
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "EXPERIENCIA LABORAL", ln=1)

    cargos = data.get("cargo", [])
    lugares = data.get("lugar", [])
    periodos = data.get("periodo", [])

    if not isinstance(cargos, list):
        cargos = [cargos]
    if not isinstance(lugares, list):
        lugares = [lugares]
    if not isinstance(periodos, list):
        periodos = [periodos]

    pdf.set_font("Arial", "", 12)
    for c, l, p in zip(cargos, lugares, periodos):
        pdf.multi_cell(0, 8, f"{c} - {l} ({p})", border=0)

    if admin:
        # Marca de agua (solo admin)
        pdf.set_font("Arial", "I", 100)
        pdf.set_text_color(180, 180, 180)
        pdf.text(60, 100, "Sin marca de agua")

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output.read()
