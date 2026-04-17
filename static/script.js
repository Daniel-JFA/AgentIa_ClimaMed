/**
 * Script para la interfaz web del Agente de Clima
 */

// Variables globales
let chatHistory = [];
const STORAGE_KEY = 'weather_agent_chat_history';

// Elementos DOM
const chatBox = document.getElementById('chatBox');
const questionInput = document.getElementById('questionInput');
const questionForm = document.getElementById('questionForm');
const sendBtn = document.getElementById('sendBtn');
const quickExamples = document.getElementById('quickExamples');
const zonesList = document.getElementById('zonesList');

/**
 * Inicializar la aplicación
 */
document.addEventListener('DOMContentLoaded', function() {
    loadChatHistory();
    loadExamples();
    loadZones();
    questionInput.focus();
});

/**
 * Cargar ejemplos de preguntas
 */
async function loadExamples() {
    try {
        const response = await fetch('/api/examples');
        const data = await response.json();
        
        if (data.success) {
            quickExamples.innerHTML = data.examples
                .map(example => `<button type="button" class="example-btn" onclick="useExample('${example}')">${example}</button>`)
                .join('');
        }
    } catch (error) {
        console.error('Error loading examples:', error);
    }
}

/**
 * Cargar zonas soportadas
 */
async function loadZones() {
    try {
        const response = await fetch('/api/zones');
        const data = await response.json();
        
        if (data.success) {
            zonesList.innerHTML = data.zones
                .map(zone => `<div class="zone-item" onclick="useZone('${zone}')">${zone}</div>`)
                .join('');
        }
    } catch (error) {
        console.error('Error loading zones:', error);
    }
}

/**
 * Usar un ejemplo
 */
function useExample(example) {
    questionInput.value = example;
    questionInput.focus();
}

/**
 * Usar una zona
 */
function useZone(zone) {
    questionInput.value = 'clima en ' + zone.toLowerCase();
    questionInput.focus();
}

/**
 * Enviar pregunta
 */
async function sendQuestion(event) {
    event.preventDefault();
    
    const question = questionInput.value.trim();
    
    if (!question) {
        return;
    }
    
    // Limpiar input
    questionInput.value = '';
    
    // Agregar mensaje del usuario al chat
    addMessage('user', question);
    
    // Mostrar loading
    const loadingId = showLoading();
    
    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: question })
        });
        
        const data = await response.json();
        
        // Remover loading
        removeLoading(loadingId);
        
        if (data.success) {
            addMessage('agent', data.response, data.timestamp);
            saveChatHistory('user', question);
            saveChatHistory('agent', data.response);
        } else {
            addMessage('agent', `❌ Error: ${data.error}`);
        }
    } catch (error) {
        removeLoading(loadingId);
        addMessage('agent', `❌ Error de conexión: ${error.message}`);
        console.error('Error:', error);
    }
    
    // Enfocar input
    questionInput.focus();
}

/**
 * Agregar mensaje al chat
 */
function addMessage(sender, text, timestamp = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const timeStr = timestamp ? `<div class="message-time">${timestamp}</div>` : '';
    
    messageDiv.innerHTML = `
        <div class="message-content">
            ${formatText(text)}
            ${timeStr}
        </div>
    `;
    
    chatBox.appendChild(messageDiv);
    
    // Scroll al final
    chatBox.scrollTop = chatBox.scrollHeight;
}

/**
 * Formatear texto (permitir saltos de línea)
 */
function formatText(text) {
    return text
        .split('\n')
        .map(line => escapeHtml(line))
        .join('<br>');
}

/**
 * Escapar HTML
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Mostrar indicador de carga
 */
function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message agent';
    loadingDiv.id = 'loading-' + Date.now();
    loadingDiv.innerHTML = `
        <div class="message-content">
            <div class="loading">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            </div>
        </div>
    `;
    
    chatBox.appendChild(loadingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    
    return loadingDiv.id;
}

/**
 * Remover indicador de carga
 */
function removeLoading(loadingId) {
    const loadingElement = document.getElementById(loadingId);
    if (loadingElement) {
        loadingElement.remove();
    }
}

/**
 * Limpiar chat
 */
function clearChat() {
    if (confirm('¿Estás seguro de que deseas limpiar el historial?')) {
        chatBox.innerHTML = `
            <div class="welcome-message">
                <h2>Bienvenido 👋</h2>
                <p>Soy un agente de IA que te ayuda con información del clima en Medellín.</p>
                <p><strong>Ejemplos de preguntas:</strong></p>
                <div class="quick-examples" id="quickExamples"></div>
            </div>
        `;
        chatHistory = [];
        localStorage.removeItem(STORAGE_KEY);
        loadExamples();
    }
}

/**
 * Guardar historial de chat
 */
function saveChatHistory(sender, message) {
    chatHistory.push({
        sender: sender,
        message: message,
        timestamp: new Date().toISOString()
    });
    
    localStorage.setItem(STORAGE_KEY, JSON.stringify(chatHistory));
}

/**
 * Cargar historial de chat
 */
function loadChatHistory() {
    const stored = localStorage.getItem(STORAGE_KEY);
    
    if (stored) {
        try {
            chatHistory = JSON.parse(stored);
            
            // Restaurar mensajes (máximo 20 últimos)
            const recentMessages = chatHistory.slice(-20);
            
            if (recentMessages.length > 0) {
                // Limpiar welcome message
                chatBox.innerHTML = '';
                
                // Restaurar mensajes
                recentMessages.forEach(msg => {
                    addMessage(msg.sender, msg.message);
                });
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
            localStorage.removeItem(STORAGE_KEY);
        }
    }
}

/**
 * Permitir enviar con Enter
 */
questionInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendQuestion(questionForm);
    }
});

// Health check al cargar
document.addEventListener('DOMContentLoaded', async function() {
    try {
        await fetch('/health');
    } catch (error) {
        console.warn('Server health check failed:', error);
    }
});
