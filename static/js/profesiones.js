document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-filtros");
  const resultados = document.getElementById("contenedor-resultados");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const params = new URLSearchParams(new FormData(form));

    try {
        resultados.innerHTML = "<p>Cargando carreras...</p>";

        const res = await fetch(`/api/filtrar-carreras?${params.toString()}`); // ✅ Corregido
        if (!res.ok) throw new Error("Error al buscar");

        const data = await res.json();
        console.log("🔍 Respuesta del backend:", data);

        // Asegurar que 'nombres' existe aunque el backend devuelva algo distinto
        const nombres = Array.isArray(data?.nombres) ? data.nombres : [];

        if (nombres.length === 0) {
            resultados.innerHTML = `
                <h3>Resultados de la búsqueda</h3>
                <p style="color: red;">No se encontraron carreras con esos filtros.</p>
            `;
            return;
        }

        const listHtml = nombres.map(n => `<li>${n}</li>`).join("");
        resultados.innerHTML = `
            <h3>Resultados de la búsqueda</h3>
            <ul>${listHtml}</ul>
        `;
    } catch (err) {
        console.error("❌ Error en la búsqueda:", err);
        resultados.innerHTML = `
            <h3>Error en la búsqueda</h3>
            <p style="color: red;">Ocurrió un error al cargar los datos. Revisa la consola del navegador para detalles.</p>
        `;
    }
  });
});