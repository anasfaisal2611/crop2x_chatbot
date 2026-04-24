// Chatbot Configuration
const CHATBOT_CONFIG = {
    apiBaseUrl: 'http://localhost:5000/api',
    userId: null,
    userType: null,
    deviceId: null
};

// Initialize chatbot on page load
document.addEventListener('DOMContentLoaded', function() {
    generateDeviceId();
    initializeChatbot();
});

// Generate unique device ID
function generateDeviceId() {
    let deviceId = localStorage.getItem('crop2x_device_id');
    if (!deviceId) {
        deviceId = 'device_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('crop2x_device_id', deviceId);
    }
    CHATBOT_CONFIG.deviceId = deviceId;
}

// Initialize chatbot
async function initializeChatbot() {
    try {
        const response = await fetch(`${CHATBOT_CONFIG.apiBaseUrl}/chatbot/init`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                device_id: CHATBOT_CONFIG.deviceId
            })
        });
        
        const data = await response.json();
        if (data.success) {
            CHATBOT_CONFIG.userId = data.user_id;
            CHATBOT_CONFIG.userType = data.user_type;
        }
    } catch (error) {
        console.error('Error initializing chatbot:', error);
    }
}

// Select user type
async function selectUserType(userType) {
    CHATBOT_CONFIG.userType = userType;
    
    try {
        const response = await fetch(`${CHATBOT_CONFIG.apiBaseUrl}/chatbot/init`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_type: userType,
                device_id: CHATBOT_CONFIG.deviceId
            })
        });
        
        const data = await response.json();
        if (data.success) {
            CHATBOT_CONFIG.userId = data.user_id;
        }
    } catch (error) {
        console.error('Error setting user type:', error);
    }
    
    // Send default message based on user type
    const messages = {
        farmer: "I'm a farmer looking to optimize my farming with AI.",
        partner: "I'm interested in partnering with Crop2X.",
        enterprise: "We're an enterprise looking for custom solutions."
    };
    
    sendMessage(messages[userType]);
}

// Send message
async function sendMessage(message = null) {
    if (!message) {
        const input = document.getElementById('message-input');
        message = input.value.trim();
        if (!message) return;
        input.value = '';
    }
    
    // Add user message to display
    addMessageToDisplay(message, 'user');
    
    try {
        const response = await fetch(`${CHATBOT_CONFIG.apiBaseUrl}/chatbot/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: CHATBOT_CONFIG.userId,
                message: message
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessageToDisplay(data.response, 'bot');
            
            // Handle CTA (Call-To-Action)
            if (data.cta) {
                handleCTA(data.cta, data.next_action);
            }
        } else {
            addMessageToDisplay('Sorry, I encountered an error. Please try again.', 'bot');
        }
    } catch (error) {
        console.error('Error sending message:', error);
        addMessageToDisplay('Connection error. Please check your internet connection.', 'bot');
    }
}

// Handle Call-To-Action
function handleCTA(cta, nextAction) {
    setTimeout(() => {
        if (cta === 'whatsapp') {
            showWhatsAppCTA(nextAction);
        } else if (cta === 'lead_form') {
            showLeadForm();
        } else if (cta === 'form') {
            showLeadForm();
        }
    }, 500);
}

// Show WhatsApp CTA
function showWhatsAppCTA(message) {
    const container = document.getElementById('messages-container');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${message}</p>
            <button class="quick-reply" onclick="openWhatsApp()">
                💬 Connect on WhatsApp
            </button>
        </div>
    `;
    container.appendChild(messageDiv);
    scrollToBottom();
}

// Open WhatsApp
function openWhatsApp() {
    // This would normally initiate WhatsApp contact
    // For demo, we show a lead form instead
    showLeadForm();
}

// Show lead form
function showLeadForm() {
    document.getElementById('lead-form-modal').style.display = 'block';
}

// Close lead form
function closeLeadForm() {
    document.getElementById('lead-form-modal').style.display = 'none';
}

// Submit lead form
async function submitLeadForm(event) {
    event.preventDefault();
    
    const leadData = {
        user_id: CHATBOT_CONFIG.userId,
        name: document.getElementById('lead-name').value,
        email: document.getElementById('lead-email').value,
        phone: document.getElementById('lead-phone').value,
        location: document.getElementById('lead-location').value,
        farm_size: document.getElementById('lead-farm-size').value,
        message: document.getElementById('lead-message').value,
        lead_type: 'demo_request',
        send_whatsapp: true
    };
    
    try {
        const response = await fetch(`${CHATBOT_CONFIG.apiBaseUrl}/leads/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(leadData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessageToDisplay(
                '✅ Thank you! Your details have been submitted. Our team will contact you soon via WhatsApp!',
                'bot'
            );
            closeLeadForm();
            document.getElementById('lead-form').reset();
        } else {
            alert('Error submitting form: ' + data.error);
        }
    } catch (error) {
        console.error('Error submitting form:', error);
        alert('Error submitting form. Please try again.');
    }
}

// Add message to display
function addMessageToDisplay(message, sender) {
    const container = document.getElementById('messages-container');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerHTML = message; // Use innerHTML to support formatted responses
    
    messageDiv.appendChild(content);
    container.appendChild(messageDiv);
    
    // Scroll to bottom with a slight delay to ensure DOM is fully rendered
    setTimeout(() => {
        scrollToBottom();
    }, 50);
}

// Scroll to bottom of messages
function scrollToBottom() {
    const container = document.getElementById('messages-container');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}

// Handle key press in input
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Minimize/Maximize
document.addEventListener('DOMContentLoaded', function() {
    const minimizeBtn = document.getElementById('minimize-btn');
    if (minimizeBtn) {
        minimizeBtn.addEventListener('click', function() {
            const container = document.getElementById('chatbot-container');
            const body = document.getElementById('chatbot-body');
            const footer = document.querySelector('.chatbot-footer');
            
            if (container.classList.contains('minimized')) {
                container.classList.remove('minimized');
                body.style.display = 'flex';
                footer.style.display = 'block';
                minimizeBtn.textContent = '−';
            } else {
                container.classList.add('minimized');
                body.style.display = 'none';
                footer.style.display = 'none';
                minimizeBtn.textContent = '+';
            }
        });
    }
});

// Close modal when clicking outside
window.addEventListener('click', function(event) {
    const modal = document.getElementById('lead-form-modal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});
