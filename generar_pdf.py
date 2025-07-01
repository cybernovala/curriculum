from fpdf import FPDF
import io
from PyPDF2 import PdfReader, PdfWriter, PageObject

def generar_pdf(data):
    pdf = FPDF()
    pdf.add_page()

    # Dibujar líneas verticales para diseño moderno
    pdf.set_draw_color(100, 100, 255)
    pdf.set_line_width(0.5)
    pdf.line(70, 10, 70, 287)  # Línea vertical izquierda
    pdf.line(140, 10, 140, 287)  # Línea vertical derecha

    # Título principal
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(40, 40, 80)
    nombre = data.get("nombre", "").upper()
    pdf.cell(0, 15, nombre, ln=1, align="C")

    # Línea horizontal
    pdf.set_draw_color(50, 50, 150)
    pdf.set_line_width(0.8)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

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

    # Línea horizontal divisoria
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

    # Línea horizontal divisoria
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

    # Exportar a bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_buffer = io.BytesIO(pdf_bytes)

    # Leer el PDF base
    reader = PdfReader(pdf_buffer)
    writer = PdfWriter()

    # Agregar marca de agua en cada página
    for page in reader.pages:
        watermark_pdf = FPDF()
        watermark_pdf.add_page()
        watermark_pdf.set_font("Arial", "B", 50)
        watermark_pdf.set_text_color(200, 200, 200)
        watermark_pdf.rotate(45, x=None, y=None)
        watermark_pdf.text(40, 150, "CYBERNOVA")
        wm_bytes = watermark_pdf.output(dest='S').encode('latin1')
        wm_buffer = io.BytesIO(wm_bytes)
        wm_reader = PdfReader(wm_buffer)

        # Crear nueva página combinada
        page.merge_page(wm_reader.pages[0])
        writer.add_page(page)

    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)
    return output_buffer.read()
