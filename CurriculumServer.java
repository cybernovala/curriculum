import fi.iki.elonen.NanoHTTPD;
import com.lowagie.text.*;
import com.lowagie.text.pdf.PdfWriter;
import java.io.*;
import java.util.Map;
import org.json.JSONObject;

public class CurriculumServer extends NanoHTTPD {
    public CurriculumServer() throws IOException {
        super(8080);
        start(NanoHTTPD.SOCKET_READ_TIMEOUT, false);
        System.out.println("Servidor iniciado en http://localhost:8080/recibirCV");
    }

    @Override
    public Response serve(IHTTPSession session) {
        if (Method.POST.equals(session.getMethod()) && session.getUri().equals("/recibirCV")) {
            try {
                // Leer el cuerpo JSON
                session.parseBody(new java.util.HashMap<>());
                InputStream inputStream = session.getInputStream();
                ByteArrayOutputStream result = new ByteArrayOutputStream();
                byte[] buffer = new byte[1024];
                int length;
                while ((length = inputStream.read(buffer)) != -1) {
                    result.write(buffer, 0, length);
                }
                String jsonStr = result.toString("UTF-8");
                JSONObject json = new JSONObject(jsonStr);

                // Generar PDF
                String filePath = "curriculum_" + json.getString("nombre").replace(" ", "_") + ".pdf";
                Document document = new Document();
                PdfWriter.getInstance(document, new FileOutputStream(filePath));
                document.open();
                document.add(new Paragraph("Currículum Vitae\n\n"));
                document.add(new Paragraph("Nombre completo: " + json.getString("nombre")));
                document.add(new Paragraph("Fecha de nacimiento: " + json.getString("fecha_nac")));
                document.add(new Paragraph("RUT: " + json.getString("rut")));
                document.add(new Paragraph("Correo: " + json.getString("correo")));
                document.add(new Paragraph("Teléfono: " + json.getString("telefono")));
                document.add(new Paragraph("Datos académicos: " + json.getString("academicos")));
                document.add(new Paragraph("Datos laborales: " + json.getString("laborales")));
                document.add(new Paragraph("Sistema de salud: " + json.getString("salud")));
                document.add(new Paragraph("Previsión: " + json.getString("prevision")));
                document.add(new Paragraph("Licencia de conducir: " + json.getString("licencia")));
                document.close();

                return newFixedLengthResponse(Response.Status.OK, "text/plain", "PDF generado: " + filePath);
            } catch (Exception e) {
                return newFixedLengthResponse(Response.Status.INTERNAL_ERROR, "text/plain", "Error: " + e.getMessage());
            }
        }
        return newFixedLengthResponse(Response.Status.NOT_FOUND, "text/plain", "Not found");
    }

    public static void main(String[] args) {
        try {
            new CurriculumServer();
        } catch (IOException ioe) {
            System.err.println("No se pudo iniciar el servidor: " + ioe.getMessage());
        }
    }
}