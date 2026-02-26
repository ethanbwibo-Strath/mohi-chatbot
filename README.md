<!-- # 🤖 Rafiki IT: Missions of Hope International (MOHI) Support Chatbot

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
**Developed by Ethan Bwibo** *IT Intern @ Missions of Hope International (MOHI)* -->

# 🤖 Rafiki IT: Missions of Hope International (MOHI) Support Chatbot

**Rafiki IT** is an intelligent Retrieval-Augmented Generation (RAG) assistant designed to provide empathic, accurate, and mission-aligned technical support to MOHI staff. It serves as a 24/7 technical bridge, grounding responses in official MOHI manuals while maintaining a "Christ-centered" approach of grace and holistic ministry.

---

## 🚀 The Architecture
The system utilizes a decoupled **Headless Architecture**, where a custom Python backend (The Brain) serves a modern web interface (The Face) via a REST API.



### Tech Stack:
* **Backend:** FastAPI (Python 3.13)
* **Orchestration:** LangChain (RAG Implementation)
* **Vector Database:** ChromaDB (Local storage for data privacy)
* **Embeddings:** OpenAI `text-embedding-3-small` 
* **LLM:** GPT-4o-mini (Pay-as-you-go API model)
* **Frontend:** React (Tailwind CSS, Lucide Icons, React-Markdown)

---

## ✨ Key Features
* **Empathic Support:** Custom directives ensure Rafiki acknowledges user well-being (e.g., stress or illness) before technical troubleshooting.
* **Conversational Memory:** Remembers context to assist with multi-step technical workflows (e.g., portal navigation).
* **Branded Interface:** Custom UI featuring MOHI brand colors (#1c3c54, #4595d1, #8bc53f) and an adaptive Light/Dark mode.
* **Quick Actions:** One-tap access for common queries like **IT Office Location**, **Portal Lockouts**, and **Leave Applications**.
* **Local Privacy:** Internal manuals (I.T. Policy, Mission & Values) are indexed locally and never used to train public models.

---

## 🛠️ Installation & Setup

### 1. Backend Setup
```bash
git clone [https://github.com/ethanbwibo-Strath/mohi-chatbot.git](https://github.com/ethanbwibo-Strath/mohi-chatbot.git)
cd mohi-chatbot
py -3.13 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run build
```

### 3. Execution
* **Start Brain:** `uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload`
* **Start Face:** `npm start` (or serve the `build/` folder via the MOHI portal)

---

## 📂 Project Structure
* `/app/services/knowledge.py`: Document ingestion, chunking, and vectorization.
* `/app/services/chatbot.py`: RAG logic and Christ-centered personality directives.
* `/app/main.py`: FastAPI REST endpoints and CORS configuration.
* `/frontend/src/App.js`: React chat interface, FAB widget, and theme logic.
* `/data`: Official MOHI documentation (PDF/Docx).

---

## 💡 Future Roadmap
- [x] High-fidelity React Frontend with Dark Mode.
- [x] Floating Chat Widget for seamless portal integration.
- [x] Multi-lingual support (Swahili/English).
- [x] Satisfaction Rating (Thumbs + Follow-up).
- [ ] Automated ticket creation for the Pangani IT Helpdesk.


---
**Developed by Ethan Bwibo** *IT Intern @ Missions of Hope International (MOHI)*