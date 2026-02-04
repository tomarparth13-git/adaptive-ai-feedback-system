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

// Voice Settings
let voiceEnabled = true;
const voiceToggleBtn = document.getElementById('voice-toggle');
const voiceStatus = document.querySelector('.voice-status');

// Speech Synthesis
const synth = window.speechSynthesis;
let currentUtterance = null;

// Voice parameters based on emotion
const emotionVoiceSettings = {
    "anxious": { pitch: 1.1, rate: 0.9 },
    "stressed": { pitch: 1.0, rate: 1.1 },
    "anger": { pitch: 0.9, rate: 1.2 },
    "sad": { pitch: 0.8, rate: 0.8 },
    "positive": { pitch: 1.2, rate: 1.1 },
    "neutral": { pitch: 1.0, rate: 1.0 },
    "danger": { pitch: 0.9, rate: 0.85 },
    "inspired": { pitch: 1.15, rate: 1.05 }
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

    // 3. Speak the response with emotion-based voice
    speak(response_text, emotion);
}

function updateTheme(hue) {
    // Smoothly transition CSS variable
    root.style.setProperty('--accent-hue', hue);
}

// Voice Toggle
voiceToggleBtn.addEventListener('click', () => {
    voiceEnabled = !voiceEnabled;
    voiceToggleBtn.classList.toggle('active', voiceEnabled);
    voiceStatus.textContent = voiceEnabled ? 'Voice: ON' : 'Voice: OFF';

    // Stop any ongoing speech
    if (!voiceEnabled && synth.speaking) {
        synth.cancel();
    }
});

// Initialize voice toggle as active
voiceToggleBtn.classList.add('active');

// Text-to-Speech Function
function speak(text, emotion = 'neutral') {
    // Stop any ongoing speech
    if (synth.speaking) {
        synth.cancel();
    }

    if (!voiceEnabled) return;

    // Remove HTML tags and markdown formatting for clean speech
    const cleanText = text
        .replace(/<[^>]*>/g, '') // Remove HTML tags
        .replace(/\*\*/g, '')     // Remove bold markdown
        .replace(/\*/g, '');      // Remove italic markdown

    const utterance = new SpeechSynthesisUtterance(cleanText);

    // Apply emotion-based voice settings
    const voiceSettings = emotionVoiceSettings[emotion] || emotionVoiceSettings['neutral'];
    utterance.pitch = voiceSettings.pitch;
    utterance.rate = voiceSettings.rate;
    utterance.volume = 0.9;

    // Try to use a more natural voice if available
    const voices = synth.getVoices();
    const preferredVoice = voices.find(voice =>
        voice.name.includes('Google') ||
        voice.name.includes('Microsoft') ||
        voice.lang.startsWith('en')
    );

    if (preferredVoice) {
        utterance.voice = preferredVoice;
    }

    currentUtterance = utterance;
    synth.speak(utterance);
}


// Load voices (some browsers need this)
if (synth.onvoiceschanged !== undefined) {
    synth.onvoiceschanged = () => {
        synth.getVoices();
    };
}
