from fpdf import FPDF
import io
from PyPDF2 import PdfReader, PdfWriter

def generar_pdf(data):
    pdf = FPDF()
    pdf.add_page()

    # Título
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(40, 40, 80)
    nombre = data.get("nombre", "").upper()
    pdf.cell(0, 10, nombre, ln=1, align="C")

    # Datos personales
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)

    campos = [
        ("Email", data.get("email", "")),
        ("Teléfono", data.get("telefono", "")),
        ("Dirección", data.get("direccion", "")),
        ("Fecha nacimiento", data.get("fecha_nacimiento", "")),
        ("Nacionalidad", data.get("nacionalidad", "")),
        ("RUT", data.get("rut", "")),
        ("Estado civil", data.get("estado_civil", "")),
        ("Salud", data.get("sistema_salud", "")),
        ("AFP", data.get("afp", "")),
        ("Licencia conducir", data.get("licencia_conducir", ""))
    ]

    for label, valor in campos:
        if valor:
            pdf.multi_cell(0, 8, f"{label}: {valor}")

    pdf.ln(5)

    # Formación académica
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Formación Académica", ln=1)
    fechas = data.get("fecha", [])
    establecimientos = data.get("establecimiento", [])
    grados = data.get("grado", [])

    if not isinstance(fechas, list):
        fechas = [fechas]
    if not isinstance(establecimientos, list):
        establecimientos = [establecimientos]
    if not isinstance(grados, list):
        grados = [grados]

    for f, e, g in zip(fechas, establecimientos, grados):
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, f"{f} - {e} ({g})")

    pdf.ln(5)

    # Experiencia laboral
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Experiencia Laboral", ln=1)
    fechas_lab = data.get("fecha", [])
    empresas = data.get("empresa", [])
    cargos = data.get("cargo", [])

    if not isinstance(empresas, list):
        empresas = [empresas]
    if not isinstance(cargos, list):
        cargos = [cargos]
    if not isinstance(fechas_lab, list):
        fechas_lab = [fechas_lab]

    for f, emp, c in zip(fechas_lab, empresas, cargos):
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, f"{f} - {emp}, {c}")

    # Generar bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_buffer = io.BytesIO(pdf_bytes)

    # Marca de agua usando PyPDF2
    reader = PdfReader(pdf_buffer)
    writer = PdfWriter()

    for page in reader.pages:
        # Simular marca de agua usando overlay
        watermark = FPDF()
        watermark.add_page()
        watermark.set_font("Arial", "B", 50)
        watermark.set_text_color(200, 200, 200)
        watermark.rotate(45)
        watermark.text(50, 150, "CYBERNOVA")
        wm_bytes = watermark.output(dest='S').encode('latin1')
        wm_buffer = io.BytesIO(wm_bytes)
        wm_pdf = PdfReader(wm_buffer)

        # Fusionar watermark con la página original
        page.merge_page(wm_pdf.pages[0])
        writer.add_page(page)

    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)
    return output_buffer.read()
