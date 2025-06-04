const API_BASE = "http://localhost:8001/api/v1/items";

const mostrarResultado = (items) => {
  const container = document.getElementById("resultados");
  container.innerHTML = "";

  if (!Array.isArray(items)) items = [items];

  items.forEach(item => {
    const div = document.createElement("div");
    div.className = "item";
    div.innerHTML = `<strong>${item.name}</strong><br>
                     Precio: $${item.price}<br>
                     Código: ${item.barcode}`;
    container.appendChild(div);
  });
};

const mostrarError = (mensaje) => {
  document.getElementById("errorMsg").innerText = mensaje;
  document.getElementById("resultados").innerHTML = "";
};

const limpiarErrores = () => {
  document.getElementById("errorMsg").innerText = "";
};

async function buscarPorId() {
  limpiarErrores();
  const id = document.getElementById("idInput").value;
  if (!id) return mostrarError("Ingresá un ID válido");

  try {
    const res = await fetch(`${API_BASE}/${id}`);
    if (!res.ok) throw new Error("No encontrado");
    const data = await res.json();
    mostrarResultado(data);
  } catch {
    mostrarError("Item no encontrado por ID.");
  }
}

async function buscarPorCodigo() {
  limpiarErrores();
  const code = document.getElementById("barcodeInput").value;
  if (!code) return mostrarError("Ingresá un código válido");

  try {
    const res = await fetch(`${API_BASE}/barcode/${code}`);
    if (!res.ok) throw new Error("No encontrado");
    const data = await res.json();
    mostrarResultado(data);
  } catch {
    mostrarError("Item no encontrado por código.");
  }
}

    