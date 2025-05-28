# 🧠 MultiAgents

**MultiAgents** is a library of autonomous agents designed for automation, experimentation, and task orchestration using LLMs (e.g., CrewAI, Guardrails, custom tools). It includes a wide variety of agents covering tasks like content generation, project planning, PDF handling, streamlit UIs, API integration, database interaction, and more.

---

## 🚀 Quick Setup

```bash
git clone https://github.com/ahy-git/multiagents.git
cd multiagents
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
````

---

## 📂 Agent Modules and Flows

### 🧠 Core Agents and Flows
<!-- AGENTS_START -->
| Directory                                          | Description                                 |
| -------------------------------------------------- | ------------------------------------------- |
| `001AutomatedProjectPlanner`                       | Automated project planning agent            |
| `002AssessingTrelloProjects`                       | Evaluates Trello productivity and cards     |
| `003SalesAgent`                                    | Simulated sales interaction agent           |
| `004SupportAnalyst`                                | Support agent with embedded troubleshooting |
| `005ContentCreator`                                | Text and content generator                  |
| `006BlogPostCrew/blogpost`                         | Blog writer crew (research, draft, edit)    |
| `10.00 Postgres`                                   | PostgreSQL integration agent                |
| `11.0 youtube`                                     | YouTube data extractor/processor            |
| `12.0 guardrails`                                  | Output validation using Guardrails          |
| `2.03 Multiplicacao para criancas`                 | Educational agent to teach multiplication   |
| `2.04 Chart Generator - Coffee production`         | Data viz agent for coffee production        |
| `2.05 Decorator`                                   | Python decorator pattern for agents         |
| `2.06 cache`                                       | Caching layer and test agent                |
| `2.07 ExchangeRage with cache`                     | Currency rates agent with cache             |
| `2.08 serperdevtool with cache`                    | Serper API tool with cache (non-functional) |
| `2.09 pdf creation tool`                           | PDF generation tool (non-functional)        |
| `3.01 - SimpleFlow No Crew`                        | Basic flow system without CrewAI            |
| `3.02 - SimpleFlowPrint`                           | Flow with intermediate print tracing        |
| `3.04 unstructured states`                         | Stateless execution flows                   |
| `3.05 StructuredState`                             | Structured flow state definitions           |
| `3.06 ConditionFlow`                               | Conditional branching flow                  |
| `3.07 FlowRouter`                                  | Task routing agent for complex flows        |
| `3.08 Flow Com Crew/flowcomcrew`                   | Multi-agent CrewAI-enabled flow             |
| `3.09 TOP Flow Reflection SeaxNG`                  | Experimental reflective agent pipeline      |
| `4.02 Streamlit`                                   | Streamlit front-end test for agents         |
| `4.03 TOP StreamlitPostcrewSearxngSpiderrs`        | Full pipeline: streamlit + crew + SearxNG   |
| `4.04 TOP AgenticPlataform`                        | Platform integrating multiple agent modules |
| `4.04 TOP EXTRA jsonpaser after docling`           | Docling-enhanced JSON parser tool           |
| `5.02 EvoAPI Configurando Tratamento de mensagens` | EvoAPI response router agent                |
| `6.01`                                             | Experimental CrewAI prototype               |
| `9.04 Facade Agent`                                | Facade agent orchestrating sub-agents       |
<!-- AGENTS_END -->
---

### 🌐 Integrations and Use Cases

| Directory            | Description                                 |
| -------------------- | ------------------------------------------- |
| `COMEX`              | International trade data retriever          |
| `gCalendar`          | Google Calendar integration agent           |
| `priceComparison`    | Price comparison across sources             |
| `tetechJournal`      | Technical journal/logging agent with memory |
| `zzzNCMRetrieval`    | Commodity classification retriever          |
| `zzzPdfExtractor`    | Text extractor for PDF files                |
| `zzzTestPydantic`    | Pydantic validation testbed                 |
| `zzzpriceComparison` | Alternative price comparison prototype      |
| `zzzsearchGithub`    | GitHub search tool agent                    |

---

## ⚙️ Project Assets

| File               | Purpose                           |
| ------------------ | --------------------------------- |
| `.envGIT`          | API credentials and token storage |
| `.gitignore`       | Git ignore configuration          |
| `requirements.txt` | Python dependency list            |

---

## 📌 Notes

* Some folders like `2.08` and `2.09` are experimental or broken.
* Agents are designed to be standalone – most can be run via `python main.py` in their folder.
* Designed for rapid prototyping of LLM-based systems and agentic flows.

---

## 🤝 Contributing

Pull requests are welcome. To contribute:

```bash
# Fork this repository
# Create your branch: git checkout -b my-feature
# Commit your changes: git commit -m "feat: added new agent"
# Push the branch: git push origin my-feature
```

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for more details.

---

For updates or more information, visit: [https://github.com/ahy-git/multiagents](https://github.com/ahy-git/multiagents)

```
