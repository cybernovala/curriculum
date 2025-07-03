// Generar y guardar marca única si no existe
function obtenerMarcaUsuario() {
  let marca = localStorage.getItem("marca_cybernova");
  if (!marca) {
    // Crear una marca aleatoria simple (ej: con timestamp + random)
    marca = "usuario_" + Date.now() + "_" + Math.floor(Math.random() * 10000);
    localStorage.setItem("marca_cybernova", marca);
  }
  return marca;
}

// Función para agregar campos
function agregarCampo(seccion) {
  const contenedor = document.getElementById(seccion);
  const grupo = document.createElement("div");
  grupo.className = "grupo";

  if (seccion === "academico") {
    grupo.innerHTML = `
      <input type="text" name="fecha_formacion" placeholder="2020-2025" required />
      <input type="text" name="establecimiento" placeholder="Establecimiento" required />
      <input type="text" name="grado" placeholder="E.Basica - Media Completa-Incompleta....." required />
    `;
  } else if (seccion === "laboral") {
    grupo.innerHTML = `
      <input type="text" name="fecha_experiencia" placeholder="2020-2025" required />
      <input type="text" name="empresa" placeholder="Empresa" required />
      <input type="text" name="cargo" placeholder="Cargo" required />
    `;
  }
  contenedor.insertBefore(grupo, contenedor.lastElementChild);
}

// Evento para generar PDF
document.getElementById("btn-generar").addEventListener("click", async () => {
  const form = document.getElementById("formulario");
  const datos = new FormData(form);
  const json = {};

  // Convertir los datos en objeto JSON
  for (let [key, value] of datos.entries()) {
    if (!json[key]) {
      json[key] = value;
    } else if (!Array.isArray(json[key])) {
      json[key] = [json[key], value];
    } else {
      json[key].push(value);
    }
  }

  // Agregar la marca única
  json["marca"] = obtenerMarcaUsuario();

  // Enviar al servidor
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
