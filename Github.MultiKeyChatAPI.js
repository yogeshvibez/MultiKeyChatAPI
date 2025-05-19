// Install dependencies: npm install express axios
const express = require('express');
const axios = require('axios');
const app = express();

// Middleware to parse JSON
app.use(express.json());

const BASE_URL = "https://models.github.ai/inference/chat/completions";
const API_KEYS = [
    "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",  // Primary
    "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"   // Fallback
];

async function callApi(messages) {
    const payload = {
        model: "openai/gpt-4.1",
        messages: messages,
        temperature: 1,
        top_p: 1
    };

    for (const key of API_KEYS) {
        try {
            const headers = {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${key}`
            };

            console.log(`[*] Trying with key ${key.substring(0,8)}...`);
            
            const response = await axios.post(BASE_URL, payload, {
                headers: headers,
                timeout: 15000
            });

            console.log(`[*] Success with key ${key.substring(0,8)} - Status: ${response.status}`);
            return response.data;

        } catch (error) {
            if (error.response) {
                console.log(`[!] Failed with key ${key.substring(0,8)}: ${error.response.status} - ${error.response.data}`);
            } else {
                console.log(`[x] Error with key ${key.substring(0,8)}: ${error.message}`);
            }
        }
    }

    return { error: "All API calls failed." };
}

app.post('/chat', async (req, res) => {
    const messages = req.body.messages;
    
    if (!messages) {
        return res.status(400).json({ error: "Missing 'messages'" });
    }

    try {
        const result = await callApi(messages);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: "Internal server error" });
    }
});

app.listen(5000, '127.0.0.1', () => {
    console.log('Server running at http://127.0.0.1:5000');
});
