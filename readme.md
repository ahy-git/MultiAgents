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
| Directory | Description (Optional) |
|-----------|------------------------|
| `AWL-001-BlogToPodcastAgent` | An autonomous CrewAI agent that scrapes blog content, summarizes it in natural language, and converts it into a human-like podcast using ElevenLabs. Ideal for automating blog-to-audio transformations. |
| `AWL-002-HeartbrokenTherapist` | The BreakupRecoveryCrew is a modular CrewAI agent system designed to help users emotionally recover from breakups. It includes four specialized agents: an empathetic therapist for emotional validation, a closure expert for unsent messages and healing rituals, a planner for a 7-day recovery routine, and a brutally honest advisor that offers raw, fact-based insights using web search. Built with LLM orchestration and optional image input support, this crew provides structured, multi-perspective guidance to navigate emotional distress. |
| `AWL-003-DataAnalsysisAgent` | This module provides a lightweight data analytics agent system using CrewAI, featuring two tools: PandasTools for in-memory DataFrame operations via natural language, and DuckDBQueryTool for executing SQL queries on CSV files using DuckDB. The DataQueryCrew class orchestrates the process, enabling an LLM-powered agent to analyze uploaded tabular data, generate insights, and return results through either SQL or pandas-based logic—ideal for automating business intelligence queries without requiring a database backend or manual coding. |
| `AWL-004-DataVisualization` | AI-powered data analysis and visualization using sandboxed Python execution. Transforms business questions into insights with automated charts, secure E2B environment, and CrewAI-driven reporting. Ideal for CTOs seeking scalable, intelligent analytics. |
| `DL-001AutomatedProjectPlanner` | A multi-agent CrewAI pipeline that transforms structured project input into a detailed project plan with task breakdown, time/resource estimates, risk mitigation, and a Mermaid-compatible Gantt chart. Outputs a full Markdown execution report including token usage, models used, and serialized plan data. |
| `DL-002AssessingTrelloProjects` | CrewAI implementation for automated project assessment: Orchestrates specialized agents to collect data, analyze metrics, generate reports, and validate outputs with hallucination checks. Features custom tools for data fetching, JSON processing, and performance logging. |
| `DL-003SalesAgent` | This advanced CrewAI pipeline automates lead qualification and personalized email outreach. It uses structured agents to extract lead data, assess cultural fit, calculate a validated lead score, and generate optimized emails. The flow branches based on lead quality (high/medium/low), enabling targeted actions like syncing with Salesforce or sending customized follow-ups. Results are validated via Pydantic schemas, and email content is refined with strong CTAs—ideal for scalable B2B sales automation using agentic workflows. |
| `DL-004SupportAnalyst` | A CrewAI workflow that analyzes support tickets, generates improvement suggestions, charts, and tables, and assembles a final markdown report using LLM and CSV data. |
| `DL-005ContentCreator` | A multi-agent CrewAI pipeline that monitors financial news, analyzes market data, and generates a markdown article with platform-specific social media posts using LLMs and web tools. |
| `DL-006BlogPostCrew` | A structured CrewAI workflow that researches a given topic and generates a detailed markdown report for blog posting. |
| `SD-.07 ExchangeRage with cache` | A simple CrewAI setup with a currency monitoring agent that queries the USD/BRL exchange rate using a custom tool with caching logic to avoid redundant API calls within 1 hour. |
| `SD-10.00 Postgres` | A smart, Streamlit-based AI assistant that empowers non-technical users to query relational databases (Postgres, MySQL, SQLite) using natural language. It translates plain-language questions into optimized SQL statements using multi-agent reasoning, executes them securely, and presents results as dynamic tables or charts. Ideal for business analysts, product teams, and operations looking to derive insights from structured data without writing a single line of SQL. |
| `SD-11.0 youtube` | An AI-driven multi-agent platform for YouTube analysis, combining comment extraction, engagement metrics, and trend detection by category and region. Ideal for marketers and strategists to monitor feedback, optimize performance, and track viral content with LLM-powered automation. |
| `SD-12.0 guardrails` | This crew automates JSON profile generation using LLMs, with built-in validation and error correction. It generates a structured profile (name, age, profession), validates output using Guardrails, and rewrites prompts iteratively until the format is correct—ideal for robust, schema-compliant profile creation in business workflows. |
| `SD-2.03 Multiplicacao para criancas` | A playful CrewAI setup that teaches multiplication to children using emojis, where one agent generates random numbers and another explains the concept in a kid-friendly way with visual examples. |
| `SD-2.04 Chart Generator - Coffee production` | A CrewAI workflow that researches Brazil's 2024 coffee production by bean type using web search, then generates a pie chart visualizing the percentage distribution for each variety. |
| `SD-2.06 cache` | A simple CrewAI tool-agent setup where a writer agent uses a cached multiplication tool (caching even results) to teach math lessons to children. |
| `SD-2.08 serperdevtool with cache (Only code not working)` | A web search agent using the SerperDevTool with a custom cache function that avoids repeated searches within one hour, optimized for efficient query handling. |
| `SD-2.09 pdf creation tool (not working)` | A CrewAI tool that generates a PDF with a title, text, and embedded image—ideal for creating visual reports and summaries. |
| `SD-3.01 - SimpleFlow No Crew` | A simple CrewAI Flow that greets the user, collects two numbers via input, and calculates their sum in a sequential three-step process. |
| `SD-3.02 - SimpleFlowPrint` | A basic CrewAI Flow that greets the user, collects two input numbers, calculates their sum, and visualizes the flow using plot(). |
| `SD-3.04 unstructured states` | A CrewAI Flow that demonstrates unstructured state management across stages, progressively building a message about a user-defined topic using internal state and multiple sequential crews. |
| `SD-3.05 StructuredState` | A structured CrewAI Flow using a typed state model to sequentially build information across three stages, demonstrating clear state tracking with Pydantic. |
| `SD-3.06 ConditionFlow` | Two CrewAI Flows demonstrating conditional branching: one using and_() to consolidate after multiple validations, and another using or_() to trigger logging when any stage completes. |
| `SD-3.07 FlowRouter` | A CrewAI Flow using @router to conditionally branch execution based on a random boolean, directing the process to either a success or failure path. |
| `SD-3.08  Flow Com Crew` | No description available. |
| `SD-3.09 TOP Flow Reflection SeaxNG` | A multi-agent CrewAI system with iterative reflection and critique. It uses a researcher, writer, and reviewer to generate short, impactful texts on a given topic, then routes the result through a critique loop until the output is validated or marked “perfect.” Includes a custom SearxNG search tool with thematic and temporal filters for enriched content sourcing. |
| `SD-4.03 TOP StreamlitPostcrewSearxngSpiderrs` | A multi-agent CrewAI system for generating high-quality blog posts. It combines web search (via SearxNG), remote scraping, and collaborative writing with agents for research, writing, and revision—optimized for use in web apps like Streamlit. |
| `SD-4.04 TOP AgenticPlataform` | A Streamlit-based agentic platform powered by CrewAI that allows users to generate blog posts and summarize PDFs. It integrates multi-agent crews with tools like SearxNG, RemoteScraper, and PDFSearchTool to research, write, revise, and extract structured insights from documents—all optimized for interactive content creation and AI-assisted workflows. |
| `SD-4.04 TOP EXTRA jsonpaser after docling` | A fully automated PDF summarization pipeline using CrewAI and Docling. It converts PDFs into structured JSON, splits content into sections, generates per-section markdown summaries, recursively synthesizes them into a final report, and handles cleanup—delivering a concise, structured, and human-readable summary file. |
| `SD-6.01-SummaryCrewForWhatsapp` | A fully automated system for generating structured WhatsApp group message summaries using CrewAI and Evolution API. It provides a Streamlit interface to configure groups, schedules daily summary tasks per group, processes recent messages using LLMs, and delivers concise summaries via WhatsApp. It supports batch scheduling, message filtering, media handling, and system-level task automation across Windows, Linux, and macOS. |
| `SD-9.04 Facade Agent` | An AI-powered WhatsApp assistant that intelligently handles customer messages—classifying them as sales-related or general inquiries. It automatically transcribes audio, generates context-aware responses using advanced language models, and replies via text and voice using ElevenLabs TTS. Designed for operational efficiency, it also interprets structured sales queries from CSV data, providing insights and summaries in natural language—enhancing customer engagement and streamlining sales intelligence. |
| `tool-SD-2.05 Decorator` | A CrewAI tool that multiplies two integers and returns a formatted string with the result. |
| `zzzMVPAutomation` | No description available. |
| `zzzNCMRetrieval` | No description available. |
| `zzzPdfExtractor` | No description available. |
| `zzzTestPydantic` | No description available. |
| `zzzgCalendar` | No description available. |
| `zzzpriceComparison` | No description available. |
| `zzzpriceComparison2` | No description available. |
| `zzzsearchGithub` | No description available. |

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
