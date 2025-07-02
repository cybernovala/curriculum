function agregarCampo(seccion) {
  const contenedor = document.getElementById(seccion);
  const grupo = document.createElement("div");
  grupo.className = "grupo";

  if (seccion === "academico") {
    grupo.innerHTML = `
      <input type="text" name="fecha" placeholder="2020-2025" required />
      <input type="text" name="establecimiento" placeholder="Establecimiento" required />
      <input type="text" name="grado" placeholder="E.Basica - Media Completa-Incompleta....." required />
    `;
  } else if (seccion === "laboral") {
    grupo.innerHTML = `
      <input type="text" name="fecha" placeholder="2020-2025" required />
      <input type="text" name="empresa" placeholder="Empresa" required />
      <input type="text" name="cargo" placeholder="Cargo" required />
    `;
  }
  contenedor.insertBefore(grupo, contenedor.lastElementChild);
}

document.getElementById("vista-previa").addEventListener("click", () => {
  const form = document.getElementById("formulario");
  const datos = new FormData(form);
  let html = "";
  for (let [key, value] of datos.entries()) {
    html += `<p><strong>${key}:</strong> ${value}</p>`;
  }
  document.getElementById("vista-previa-contenido").innerHTML = html;
  document.getElementById("vista-previa-container").style.display = "block";
  document.getElementById("botones-acciones").style.display = "block";
});

document.getElementById("modificar").addEventListener("click", () => {
  document.getElementById("vista-previa-container").style.display = "none";
  document.getElementById("botones-acciones").style.display = "none";
});

document.getElementById("btn-generar").addEventListener("click", async () => {
  const form = document.getElementById("formulario");
  const datos = new FormData(form);
  const json = {};

  // Convertir los datos del formulario en un objeto JSON correctamente estructurado
  for (let [key, value] of datos.entries()) {
    if (!json[key]) {
      json[key] = value;
    } else if (!Array.isArray(json[key])) {
      json[key] = [json[key], value]; // Convertir en array si ya existe un valor
    } else {
      json[key].push(value); // Añadir al array si ya existe
    }
  }

  // Enviar los datos al servidor para generar el PDF
  const response = await fetch("https://curriculum-9s9x.onrender.com/generar_pdf", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(json),
  });

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "curriculum_cybernova.pdf";
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
  document.getElementById("mensaje-descarga").style.display = "block";
});
