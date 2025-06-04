const API_BASE = "http://localhost:8001/api/v1/items";

// Estado de la aplicación
let todosLosProductos = [];
let isLoading = false;

// Elementos del DOM
const elementos = {
  resultados: document.getElementById("resultados"),
  errorMsg: document.getElementById("errorMsg"),
  successMsg: document.getElementById("successMsg"),
  loading: document.getElementById("loading"),
  idInput: document.getElementById("idInput"),
  barcodeInput: document.getElementById("barcodeInput")
};

// Funciones de utilidad
const mostrarLoading = (show = true) => {
  elementos.loading.classList.toggle('show', show);
  isLoading = show;
};

const limpiarMensajes = () => {
  elementos.errorMsg.classList.remove('show');
  elementos.successMsg.classList.remove('show');
};

const mostrarError = (mensaje) => {
  limpiarMensajes();
  elementos.errorMsg.textContent = mensaje;
  elementos.errorMsg.classList.add('show');
  elementos.resultados.innerHTML = "";
};

const mostrarExito = (mensaje) => {
  limpiarMensajes();
  elementos.successMsg.textContent = mensaje;
  elementos.successMsg.classList.add('show');
};

const mostrarResultados = (items, esReset = false) => {
  limpiarMensajes();
  
  if (!Array.isArray(items)) {
    items = [items];
  }

  if (items.length === 0) {
    elementos.resultados.innerHTML = `
      <div class="empty-state">
        <h3>No se encontraron productos</h3>
        <p>Intenta con otro término de búsqueda</p>
      </div>
    `;
    return;
  }

  const header = esReset ? 
    `<div class="results-header">
      <div class="results-count">Mostrando todos los productos (${items.length})</div>
    </div>` :
    `<div class="results-header">
      <div class="results-count">${items.length} producto(s) encontrado(s)</div>
    </div>`;

  const itemsHTML = items.map(item => `
    <div class="item">
      <div class="item-name">${item.name || 'Sin nombre'}</div>
      <div class="item-price">$${item.price ? parseFloat(item.price).toLocaleString('es-AR', {minimumFractionDigits: 2}) : '0.00'}</div>
      <div class="item-barcode">Código: ${item.barcode || 'N/A'}</div>
    </div>
  `).join('');

  elementos.resultados.innerHTML = `
    ${header}
    <div class="items-grid">
      ${itemsHTML}
    </div>
  `;

  if (!esReset) {
    mostrarExito(`Búsqueda completada: ${items.length} resultado(s)`);
  }
};

// Funciones de búsqueda
async function cargarTodosLosProductos() {
  if (isLoading) return;
  
  mostrarLoading(true);
  limpiarMensajes();
  
  try {
    const response = await fetch(API_BASE);
    
    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    todosLosProductos = Array.isArray(data) ? data : [data];
    mostrarResultados(todosLosProductos, true);
    
  } catch (error) {
    console.error('Error al cargar productos:', error);
    mostrarError("Error al cargar los productos. Verifica que el servidor esté funcionando.");
  } finally {
    mostrarLoading(false);
  }
}

async function buscarPorId() {
  if (isLoading) return;
  
  limpiarMensajes();
  const id = elementos.idInput.value.trim();
  
  if (!id) {
    mostrarError("Por favor, ingresa un ID válido");
    elementos.idInput.focus();
    return;
  }

  mostrarLoading(true);
  
  try {
    const response = await fetch(`${API_BASE}/${encodeURIComponent(id)}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error("Producto no encontrado");
      }
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    mostrarResultados(data);
    
  } catch (error) {
    console.error('Error en búsqueda por ID:', error);
    mostrarError(`No se pudo encontrar el producto con ID "${id}"`);
  } finally {
    mostrarLoading(false);
  }
}

async function buscarPorCodigo() {
  if (isLoading) return;
  
  limpiarMensajes();
  const codigo = elementos.barcodeInput.value.trim();
  
  if (!codigo) {
    mostrarError("Por favor, ingresa un código de barras válido");
    elementos.barcodeInput.focus();
    return;
  }

  mostrarLoading(true);
  
  try {
    const response = await fetch(`${API_BASE}/barcode/${encodeURIComponent(codigo)}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error("Producto no encontrado");
      }
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    mostrarResultados(data);
    
  } catch (error) {
    console.error('Error en búsqueda por código:', error);
    mostrarError(`No se pudo encontrar el producto con código "${codigo}"`);
  } finally {
    mostrarLoading(false);
  }
}

function resetearBusqueda() {
  elementos.idInput.value = '';
  elementos.barcodeInput.value = '';
  limpiarMensajes();
  cargarTodosLosProductos();
}

// Event listeners para Enter
elementos.idInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    buscarPorId();
  }
});

elementos.barcodeInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    buscarPorCodigo();
  }
});

// Cargar productos al iniciar
document.addEventListener('DOMContentLoaded', () => {
  cargarTodosLosProductos();
});