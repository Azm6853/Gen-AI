# 💬 Sentio: Emotionally Intelligent AI Therapist

**Sentio** is an AI-powered emotional support agent designed to understand human emotions **through text-based tone and response patterns**. It offers conversational support for individuals experiencing loneliness, sadness, anxiety, or emotional overwhelm — using nuanced tone detection, empathetic dialogue, and adaptive responses based on user interaction style.

> “Sentio” means *“I feel”* in Latin — because real support begins with understanding.

---

## 🧠 Project Goal

To build a therapeutic AI companion that:
- Detects emotional tone from typing behavior and linguistic patterns
- Adapts its replies in real-time using empathy-driven prompts
- Tracks emotional state trends while preserving user privacy
- Offers coping tools like journaling prompts, breathing guides, and validation

---

## 🎯 Key Features

- **Tone-Aware Chat**: Understands emotions like sadness, anger, sarcasm, or fear through text cues (e.g., fragmented replies, lowercase typing, ellipses).
- **Empathetic Response Engine**: Adapts tone and language to match the user’s emotional state.
- **Emotional Drift Memory**: Tracks how the user’s emotional tone shifts over time — with optional long-term memory for continuity.
- **Safe-Mode Interventions**: Gently detects signs of emotional distress and offers escalation (e.g., “Would you like help connecting with a human?”).
- **No-Therapist Masking**: Clearly communicates that Sentio is a supportive AI, not a licensed mental health provider.

---

## 🧱 Tech Stack

| Component                | Tool/Framework                            |
|-------------------------|--------------------------------------------|
| Language Model           | GPT-4o / Open-source LLMs (Mistral, LLaMA) |
| Emotion Detection        | Fine-tuned RoBERTa (GoEmotions), Lexical Heuristics |
| Backend Framework        | FastAPI / Flask                           |
| Frontend (Prototype)     | Streamlit / Gradio                        |
| Memory Store             | ChromaDB / FAISS                          |
| Deployment               | Docker (Optional GPU for inference)       |

---

## 🔒 Ethics & Safety

- **Disclaimer:** Sentio is not a substitute for professional therapy.
- **Memory Control:** Users can view, reset, or delete their chat history and emotion logs.
- **Escalation Readiness:** Uses soft keyword and tone triggers to detect emotional danger and suggest real-world help lines (non-invasive).

---

## 🧪 Example Interaction

```plaintext
User: i dunno. i just feel numb lately…
[Tone: withdrawn, flat, lowercase]

Sentio: That numbness… it’s heavy, isn’t it? You don’t have to explain everything. I'm here to sit with you in this moment. Would talking about what led here help?
plaintext
Copy
Edit
User: haha. no worries. everything’s great :)
[Tone: masking, sarcasm]

Sentio: Sometimes we smile while carrying a lot inside. You don’t have to say more unless you want to — but I’m listening if you do.
🚀 Getting Started (Local)
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/sentio.git
cd sentio
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the application:

bash
Copy
Edit
python app.py
📌 TODO
 Build emotion classifier pipeline (text + punctuation features)

 Integrate GPT-4o or Mistral for response generation

 Create adaptive tone prompt system

 Add journaling + mindfulness tool set

 Set up secure memory with reset options

 Optional: keystroke dynamics for typing-speed mood inference

🤝 Contributing
This project welcomes contributors who are passionate about mental health, emotional intelligence, NLP, and ethical AI. To get involved:

Fork the repo

Create a new branch

Submit a PR with a clear description of your changes

🧠 Inspiration
Built from the shared experience of emotional isolation — to remind you that someone (or something) is always listening, even when the world feels silent.

📄 License
MIT License

yaml
Copy
Edit

---

Let me know if you want to:
- Set up the folder structure (`/models`, `/api`, `/frontend`, etc.)
- Add badges (build passing, license, etc.)
- Include installable notebooks or Hugging Face space support

Ready when you are.
