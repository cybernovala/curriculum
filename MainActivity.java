package com.example.curriculumapp;

import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import org.json.JSONObject;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends AppCompatActivity {
    EditText etNombre, etFechaNac, etRut, etCorreo, etTelefono, etAcademicos, etLaborales, etSalud, etPrevision, etLicencia;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        etNombre = findViewById(R.id.etNombre);
        etFechaNac = findViewById(R.id.etFechaNac);
        etRut = findViewById(R.id.etRut);
        etCorreo = findViewById(R.id.etCorreo);
        etTelefono = findViewById(R.id.etTelefono);
        etAcademicos = findViewById(R.id.etAcademicos);
        etLaborales = findViewById(R.id.etLaborales);
        etSalud = findViewById(R.id.etSalud);
        etPrevision = findViewById(R.id.etPrevision);
        etLicencia = findViewById(R.id.etLicencia);

        findViewById(R.id.btnEnviar).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                enviarDatos();
            }
        });
    }

    private void enviarDatos() {
        new Thread(() -> {
            try {
                JSONObject json = new JSONObject();
                json.put("nombre", etNombre.getText().toString());
                json.put("fecha_nac", etFechaNac.getText().toString());
                json.put("rut", etRut.getText().toString());
                json.put("correo", etCorreo.getText().toString());
                json.put("telefono", etTelefono.getText().toString());
                json.put("academicos", etAcademicos.getText().toString());
                json.put("laborales", etLaborales.getText().toString());
                json.put("salud", etSalud.getText().toString());
                json.put("prevision", etPrevision.getText().toString());
                json.put("licencia", etLicencia.getText().toString());

                // Cambia la IP por la de tu PC en la red local
                URL url = new URL("http://192.168.1.100:8080/recibirCV");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json; utf-8");
                conn.setDoOutput(true);

                OutputStream os = conn.getOutputStream();
                os.write(json.toString().getBytes());
                os.flush();
                os.close();

                int responseCode = conn.getResponseCode();
                runOnUiThread(() -> Toast.makeText(this, responseCode == 200 ? "Enviado" : "Error", Toast.LENGTH_SHORT).show());
            } catch (Exception e) {
                runOnUiThread(() -> Toast.makeText(this, "Error: " + e.getMessage(), Toast.LENGTH_LONG).show());
            }
        }).start();
    }
}