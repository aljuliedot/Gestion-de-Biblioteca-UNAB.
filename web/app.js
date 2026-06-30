// Variables de estado
let activeView = 'catalogo';
let librosCache = []; // Cache local de libros para búsqueda en tiempo real
let isApiReady = false;

// Espera a que PyWebView esté listo
window.addEventListener('pywebviewready', () => {
    isApiReady = true;
    init();
});

// Inicialización de la aplicación
function init() {
    loadCatalog();
    // Iniciar con la vista de catálogo
    switchView('catalogo');
}

// Cambiar de vista en la UI
function switchView(viewId) {
    activeView = viewId;
    
    // Ocultar todas las vistas y remover clases activas de botones
    document.querySelectorAll('.app-view').forEach(view => view.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    
    // Mostrar la vista seleccionada y activar su botón
    const activeSection = document.getElementById(`view-${viewId}`);
    const activeBtn = document.getElementById(`btn-${viewId}`);
    
    if (activeSection) activeSection.classList.remove('active'), activeSection.classList.add('active');
    if (activeBtn) activeBtn.classList.add('active');
    
    // Mostrar u ocultar barra de búsqueda de catálogo
    const searchBox = document.querySelector('.search-box');
    if (viewId === 'catalogo') {
        searchBox.style.opacity = '1';
        searchBox.style.pointerEvents = 'all';
    } else {
        searchBox.style.opacity = '0';
        searchBox.style.pointerEvents = 'none';
    }

    // Cargar datos según la vista activa
    if (viewId === 'catalogo') {
        loadCatalog();
    } else if (viewId === 'historial') {
        // Por defecto, carga todos los préstamos
        document.getElementById('filter-all').classList.add('active');
        document.getElementById('filter-active').classList.remove('active');
        loadHistorial(false);
    }
}

// Cargar catálogo de libros desde Python
function loadCatalog() {
    if (!isApiReady) return;
    
    const catalogList = document.getElementById('catalog-list');
    
    window.pywebview.api.get_libros()
        .then(libros => {
            librosCache = libros;
            renderCatalog(libros);
            updateStats(libros);
        })
        .catch(err => {
            console.error(err);
            catalogList.innerHTML = `
                <div class="empty-state">
                    <i class="fa-solid fa-circle-exclamation" style="color: var(--color-warning);"></i>
                    <p>Error al conectar con el catálogo de libros.</p>
                </div>
            `;
        });
}

// Renderizar libros en el grid
function renderCatalog(libros) {
    const catalogList = document.getElementById('catalog-list');
    catalogList.innerHTML = '';
    
    if (libros.length === 0) {
        catalogList.innerHTML = `
            <div class="empty-state">
                <i class="fa-solid fa-folder-open"></i>
                <p>No hay libros registrados en la biblioteca.</p>
            </div>
        `;
        return;
    }
    
    libros.forEach(libro => {
        const card = document.createElement('div');
        card.className = 'book-card';
        
        const isPrestado = libro.esta_prestado;
        const badgeClass = isPrestado ? 'loaned' : 'available';
        const badgeText = isPrestado ? 'Prestado' : 'Disponible';
        
        // Botón de acción dinámico
        const actionButton = isPrestado 
            ? `<button class="btn btn-danger" onclick="devolverLibro('${escapeString(libro.titulo)}')">
                 <i class="fa-solid fa-arrow-rotate-left"></i> Devolver
               </button>`
            : `<button class="btn btn-primary" onclick="prestarLibro('${escapeString(libro.titulo)}')">
                 <i class="fa-solid fa-book-bookmark"></i> Prestar
               </button>`;
               
        card.innerHTML = `
            <div>
                <h3 class="book-title" title="${libro.titulo}">${libro.titulo}</h3>
                <div class="book-meta">
                    <p>Autor: <span>${libro.autor || 'N/A'}</span></p>
                    <p>Género: <span>${libro.genero || 'N/A'}</span></p>
                    <p>Editorial: <span>${libro.editorial || 'N/A'}</span></p>
                </div>
            </div>
            <div class="book-footer">
                <span class="status-badge ${badgeClass}">${badgeText}</span>
                ${actionButton}
            </div>
        `;
        
        catalogList.appendChild(card);
    });
}

// Actualizar estadísticas del catálogo
function updateStats(libros) {
    const statsLabel = document.getElementById('catalogo-stats');
    const total = libros.length;
    const disponibles = libros.filter(l => !l.esta_prestado).length;
    statsLabel.textContent = `${disponibles} de ${total} libros disponibles actualmente`;
}

// Filtrar catálogo en tiempo real (barra superior)
function filterCatalog() {
    const query = document.getElementById('catalog-search').value.toLowerCase().trim();
    if (!query) {
        renderCatalog(librosCache);
        return;
    }
    
    const filtrados = librosCache.filter(libro => 
        libro.titulo.toLowerCase().includes(query) || 
        libro.autor.toLowerCase().includes(query) ||
        libro.genero.toLowerCase().includes(query)
    );
    
    renderCatalog(filtrados);
}

// Acción de prestar libro
function prestarLibro(titulo) {
    if (!isApiReady) return;
    
    window.pywebview.api.prestar_libro(titulo)
        .then(res => {
            if (res.success) {
                showToast(res.message, 'success');
                loadCatalog();
            } else {
                showToast(res.message, 'error');
            }
        })
        .catch(err => showToast('Error al procesar el préstamo.', 'error'));
}

// Acción de devolver libro
function devolverLibro(titulo) {
    if (!isApiReady) return;
    
    window.pywebview.api.devolver_libro(titulo)
        .then(res => {
            if (res.success) {
                showToast(res.message, 'success');
                loadCatalog();
            } else {
                showToast(res.message, 'error');
            }
        })
        .catch(err => showToast('Error al procesar la devolución.', 'error'));
}

// Enviar formulario de nuevo libro
function submitBook(event) {
    event.preventDefault();
    if (!isApiReady) return;
    
    const titulo = document.getElementById('form-titulo').value.trim();
    const autor = document.getElementById('form-autor').value.trim();
    const genero = document.getElementById('form-genero').value.trim();
    const editorial = document.getElementById('form-editorial').value.trim();
    
    window.pywebview.api.agregar_libro(titulo, autor, genero, editorial)
        .then(res => {
            if (res.success) {
                showToast(res.message, 'success');
                // Limpiar formulario
                document.getElementById('add-book-form').reset();
                // Redirigir al catálogo
                switchView('catalogo');
            } else {
                showToast(res.message, 'error');
            }
        })
        .catch(err => showToast('Error al registrar el libro.', 'error'));
}

// Buscar Recomendación (Estrategias)
function getRecommendation() {
    if (!isApiReady) return;
    
    const criterio = document.getElementById('rec-criterio').value;
    const pref = document.getElementById('rec-pref').value.trim();
    const resultContainer = document.getElementById('recommendation-result');
    
    if (!pref) {
        showToast('Escribe una preferencia antes de buscar.', 'error');
        return;
    }
    
    resultContainer.innerHTML = `
        <div style="text-align: center; color: var(--text-muted); padding: 10px;">
            <i class="fa-solid fa-spinner fa-spin"></i> Analizando biblioteca...
        </div>
    `;
    
    window.pywebview.api.recomendar_libro(criterio, pref)
        .then(res => {
            resultContainer.innerHTML = '';
            if (res.success) {
                const libro = res.libro;
                resultContainer.innerHTML = `
                    <div class="sug-card">
                        <div class="sug-header">
                            <i class="fa-solid fa-star"></i>
                            <span>RECOMENDACIÓN SUGERIDA</span>
                        </div>
                        <h3 class="sug-title">${libro.titulo}</h3>
                        <div class="sug-meta">
                            <p>Autor: <span>${libro.autor || 'N/A'}</span></p>
                            <p>Género: <span>${libro.genero || 'N/A'}</span></p>
                            <p>Editorial: <span>${libro.editorial || 'N/A'}</span></p>
                        </div>
                    </div>
                `;
            } else {
                resultContainer.innerHTML = `
                    <div class="sug-error">
                        <i class="fa-solid fa-circle-xmark"></i>
                        <span>${res.message}</span>
                    </div>
                `;
            }
        })
        .catch(err => {
            resultContainer.innerHTML = `
                <div class="sug-error">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    <span>Error al buscar recomendación.</span>
                </div>
            `;
        });
}

// Cargar historial de préstamos
function loadHistorial(soloActivos) {
    if (!isApiReady) return;
    
    const listContainer = document.getElementById('historial-list');
    listContainer.innerHTML = `
        <div class="loading-state">
            <i class="fa-solid fa-spinner fa-spin"></i>
            <p>Cargando registros...</p>
        </div>
    `;
    
    // Activar estilo de botón de filtro
    if (soloActivos) {
        document.getElementById('filter-active').classList.add('active');
        document.getElementById('filter-all').classList.remove('active');
    } else {
        document.getElementById('filter-all').classList.add('active');
        document.getElementById('filter-active').classList.remove('active');
    }

    window.pywebview.api.get_historial(soloActivos)
        .then(historial => {
            listContainer.innerHTML = '';
            if (historial.length === 0) {
                listContainer.innerHTML = `
                    <div class="empty-state">
                        <i class="fa-solid fa-file-invoice"></i>
                        <p>No hay préstamos para mostrar.</p>
                    </div>
                `;
                return;
            }
            
            historial.forEach(p => {
                const card = document.createElement('div');
                card.className = 'history-card';
                
                const badgeClass = p.esta_vigente ? 'loaned' : 'available';
                const badgeText = p.esta_vigente ? 'En curso' : 'Devuelto';
                
                card.innerHTML = `
                    <div class="history-info">
                        <span class="history-title">${p.libro}</span>
                        <span class="history-sub">Usuario: <span>${p.usuario}</span> | Fecha: <span>${p.fecha}</span></span>
                    </div>
                    <span class="status-badge ${badgeClass}">${badgeText}</span>
                `;
                listContainer.appendChild(card);
            });
        })
        .catch(err => {
            listContainer.innerHTML = `
                <div class="empty-state">
                    <i class="fa-solid fa-triangle-exclamation" style="color: var(--color-warning);"></i>
                    <p>Error al cargar el historial.</p>
                </div>
            `;
        });
}

// Mostrar notificaciones emergentes (toasts)
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icon = type === 'success' ? 'fa-circle-check' : 'fa-circle-exclamation';
    
    toast.innerHTML = `
        <i class="fa-solid ${icon}"></i>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    // Auto-eliminar después de 3.5 segundos
    setTimeout(() => {
        toast.style.animation = 'fadeIn 0.3s ease-out reverse forwards';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3500);
}

// Auxiliar para escapar cadenas de texto en HTML onclick
function escapeString(str) {
    return str.replace(/'/g, "\\'").replace(/"/g, '\\"');
}
