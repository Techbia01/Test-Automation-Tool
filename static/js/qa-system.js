/* ===================================
   SISTEMA QA - JAVASCRIPT MODERNO
   Preparado para migración a TypeScript
   =================================== */

/**
 * Sistema QA - Clase principal
 * @class QASystem
 */
class QASystem {
    constructor() {
        this.config = {
            apiBaseUrl: window.location.origin,
            animationDuration: 300,
            debounceDelay: 300,
            notificationDuration: 5000
        };
        
        this.components = new QAComponents();
        this.api = new QAApi(this.config.apiBaseUrl);
        this.notifications = new QANotifications();
        
        this.init();
    }
    
    /**
     * Inicializar el sistema
     */
    init() {
        this.initializeBootstrap();
        this.setupEventListeners();
        this.initializeAnimations();
        
        console.log('🚀 Sistema QA inicializado correctamente');
    }
    
    /**
     * Inicializar componentes de Bootstrap
     */
    initializeBootstrap() {
        // Tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
        
        // Popovers
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
    }
    
    /**
     * Configurar event listeners globales
     */
    setupEventListeners() {
        // Prevenir envío de formularios vacíos
        document.addEventListener('submit', (e) => {
            const form = e.target;
            if (form.tagName === 'FORM') {
                const requiredFields = form.querySelectorAll('[required]');
                let isValid = true;
                
                requiredFields.forEach(field => {
                    if (!field.value.trim()) {
                        field.classList.add('is-invalid');
                        isValid = false;
                    } else {
                        field.classList.remove('is-invalid');
                    }
                });
                
                if (!isValid) {
                    e.preventDefault();
                    this.notifications.show('Por favor completa todos los campos requeridos', 'warning');
                }
            }
        });
        
        // Auto-hide alerts
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => {
                const alerts = document.querySelectorAll('.alert');
                alerts.forEach(alert => {
                    if (alert.classList.contains('alert-success')) {
                        setTimeout(() => {
                            alert.style.opacity = '0';
                            setTimeout(() => alert.remove(), 300);
                        }, this.config.notificationDuration);
                    }
                });
            }, 1000);
        });
    }
    
    /**
     * Inicializar animaciones
     */
    initializeAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add('animate-slide-up');
                    }, index * 100);
                }
            });
        }, observerOptions);
        
        // Observar elementos para animación
        document.querySelectorAll('.card, .stat-card, .project-card').forEach(el => {
            observer.observe(el);
        });
    }
    
    /**
     * Utilidades generales
     */
    static utils = {
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },
        
        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        },
        
        generateId() {
            return 'qa_' + Math.random().toString(36).substr(2, 9);
        },
        
        copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                window.qaSystem.notifications.show('Copiado al portapapeles', 'success');
            });
        }
    };
}

/**
 * Componentes UI reutilizables
 * @class QAComponents
 */
class QAComponents {
    /**
     * Crear modal dinámico
     */
    createModal(title, content, actions = []) {
        const modalId = QASystem.utils.generateId();
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = modalId;
        modal.setAttribute('tabindex', '-1');
        
        let actionsHTML = '';
        actions.forEach(action => {
            actionsHTML += `
                <button type="button" 
                        class="btn btn-${action.type || 'secondary'} btn-modern" 
                        onclick="${action.onclick || ''}" 
                        ${action.dismiss ? 'data-bs-dismiss="modal"' : ''}>
                    ${action.icon ? `<i class="${action.icon}"></i>` : ''}
                    ${action.text}
                </button>
            `;
        });
        
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-cog"></i>
                            ${title}
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${content}
                    </div>
                    <div class="modal-footer">
                        ${actionsHTML}
                        <button type="button" class="btn btn-outline-modern" data-bs-dismiss="modal">
                            <i class="fas fa-times"></i>
                            Cerrar
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        
        // Limpiar modal cuando se cierre
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
        
        return bsModal;
    }
    
    /**
     * Crear confirmación elegante
     */
    async confirm(message, title = 'Confirmar acción') {
        return new Promise((resolve) => {
            const modal = this.createModal(
                title,
                `<div class="text-center py-3">
                    <i class="fas fa-question-circle fa-3x text-warning mb-3"></i>
                    <p class="mb-0 fs-5">${message}</p>
                </div>`,
                [
                    {
                        text: 'Confirmar',
                        type: 'primary',
                        icon: 'fas fa-check',
                        onclick: `
                            document.getElementById('${modal._element.id}').dispatchEvent(new CustomEvent('confirm'));
                            bootstrap.Modal.getInstance(document.getElementById('${modal._element.id}')).hide();
                        `
                    }
                ]
            );
            
            modal._element.addEventListener('confirm', () => resolve(true));
            modal._element.addEventListener('hidden.bs.modal', () => resolve(false));
            modal.show();
        });
    }
    
