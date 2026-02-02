const form = document.getElementById('input-form');
const userInput = document.getElementById('user-input');
const responseArea = document.getElementById('response-area');
const aiText = document.getElementById('ai-text');
const moodBadge = document.getElementById('mood-badge');
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
    "danger": 0       // Red (Alarm)
};

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = userInput.value.trim();
    if (!text) return;

    // UI Loading State
    setLoading(true);

    try {
        const response = await fetch('http://localhost:5000/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        if (data.status === 'success') {
            displayResult(data.data);
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
        btnText.textContent = 'Analyzing...';
        btnLoader.classList.remove('hidden');
        responseArea.classList.add('hidden');
    } else {
        submitBtn.disabled = false;
        btnText.textContent = 'Share';
        btnLoader.classList.add('hidden');
    }
}

function displayResult(data) {
    const { emotion, response_text } = data;

    // 1. Update Text
    aiText.innerHTML = response_text; // Use innerHTML for <strong> tags
    moodBadge.textContent = emotion.charAt(0).toUpperCase() + emotion.slice(1);

    // 2. Show Response Area
    responseArea.classList.remove('hidden');

    // 3. Update Theme Colors
    const hue = emotionHues[emotion] || 220;
    document.body.setAttribute('data-mood', emotion);
    console.log("Detected Emotion:", emotion, "Set Hue:", hue);
    updateTheme(hue);

    // 4. Clear input
    userInput.value = '';
}

function updateTheme(hue) {
    // Smoothly transition CSS variable
    root.style.setProperty('--accent-hue', hue);
}
