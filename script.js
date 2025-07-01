document.getElementById("formulario").addEventListener("submit", async function (e) {
  e.preventDefault();

  const data = {
    autorizador: document.getElementById("autorizador").value.toUpperCase(),
    rut_autorizador: document.getElementById("rut_autorizador").value,
    autorizado: document.getElementById("autorizado").value.toUpperCase(),
    rut_autorizado: document.getElementById("rut_autorizado").value,
    tramite: document.getElementById("tramite").value.toUpperCase(),
    fecha: document.getElementById("fecha").value.toUpperCase()
  };

  try {
    const response = await fetch("https://poder-simple.onrender.com/generar_poder", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) throw new Error("Error al generar PDF");

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "poder_simple_cybernova.pdf";
    a.click();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    alert("Hubo un error al generar el PDF");
    console.error(error);
  }
});