    /**
     * Crear loading overlay
     */
    showLoading(message = 'Procesando...') {
        const loadingId = 'loading-overlay';
        let overlay = document.getElementById(loadingId);
        
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = loadingId;
            overlay.className = 'loading-overlay';
            overlay.innerHTML = `
                <div class="loading-spinner">
                    <div class="spinner-modern"></div>
                    <div class="loading-text">${message}</div>
                </div>
            `;
            document.body.appendChild(overlay);
        }
        
        overlay.querySelector('.loading-text').textContent = message;
        overlay.classList.add('show');
        
        return {
            hide: () => {
                overlay.classList.remove('show');
                setTimeout(() => overlay.remove(), 300);
            },
            updateMessage: (newMessage) => {
                overlay.querySelector('.loading-text').textContent = newMessage;
            }
        };
    }
    
    /**
     * Crear progress bar
     */
    createProgressBar(container, progress = 0) {
        const progressBar = document.createElement('div');
        progressBar.className = 'progress mb-3';
        progressBar.style.height = '12px';
        progressBar.style.borderRadius = '6px';
        progressBar.style.background = 'var(--bg-tertiary)';
        
        progressBar.innerHTML = `
            <div class="progress-bar progress-bar-striped progress-bar-animated" 
                 role="progressbar" 
                 style="width: ${progress}%; background: var(--gradient-primary);"
                 aria-valuenow="${progress}" 
                 aria-valuemin="0" 
                 aria-valuemax="100">
            </div>
        `;
        
        if (container) {
            container.appendChild(progressBar);
        }
        
        return {
            element: progressBar,
            update: (newProgress) => {
                const bar = progressBar.querySelector('.progress-bar');
                bar.style.width = newProgress + '%';
                bar.setAttribute('aria-valuenow', newProgress);
            }
        };
    }
}

/**
 * API Client
 * @class QAApi
 */
class QAApi {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }
    
    /**
     * Realizar petición HTTP
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            // Si es descarga de archivo
            if (response.headers.get('content-type')?.includes('text/csv')) {
                return response.blob();
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
    
    /**
     * Crear proyecto
     */
    async createProject(projectData) {
        return this.request('/create_project', {
            method: 'POST',
            body: JSON.stringify(projectData)
        });
    }
    
    /**
     * Generar casos de prueba
     */
    async generateTestCases(projectId) {
        return this.request('/generate_test_cases', {
            method: 'POST',
            body: JSON.stringify({ project_id: projectId })
        });
    }
    
    /**
     * Exportar a Linear
     */
    async exportToLinear(projectId, type = 'simple', parentId = null) {
        let endpoint = `/export_linear_${type}/${projectId}`;
        if (parentId && type === 'subissues') {
            endpoint += `?parent_id=${encodeURIComponent(parentId)}`;
        }
        
        return this.request(endpoint);
    }
}

/**
 * Sistema de notificaciones
 * @class QANotifications
 */
class QANotifications {
    constructor() {
        this.container = this.createContainer();
    }
    
