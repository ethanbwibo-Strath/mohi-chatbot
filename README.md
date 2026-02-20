# 🤖 Rafiki IT: Missions of Hope International (MOHI) Support Chatbot

**Rafiki IT** is a Retrieval-Augmented Generation (RAG) assistant designed to provide empathic, accurate, and mission-aligned technical support to MOHI staff. It leverages internal documentation to answer queries regarding I.T. policies, portal navigation, and office procedures.

---

## 🚀 The Architecture
The system is built on a modular "Engine" that separates knowledge storage from the user interface, allowing for model-agnostic flexibility.



### Tech Stack:
* **Backend:** FastAPI (Python)
* **Orchestration:** LangChain (v1.0 Modular Structure)
* **Vector Database:** ChromaDB (Local storage for data privacy)
* **Embeddings:** OpenAI `text-embedding-3-small`
* **LLM:** GPT-4o-mini
* **Frontend:** Streamlit

---

## ✨ Key Features
* **Empathic Support:** Custom system directives ensure the bot acknowledges user distress (e.g., sickness or stress) before providing technical solutions.
* **Conversational Memory:** Implements `ConversationalRetrievalChain` to maintain context across multi-step technical workflows.
* **MOHI Specific:** Grounded in actual MOHI documents, including the I.T. Policy and Pangani Center extension guides.
* **Local Privacy:** Uses a local vector store to ensure internal documentation is indexed securely.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ethanbwibo-Strath/mohi-chatbot.git
   ```
2. **Setup Virtual Environment:**
   ```bash
   py -3.13 -m venv venv
   venv\Scripts\activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install fastapi uvicorn langchain-openai langchain-chroma langchain-core langchain-classic streamlit python-dotenv
   ```
4. **Environment Variables:**
   Create a `.env` file with your `OPENAI_API_KEY`.

---

## 📂 Project Structure
* `/app/services/knowledge.py`: Handles document loading, chunking, and vectorization.
* `/app/services/chatbot.py`: Contains the retrieval logic and personality directives.
* `/app/main.py`: FastAPI routes.
* `interface.py`: Streamlit-based chat interface.
* `/data`: Directory for internal PDF/Docx documentation.

---

## 💡 Future Roadmap
- [ ] Integration with MOHI's internal Slack or Microsoft Teams.
- [ ] Support for Swahili-based queries.
- [ ] Automated ticket creation for the Pangani IT Helpdesk.

---
**Developed by Ethan Bwibo** *IT Intern @ Missions of Hope International (MOHI)*