# 🧠 SQL Query Generator with CrewAI, Ollama, and PostgreSQL

This project is an AI-powered SQL query generator using **CrewAI**, **local LLMs via Ollama**, and a user-friendly **Streamlit** interface. It connects to local PostgreSQL databases, reads their schema, and generates optimized queries based on natural language input. Fork from Sandeco's.

---

## 📦 Features

- 🔍 Natural language to SQL conversion using multi-agent reasoning (CrewAI)
- 🧠 Supports LLMs like Qwen3, Llama3, Mistral, and Deepseek via **Ollama**
- 🗂️ Schema extraction and YAML generation for Postgres databases
- 📊 Streamlit interface for querying and visualizing results
- ✅ Optional JSON output formatting
- ⚙️ Custom YAML-based schema context improves accuracy
- 📁 Works with multiple databases (`clinica`, `ecommerce`) and customizable schema files

---

## 🚀 How It Works

1. Connects to a PostgreSQL database
2. Reads YAML schema file generated via `SchemaTool`
3. Uses **CrewAI agents**:
   - One agent to generate the SQL
   - Another agent to **clean and validate** the query output
4. Executes the generated query and shows the results in a table or chart

---

## 🛠️ Requirements

- Python 3.10+
- PostgreSQL running locally (default port: `5435`)
- `.env` file with:
```

DATABASE\_URI=postgresql://user\:password\@localhost:5435

```
- Ollama installed with models like:
```

ollama pull qwen:14b
ollama pull codellama:70b

```

---

## 🧪 Project Structure

```

📁 crewAI2/
├── 10.00 Postgres/
│   ├── crew\_query.py
│   ├── postgres\_connection.py
│   ├── postgres\_db.py
│   ├── schema\_generator.py
│   ├── testGenSchemas.py
│   ├── testCrewQuery.py
│   ├── crew\_query\_st.py      # Streamlit app
│   ├── schemas/              # Auto-generated YAML files
│   └── .env

````

---

## 🖥️ Running the App

```bash
# Generate YAMLs from schema
python testGenSchemas.py

# Run the Streamlit UI
streamlit run crew_query_st.py
````

---

## ✅ Example Input

> *"What are the top 5 products that cost less than \$100?"*

✅ Output:

```sql
SELECT name, price
FROM public.products
WHERE price < 100
ORDER BY price ASC
LIMIT 5;
```

---

## 🧠 Models Used

* Qwen3 14B (Ollama)
* Mistral small (for SQL cleanup)
* You can plug in any other LLM with large context window

---

## 📈 Chart Support

If your query returns numeric data, check **"Show results in chart?"** to view an auto-generated bar chart.

---

## 📚 License

This project is open-source and free to use.
