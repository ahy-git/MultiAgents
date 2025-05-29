# 📰➡️🎙️ Blog to Podcast Agent (CrewAI)

This project uses the [CrewAI](https://docs.crewai.com/) framework to automatically transform **blog posts into podcasts**. It defines an agent that:

1. Scrapes the blog content using Firecrawl
2. Summarizes the content using an LLM
3. Converts the summary into natural-sounding speech using ElevenLabs

## 📦 Project Structure

- `BlogToPodcastCrew.py`: Main class defining the Crew, agent, and tasks.
- `toolElevenLabs.py`: Custom Tool for ElevenLabs API integration.
- `firecrawl_tool.py` (or imported official tool): Tool for scraping with Firecrawl.
- `.env`: Stores API keys securely via environment variables.

## 🚀 How It Works

The agent performs a sequential task:

1. Uses `FirecrawlScrapeWebsiteTool` to extract the blog content.
2. Summarizes it in a compelling way with a 2000-character limit.
3. Converts the summary into `.wav` audio using `ElevenLabsTool`.
4. Returns the path to the generated audio file.

## 🔧 Requirements

- Python 3.10+
- Packages: `crewai`, `crewai-tools`, `requests`, `python-dotenv`
- Valid API keys for:
  - [OpenAI](https://platform.openai.com/)
  - [Firecrawl](https://firecrawl.dev)
  - [ElevenLabs](https://www.elevenlabs.io/)

## 📁 Installation

```bash
git clone https://github.com/yourusername/blog-to-podcast-crewai.git
cd blog-to-podcast-crewai
pip install -r requirements.txt
```

Create a `.env` file with your API keys:

```
OPENAI_API_KEY=sk-...
FIRECRAWL_API_KEY=fc-...
ELEVENLABS_API_KEY=eleven-...
```

## ▶️ Running

```bash
python BlogToPodcastCrew.py
```

Or call it programmatically:

```python
crew = BlogToPodcastCrew()
audio_path = crew.kickoff("https://yourblog.com/article")
print(f"Podcast generated at: {audio_path}")
```

## 🧠 Custom LLM Support

You can swap in any compatible LLM (cloud or local), such as GPT-4o, Mistral, or Ollama:

```python
from MyLLM import MyLLM
self.llm = MyLLM.gpt4o_mini  # or use self.llm = MyLLM.OTHERMODEL
```

## 📝 Example Output

```
✅ Podcast generated at: audio_generations/podcast_HASH.wav
```

## 📄 License

MIT – Free for use and modification.

```

```
