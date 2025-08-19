# Create Your Own Character Chatbot

A dynamic CLI chatbot built with OpenAI Agents SDK that lets you create custom AI personas with unique personalities, expertise, and response styles - all protected by real-time content safety guardrails.

## ✨ Features

- **🎭 Dynamic Character Creation** - Define custom names, personalities, expertise, ages, and response styles
- **🛡️ Real-time Output Guardrails** - Configurable content safety filters (offensive, explicit, vulgar)
- **🧠 Stateful Conversations** - Maintains context across chat sessions
- **⚙️ Configurable Safety** - Choose your preferred guardrail intensity
- **🚀 Powered by Gemini** - Utilizes Google's Gemini 2.5 Flash model

## 🛠️ Tech Stack

- **OpenAI Agents SDK** - Agent orchestration, dynamic instructions, output guardrails
- **Google Gemini API** - LLM backbone via gemini-2.5-flash
- **Pydantic** - Structured output validation
- **SQLite** - Conversation session management
- **Python** - Core programming language

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/abdullahN111/ai-agents.git
cd ai-agents/Projects/create_your_own_chatbot

2. **Add your secrets**

OPENAI_API_KEY=your_openai_api_key_here (Optional for tracing)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta

3. **Install Modules and Run the Project**
```bash
uv add -r requirements.txt
uv run main.py