    createContainer() {
        let container = document.getElementById('notifications-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'notifications-container';
            container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                max-width: 400px;
            `;
            document.body.appendChild(container);
        }
        return container;
    }
    
    show(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        const id = QASystem.utils.generateId();
        notification.id = id;
        
        const icons = {
            'success': 'fa-check-circle',
            'danger': 'fa-exclamation-triangle',
            'warning': 'fa-exclamation-circle',
            'info': 'fa-info-circle'
        };
        
        notification.className = `alert alert-${type} alert-dismissible fade show animate-slide-right mb-3`;
        notification.style.cssText = `
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            border: none;
            border-radius: 12px;
        `;
        
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas ${icons[type]} me-3 fs-5"></i>
                <div class="flex-grow-1">${message}</div>
                <button type="button" class="btn-close btn-close-white ms-3" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        this.container.appendChild(notification);
        
        // Auto-remove
        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.opacity = '0';
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => notification.remove(), 300);
            }
        }, duration);
        
        return id;
    }
}

/**
 * Funciones específicas del proyecto
 * @class QAProject
 */
class QAProject {
    constructor(qaSystem) {
        this.qaSystem = qaSystem;
    }
    
    /**
     * Crear proyecto con validación
     */
    async create(formData) {
        const loading = this.qaSystem.components.showLoading('Creando proyecto...');
        
        try {
            const result = await this.qaSystem.api.createProject(formData);
            
            this.qaSystem.notifications.show(
                'Proyecto creado exitosamente', 
                'success'
            );
            
            return result;
        } catch (error) {
            this.qaSystem.notifications.show(
                'Error: ' + error.message, 
                'danger'
            );
            throw error;
        } finally {
            loading.hide();
        }
    }
    
    /**
     * Generar casos de prueba
     */
    async generateTestCases(projectId, button) {
        const originalText = button.innerHTML;
        button.disabled = true;
        button.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2"></span>
            Generando...
        `;
        
        try {
            const result = await this.qaSystem.api.generateTestCases(projectId);
            
            this.qaSystem.notifications.show(
                `${result.test_cases_count} casos de prueba generados exitosamente`, 
                'success'
            );
            
            // Recargar después de un momento
            setTimeout(() => {
                window.location.reload();
            }, 1500);
            
            return result;
        } catch (error) {
            this.qaSystem.notifications.show(
                'Error: ' + error.message, 
                'danger'
            );
            throw error;
        } finally {
            button.disabled = false;
            button.innerHTML = originalText;
        }
    }
    
    /**
     * Exportar a Linear
     */
    async exportToLinear(projectId, type = 'simple', parentId = null) {
        const loading = this.qaSystem.components.showLoading('Exportando a Linear...');
        
        try {
            const blob = await this.qaSystem.api.exportToLinear(projectId, type, parentId);
            
            // Descargar archivo
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = `linear_export_${type}_${projectId}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(downloadUrl);
            
            this.qaSystem.notifications.show(
                'Exportación completada exitosamente', 
                'success'
            );
        } catch (error) {
            this.qaSystem.notifications.show(
                'Error: ' + error.message, 
                'danger'
            );
            throw error;
        } finally {
            loading.hide();
        }
    }
}

// Inicializar sistema global
let qaSystem;
document.addEventListener('DOMContentLoaded', () => {
    qaSystem = new QASystem();
    qaSystem.project = new QAProject(qaSystem);
    
    // Hacer disponible globalmente
    window.qaSystem = qaSystem;
});

// Funciones globales para compatibilidad con templates existentes
async function generateTestCases(projectId) {
    const button = event.target;
    await window.qaSystem.project.generateTestCases(projectId, button);
}

async function exportLinearSimple(projectId) {
    await window.qaSystem.project.exportToLinear(projectId, 'simple');
}

async function exportAsSubissues(projectId) {
    const parentId = prompt('Ingresa el ID del Issue padre en Linear (ej: TEST-123):');
    if (parentId && parentId.trim()) {
        await window.qaSystem.project.exportToLinear(projectId, 'subissues', parentId.trim());
    }
}

function loadTemplates() {
    const templates = [
        {
            name: 'Historia de Usuario Web',
            description: 'Plantilla para funcionalidades web estándar',
            icon: 'fas fa-globe',
            color: 'var(--bia-primary)'
        },
        {
            name: 'API REST',
            description: 'Plantilla para endpoints de API',
            icon: 'fas fa-code',
            color: 'var(--bia-secondary)'
        },
        {
            name: 'Proceso de Negocio',
            description: 'Plantilla para flujos de trabajo complejos',
            icon: 'fas fa-sitemap',
            color: 'var(--bia-warning)'
        },
        {
            name: 'Integración Externa',
            description: 'Plantilla para integraciones con sistemas externos',
            icon: 'fas fa-plug',
            color: 'var(--bia-info)'
        }
    ];
    
    let content = '<div class="row g-3">';
    templates.forEach(template => {
        content += `
            <div class="col-md-6">
                <div class="card h-100 template-card" style="cursor: pointer;" onclick="useTemplate('${template.name}')">
                    <div class="card-body text-center p-4">
                        <div class="template-icon mb-3" style="color: ${template.color};">
                            <i class="${template.icon} fa-3x"></i>
                        </div>
                        <h6 class="card-title fw-bold">${template.name}</h6>
                        <p class="card-text text-muted small">${template.description}</p>
                        <button class="btn btn-outline-modern btn-sm">
                            <i class="fas fa-plus me-2"></i>
                            Usar Plantilla
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    content += '</div>';
    
    window.qaSystem.components.createModal(
        'Plantillas Disponibles',
        content
    ).show();
}

function useTemplate(templateName) {
    window.qaSystem.notifications.show(
        `Plantilla "${templateName}" seleccionada. Redirigiendo...`,
        'info'
    );
    
    setTimeout(() => {
        window.location.href = '/new_project?template=' + encodeURIComponent(templateName);
    }, 1000);
}
