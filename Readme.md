# AccessoryIQ

## product-accessory-intelligence

---

## 🎯 Overview

**AccessoryIQ** is a production-grade AI system that recommends compatible accessories for electronic products using **verified technical documentation** and **trusted community knowledge** — never guesses, never hallucinates.

It is built around a **RAG-first architecture** (Retrieval-Augmented Generation) with a **controlled search fallback**, ensuring accuracy, explainability, and safety.

---

## ✅ Core Principles

- Evidence over assumptions
- RAG before Search
- Search only when RAG fails
- No hallucinations
- Source transparency
- Deterministic output

---

## 🧠 System Architecture

    User Input
        ↓
    RAG Engine (FAISS + PDFs)
        ↓
    [If RAG Fails]
        ↓
    Trusted Web Search (Serper)
        ↓
    Planner Agent
        ↓
    Structured Output + Confidence

## 📂 Project Structure

---
    AccessoryIQ/
    │
    ├── app/
    │ ├── agents/
    │ │ ├── evidence_agent.py
    │ │ ├── search_agent.py
    │ │ └── planner_agent.py
    │ │
    │ ├── rag/
    │ │ ├── pdf_loader.py
    │ │ ├── chunking.py
    │ │ ├── vector_store.py
    │ │
    │ ├── pipeline/
    │ │ └── main_pipeline.py
    │ │
    │ └── ui/
    │ └── app.py
    │
    ├── config/
    │ └── settings.py
    │
    ├── data/
    │ └── pdfs/
    │
    ├── .env
    ├── requirements.txt
    └── README.md
---


## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/AccessoryIQ.git
   cd AccessoryIQ
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**

   Create a `.env` file in the root directory and add your OpenRouter API key and the serper API Key:
   ```
    OPENROUTER_API_KEY=your_key_here
    OPENROUTER_MODEL=meta-llama/llama-3-8b-instruct
    OPENROUTER_FALLBACK_MODEL=mistralai/mixtral-8x7b-instruct
    SERPER_API_KEY=your_serper_key_here

   ```

---

## 🛠️ Usage

1. **Run the application**

   ```bash
   python -m ui.app 
   ```

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please review the [CONTRIBUTING.md](CONTRIBUTING.md) guidelines for details.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## License
This project is licensed under the **MIT** License.

---
🔗 GitHub Repo: https://github.com/Manisankarrr/AccessoryIQ