# 📅 Appointment AI Agent Bot

An AI-powered Telegram scheduling assistant that helps users book, manage, update, and cancel appointments using natural language conversations.

Built with modern AI agent architecture using **LangGraph**, **FastAPI**, and **LLMs**.

---

## 🤖 Bot Access

**Telegram Bot:**  
[@Scheduler_AI_Agent_bot](https://t.me/Scheduler_AI_Agent_bot)

---

# ✨ Features

## 🧠 Natural Language Scheduling

Users can chat naturally with the bot:

- “Book a haircut for tomorrow at 3 PM”
- “Schedule a meeting next Monday at 4 PM”
- “Cancel my appointment for Friday”
- “Show my appointments this week”

The AI understands:

- Relative dates (`tomorrow`, `next Monday`)
- Time formats (`3 PM`, `15:00`)
- Intent detection
- Appointment modifications

---

## 📌 Appointment Management

### ✅ Create Appointments
Book appointments instantly through chat.

### 🔄 Update Appointments
Reschedule existing bookings naturally.

### ❌ Cancel Appointments
Cancel bookings with conversational commands.

### 📖 View Appointments
See upcoming or past appointment history.

---

## 🏢 Smart Business Logic

The bot automatically enforces:

- Business hours: **Mon–Sat | 09:00 AM – 06:00 PM**
- No Sunday bookings
- No past-date appointments
- Double-booking prevention
- User rate limiting

---

## 🧠 AI Agent Architecture

Powered by:

- LangGraph stateful workflows
- Persistent conversation memory
- Tool-based AI actions
- LLM reasoning for scheduling decisions

---

# 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| AI Agent | LangGraph + LangChain |
| LLM | Groq (Llama 3.1) / OpenAI Compatible |
| Database | SQLite + aiosqlite |
| Cache & Rate Limiting | Upstash Redis |
| Telegram Integration | python-telegram-bot |
| Config Management | Pydantic Settings + dotenv |

---

# 🚀 Quick Start

## 1️⃣ Clone Repository

```bash
git clone https://github.com/AmanMahor21/appointment-agent.git

cd appointment-agent
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Configure Environment Variables

Copy environment file:

```bash
cp .env.example .env
```

Update `.env`:

```env
# LLM
OPENAI_API_KEY=your_groq_api_key_here

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_WEBHOOK_URL=https://your-domain.com/webhook/telegram

# Database
DATABASE_URL=appointments.db

# Upstash Redis
UPSTASH_REDIS_REST_URL=your_upstash_redis_rest_url
UPSTASH_REDIS_REST_TOKEN=your_upstash_redis_token
```

---

## 4️⃣ Run the Application

```bash
python main.py
```

The application will:

- Create the SQLite database automatically
- Register Telegram webhook
- Start the FastAPI server

---

# ⚙️ Configuration

You can easily customize:

- Business working hours
- Maximum bookings per user
- AI model provider
- Rate limiting settings
- Prompt behavior
- Appointment duration rules

---

# 🔒 Security & Best Practices

✅ Webhook-based Telegram integration  
✅ Environment variable protection  
✅ Rate limiting implemented  
✅ Persistent AI conversation memory  
✅ Input validation & scheduling checks  
✅ Async architecture for scalability

---

# 📌 Future Enhancements

- Google Calendar integration
- Multi-service appointment durations
- Admin dashboard
- Email & SMS notifications
- Payment gateway integration
- Voice message support

---

# 🤝 Contributing

Contributions are welcome.

You can help by:

- Reporting bugs
- Suggesting new features
- Improving prompts
- Optimizing workflows
- Submitting pull requests

---

# 📄 License

This project is licensed under the MIT License.

---

# ❤️ Built With

- LangGraph
- FastAPI
- Groq
- Telegram
- AI Agents & Modern LLM Workflows
