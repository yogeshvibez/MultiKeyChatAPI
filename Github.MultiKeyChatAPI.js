// server.js
import express from "express";
import ModelClient, { isUnexpected } from "@azure-rest/ai-inference";
import { AzureKeyCredential } from "@azure/core-auth";

const app = express();
app.use(express.json());

const ENDPOINT = "https://models.github.ai/inference";
const MODEL = "openai/gpt-4.1";

const API_KEYS = [
    "ghp_HOUESqrdhyxTlPFFkHaOwLfJ50SlRz0sey46",
    "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"
];

async function sendMessage(messages) {
  for (const key of API_KEYS) {
    try {
      const client = ModelClient(
        ENDPOINT,
        new AzureKeyCredential(key)
      );

      const response = await client.path("/chat/completions").post({
        body: {
          model: MODEL,
          messages: messages,
          temperature: 1,
          top_p: 1
        }
      });

      if (!isUnexpected(response)) {
        return response.body;
      } else {
        console.error(`[!] Failed with key ${key.slice(0, 8)}:`, response.body.error);
      }
    } catch (err) {
      console.error(`[x] Error with key ${key.slice(0, 8)}:`, err.message);
    }
  }

  return { error: "All API calls failed." };
}

app.post("/chat", async (req, res) => {
  const { messages } = req.body;

  if (!messages) {
    return res.status(400).json({ error: "Missing 'messages' in request body." });
  }

  const result = await sendMessage(messages);
  res.json(result);
});

app.listen(5000, () => {
  console.log("[*] Server running at http://localhost:5000");
});
