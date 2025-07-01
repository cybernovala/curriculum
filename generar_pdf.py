from fpdf import FPDF
import io
from PyPDF2 import PdfReader, PdfWriter

def generar_pdf(data):
    pdf = FPDF()
    pdf.add_page()

    # Título principal
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(40, 40, 80)
    nombre = data.get("nombre", "").upper()
    pdf.cell(0, 15, nombre, ln=1, align="C")

    y_actual = pdf.get_y() + 5

    # Columna lateral
    pdf.set_fill_color(230, 230, 230)
    pdf.rect(10, y_actual, 40, 250 - y_actual, 'F')

    # Línea horizontal
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
        ("EMAIL", data.get("email", "")),
        ("TELÉFONO", data.get("telefono", "")),
        ("DIRECCIÓN", data.get("direccion", "")),
        ("FECHA DE NACIMIENTO", data.get("fecha_nacimiento", "")),
        ("NACIONALIDAD", data.get("nacionalidad", "")),
        ("RUT", data.get("rut", "")),
        ("ESTADO CIVIL", data.get("estado_civil", "")),
        ("SISTEMA DE SALUD", data.get("sistema_salud", "")),
        ("AFP", data.get("afp", "")),
        ("LICENCIA DE CONDUCIR", data.get("licencia_conducir", ""))
    ]

    for label, valor in campos:
        if valor:
            pdf.multi_cell(0, 8, f"{label}: {valor.upper()}", border=0)
    pdf.ln(3)

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
        texto = f"{f} - {e.upper()} ({g.upper()})"
        pdf.multi_cell(0, 8, texto, border=0)
    pdf.ln(3)

    pdf.set_draw_color(150, 150, 150)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Experiencia laboral
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "EXPERIENCIA LABORAL", ln=1)

    fechas_lab = data.get("fecha", [])
    empresas = data.get("empresa", [])
    cargos = data.get("cargo", [])

    if not isinstance(empresas, list):
        empresas = [empresas]
    if not isinstance(cargos, list):
        cargos = [cargos]
    if not isinstance(fechas_lab, list):
        fechas_lab = [fechas_lab]

    pdf.set_font("Arial", "", 12)
    for f, emp, c in zip(fechas_lab, empresas, cargos):
        texto = f"{f} - {emp.upper()}, {c.upper()}"
        pdf.multi_cell(0, 8, texto, border=0)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_buffer = io.BytesIO(pdf_bytes)

    reader = PdfReader(pdf_buffer)
    writer = PdfWriter()

    # Marca de agua corregida: cubrir todo el ancho
    for page in reader.pages:
        wm_pdf = FPDF()
        wm_pdf.add_page()

        wm_pdf.set_font("Arial", "B", 70)
        wm_pdf.set_text_color(220, 220, 220)

        # Repetir varias veces para cubrir
        for y in range(0, 300, 60):
            wm_pdf.rotate(45, x=0, y=0)
            wm_pdf.text(-50, y, "CYBERNOVA      CYBERNOVA      CYBERNOVA")
            wm_pdf.rotate(0)

        wm_bytes = wm_pdf.output(dest='S').encode('latin1')
        wm_buffer = io.BytesIO(wm_bytes)
        wm_reader = PdfReader(wm_buffer)

        page.merge_page(wm_reader.pages[0])
        writer.add_page(page)

    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)
    return output_buffer.read()
