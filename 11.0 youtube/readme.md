# 💬 YouTube Comments Analyzer

This is a project for analyzing YouTube video comments using intelligent agents built with [CrewAI](https://github.com/joaomdmoura/crewai) and a user-friendly interface powered by [Streamlit](https://streamlit.io/). The goal is to extract and analyze meaningful user comments, filtering out generic ones and generating insights about audience needs, feedback, and suggestions.

---

## 🚀 Features

- ✅ Automatically extracts comments from YouTube videos
- ✅ Filters out generic praise and irrelevant messages
- ✅ Analyzes user feedback patterns (complaints, questions, suggestions)
- ✅ Simple and interactive interface built with Streamlit
- ✅ Powered by CrewAI agents for task execution

---

## 📁 Project Structure

```bash
📁 project/
│
├── st_comments.py             # Comment Analyzer Streamlit UI
├── st_trends.py               # Trend Analyzer Streamlit UI
├── crew_comments_analyzer.py  # CrewAI agent and task setup
├── crew_trends_analyzer.py    # CrewAI agent and task setup
├── crew_links_analyzer.py     # CrewAI agent and task setup
├── tool_comments.py           # CrewAI tool to fetch YouTube comments
├── tool_trends.py             # CrewAI tool to fetch YouTube trends
├── tool_youtube_videos.py     # CrewAI tool to fetch YouTube videos details
├── MyLLM.py                   # LLM configuration and integration
├── .env                       # Contains your YouTube API key (never commit this!)
├── yt_categories.json         # (optional) YouTube category reference
├── yt_regions.json            # (optional) YouTube region reference
````

---

## ⚙️ How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/youtube-comments-analyzer.git
cd youtube-comments-analyzer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> Make sure you have `crewai`, `streamlit`, and `python-dotenv` installed.

### 3. Set your YouTube API key

Create a `.env` file in the root directory:

```
YOUTUBE_API_KEY=your_api_key_here
```

### 4. Launch the app

```bash
streamlit run st_comments.py
```

Open your browser and go to `http://localhost:8501`.

---

## 🧰 Tech Stack

* [Streamlit](https://streamlit.io/) – interactive Python UI
* [CrewAI](https://github.com/joaomdmoura/crewai) – multi-agent orchestration
* [YouTube Data API v3](https://developers.google.com/youtube/v3) – comment data source
* [Python 3.10+](https://www.python.org/) – programming language

---

## ⚠️ Notes

* The tool respects YouTube API limits and content availability.
* Comments may be disabled or restricted on some videos.
* Do not expose your API key publicly – never commit your `.env` file.

---
