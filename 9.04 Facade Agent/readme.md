# 🤖 WhatsApp AI Assistant with CrewAI, Whisper & ElevenLabs (Modded from Sandeco's version)

This project is an intelligent, voice-enabled WhatsApp assistant powered by:

- 🧠 **CrewAI** for multi-agent task orchestration
- 🗣️ **Whisper (or FasterWhisper)** for audio transcription
- 📊 **Pandas** + **CSV query tool** for sales analytics
- 🗨️ **ElevenLabs** for realistic Text-to-Speech synthesis
- 📦 Flask-based webhook to integrate with WhatsApp

## 📌 Features

- ✅ Receives WhatsApp text or voice messages
- ✅ Transcribes voice messages using OpenAI's Whisper (or FasterWhisper)
- ✅ Handles natural language queries about structured CSV data
- ✅ Generates spoken responses using ElevenLabs voices
- ✅ Returns both text and audio to the user via WhatsApp
- ✅ Fully modular, built for local execution with extensibility

---

## 🛠️ Technologies Used

| Component       | Tech Stack                          |
|----------------|-------------------------------------|
| Backend Server | Flask                               |
| Messaging      | WhatsApp Webhook                    |
| NLP Engine     | [CrewAI](https://github.com/joaomdmoura/crewAI) |
| Transcription  | Whisper / FasterWhisper             |
| TTS            | ElevenLabs API                      |
| CSV Analysis   | Pandas, Custom Python Tool          |

---

## 📁 Folder Structure

```

.
├── app.py                     # Flask webhook server
├── receiveWhatsapp.py        # WhatsApp message parsing
├── sendWhatsapp.py           # Send messages/audio to WhatsApp
├── fluxo\_audio\_origin.py     # CrewAI flow handler
├── crew\_sales\_report.py      # Crew definition for CSV analysis
├── transcript.py             # Whisper-based transcription
├── generate.py               # ElevenLabs TTS generation
├── vendas\_ficticias\_brasil.csv  # Example CSV dataset
├── requirements.txt
└── README.md

````

---

## 🚀 How to Run

### 1. Clone and Install

```bash
git clone https://github.com/your/repo.git
cd your-project-folder
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
````

### 2. Add Environment Variables

Create a `.env` file:

```env
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

### 3. Start the Server

```bash
python app.py
```

The server will start on `http://0.0.0.0:6565`.

---

## ⚙️ Customization

* **Change Voice ID**
  In `generate.py`, replace `voice_id` with a free voice (e.g., "Matilda", "Brian").

* **CSV Source**
  Place your own `vendas_ficticias_brasil.csv` or modify `file_path` in `crew_sales_report.py`.

* **LLM Backend**
  Update `MyLLM.py` to use your preferred provider (Gemini, OpenAI, local LLM).

---

## 🔒 Notes

* Ensure Whisper or FasterWhisper is installed and configured correctly.
* ElevenLabs free tier has limited access to voices — use only supported IDs.
* Flask must be exposed to receive WhatsApp updates via public URL (e.g., Ngrok).

---

## 📈 Example Query

> Você pode mandar um áudio dizendo:
>
> “Qual vendedor teve mais vendas no mês passado?”

The system will:

1. Transcribe the audio
2. Use CrewAI to interpret and analyze CSV data
3. Generate a spoken answer
4. Send you a voice message back

---

## 🧠 Coming Soon

* [ ] Multilingual support
* [ ] Real-time dashboards
* [ ] Persistent chat memory
* [ ] CSV upload via WhatsApp

---

## 🤝 Contributing

Pull requests welcome. For major changes, please open an issue first.

---

## 📄 License

MIT License

---

