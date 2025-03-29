document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generate-btn');
    const promptInput = document.getElementById('prompt');
    const resultDiv = document.getElementById('result');

    generateBtn.addEventListener('click', async function() {
        const prompt = promptInput.value.trim();
        if (prompt === '') {
            alert('Please enter a prompt');
            return;
        }

        // Show loading indicator
        resultDiv.innerHTML = 'Generating...';
        generateBtn.disabled = true;

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: prompt,
                    max_length: 100,
                    temperature: 0.7
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            resultDiv.innerHTML = data.generated_text;
        } catch (error) {
            resultDiv.innerHTML = `Error: ${error.message}`;
        } finally {
            generateBtn.disabled = false;
        }
    });
});
