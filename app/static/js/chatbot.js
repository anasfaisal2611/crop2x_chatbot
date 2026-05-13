// Chatbot Configuration
const CHATBOT_CONFIG = {
    apiBaseUrl: 'http://localhost:5000/api',
    userId: null,
    deviceId: null
};

// 1. App Initialization
document.addEventListener('DOMContentLoaded', function() {
    generateDeviceId();
    initializeChatbot();
    setupMinimizeListener();
});

// 2. Generate/Get Unique Device ID
function generateDeviceId() {
    let deviceId = localStorage.getItem('crop2x_device_id');
    if (!deviceId) {
        deviceId = 'device_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('crop2x_device_id', deviceId);
    }
    CHATBOT_CONFIG.deviceId = deviceId;
}

async function showKnowledgeStatus() {
    try {
        const res = await fetch(`${CHATBOT_CONFIG.apiBaseUrl}/chatbot/knowledge-status`);
        const kb = await res.json();
        if (!kb.success) return;
        if (kb.ready) {
            return;
        }
        const key = 'crop2x_kb_missing_shown';
        if (sessionStorage.getItem(key) === '1') return;
        sessionStorage.setItem(key, '1');
        let msg = 'Note: No active knowledge document was found (or text could not be read from the PDF). You can still say hello or ask general questions about Crop2X.';
        if (kb.hint) msg += ' ' + kb.hint;
        appendMessage('bot', msg);
    } catch (e) {
        /* ignore */
    }
}

// 3. Initialize Chat Session
async function initializeChatbot() {
    try {
        const res = await fetch(`${CHATBOT_CONFIG.apiBaseUrl}/chatbot/init`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ device_id: CHATBOT_CONFIG.deviceId })
        });
        const data = await res.json();
        if (data.success) {
            CHATBOT_CONFIG.userId = data.user_id;
            await showKnowledgeStatus();
        }
    } catch (err) {
        console.error("Initialization failed:", err);
    }
}

// --- Note: PDF Upload Logic removed from here because Admin handles it now ---

// 4. Messaging Logic
// ... (Initial Config and Init functions same rahenge)

// messaging Logic ko isse replace karein
async function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    if (!message || !CHATBOT_CONFIG.userId) return;

    appendMessage('user', message);
    input.value = '';

    try {
        const res = await fetch(`${CHATBOT_CONFIG.apiBaseUrl}/chatbot/message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                user_id: CHATBOT_CONFIG.userId, 
                message: message 
            })
        });
        const data = await res.json();
        
        if (data.response) {
            appendMessage('bot', data.response);
        } else if (data.success === false && data.error) {
            appendMessage('bot', "Server error: " + data.error);
        } else {
            appendMessage('bot', "No response received. Please try again or check that the server is running.");
        }
    } catch (err) {
        appendMessage('bot', "Connection error. Please check your network and that the server is running.");
    }
}
// ... (appendMessage and other functions same rahenge)
function appendMessage(sender, text) {
    const container = document.getElementById('messages-container');
    if (container) {
        container.innerHTML += `<div class="message ${sender}-message"><p>${text}</p></div>`;
        container.scrollTop = container.scrollHeight;
    }
}

// 5. UI Utilities
function connectWhatsApp() {
    window.open("https://wa.me/923182560704", "_blank");
}

function setupMinimizeListener() {
    const btn = document.getElementById('minimize-btn');
    const container = document.getElementById('chatbot-container');
    if (btn && container) {
        btn.addEventListener('click', () => {
            container.classList.toggle('minimized');
            btn.textContent = container.classList.contains('minimized') ? '+' : '−';
        });
    }
}

function handleKeyPress(e) { 
    if (e.key === 'Enter') sendMessage(); 
}