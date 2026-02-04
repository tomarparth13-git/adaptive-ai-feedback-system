const form = document.getElementById('input-form');
const userInput = document.getElementById('user-input');
const chatHistory = document.getElementById('chat-history');
const submitBtn = document.getElementById('submit-btn');
const btnText = document.querySelector('.btn-text');
const btnLoader = document.querySelector('.btn-loader');
const root = document.documentElement;

// Hue mapping for emotions
const emotionHues = {
    "anxious": 270,   // Purple
    "stressed": 20,   // Orange
    "anger": 0,       // Red
    "sad": 210,       // Blue
    "positive": 140,  // Green
    "neutral": 220,   // Slate Blue
    "danger": 0,      // Red (Alarm)
    "inspired": 45    // Gold/Yellow
};

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = userInput.value.trim();
    if (!text) return;

    // 1. Add User Message to UI
    appendMessage('user', text);
    userInput.value = '';

    // 2. UI Loading State
    setLoading(true);

    try {
        const response = await fetch('http://localhost:5000/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        if (data.status === 'success') {
            displayAIResponse(data.data);
        } else {
            alert('Something went wrong. Please try again.');
        }

    } catch (error) {
        console.error('Error:', error);
        alert('Could not connect to the AI server. Is the backend running?');
    } finally {
        setLoading(false);
    }
});

function setLoading(isLoading) {
    if (isLoading) {
        submitBtn.disabled = true;
        btnText.textContent = 'Reflecting...';
        btnLoader.classList.remove('hidden');
    } else {
        submitBtn.disabled = false;
        btnText.textContent = 'Share';
        btnLoader.classList.add('hidden');
    }
}

function appendMessage(role, text, emotion = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;

    let contentHtml = '';
    if (role === 'ai') {
        contentHtml = `
            <div class="ai-avatar">AI</div>
            <div class="message-content">
                ${emotion ? `<div class="mood-badge-container"><span class="mood-badge">${emotion}</span></div>` : ''}
                <p>${text}</p>
            </div>
        `;
    } else {
        contentHtml = `
            <div class="message-content">
                <p>${text}</p>
            </div>
        `;
    }

    messageDiv.innerHTML = contentHtml;
    chatHistory.appendChild(messageDiv);

    // Smooth scroll to bottom
    chatHistory.scrollTo({
        top: chatHistory.scrollHeight,
        behavior: 'smooth'
    });
}

function displayAIResponse(data) {
    const { emotion, response_text } = data;

    // 1. Append AI Message
    appendMessage('ai', response_text, emotion.charAt(0).toUpperCase() + emotion.slice(1));

    // 2. Update Theme Colors
    const hue = emotionHues[emotion] || 220;
    document.body.setAttribute('data-mood', emotion);
    updateTheme(hue);
}

function updateTheme(hue) {
    // Smoothly transition CSS variable
    root.style.setProperty('--accent-hue', hue);
}
