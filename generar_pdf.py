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
    # Crear el PDF
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

    # Asegurar que las fechas, establecimientos y grados sean listas
    fechas = data.get("fecha_formacion", [])
    establecimientos = data.get("establecimiento", [])
    grados = data.get("grado", [])

    # Convertir a listas si no lo son
    if not isinstance(fechas, list):
        fechas = [fechas]
    if not isinstance(establecimientos, list):
        establecimientos = [establecimientos]
    if not isinstance(grados, list):
        grados = [grados]

    pdf.set_font("Arial", "", 12)
    for f, e, g in zip(fechas, establecimientos, grados):
        pdf.set_font("Arial", "", 12)
        pdf.cell(60, 8, f, border=0)
        pdf.multi_cell(0, 8, f"{e.upper()} ({g.upper()})", border=0)
    pdf.ln(3)

    # Línea divisoria
    pdf.set_draw_color(150, 150, 150)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Experiencia laboral
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "EXPERIENCIA LABORAL", ln=1)

    # Asegurar que las fechas de experiencia laboral sean listas
    fechas_lab = data.get("fecha_experiencia", [])
    empresas = data.get("empresa", [])
    cargos = data.get("cargo", [])

    if not isinstance(fechas_lab, list):
        fechas_lab = [fechas_lab]
    if not isinstance(empresas, list):
        empresas = [empresas]
    if not isinstance(cargos, list):
        cargos = [cargos]

    pdf.set_font("Arial", "", 12)
    for f, emp, c in zip(fechas_lab, empresas, cargos):
        pdf.set_font("Arial", "", 12)
        pdf.cell(60, 8, f, border=0)
        pdf.multi_cell(0, 8, f"{emp.upper()}, {c.upper()}", border=0)

    # Convertir a bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_buffer = io.BytesIO(pdf_bytes)

    # Leer el PDF generado
    reader = PdfReader(pdf_buffer)
    writer = PdfWriter()

    # Si no es admin, agregar marca de agua
    if not admin:
        for page in reader.pages:
            # Crear un PDF con la marca de agua
            wm_pdf = FPDF()
            wm_pdf.add_page()
            wm_pdf.set_font("Arial", "B", 70)
            wm_pdf.set_text_color(245, 245, 245)

            # Aplicar la marca de agua inclinada
            for y in range(0, 300, 140):
                wm_pdf.rotate(45, x=0, y=0)
                wm_pdf.text(-50, y, "  CYBERNOVA     CYBERNOVA       CYBERNOVA")
                wm_pdf.rotate(0)

            wm_bytes = wm_pdf.output(dest='S').encode('latin1')
            wm_buffer = io.BytesIO(wm_bytes)
            wm_reader = PdfReader(wm_buffer)

            # Mezclar la marca de agua con la página existente
            page.merge_page(wm_reader.pages[0])
            writer.add_page(page)
    else:
        for page in reader.pages:
            writer.add_page(page)

    # Escribir el PDF final con marca de agua o sin ella
    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)

    return output_buffer.read()
