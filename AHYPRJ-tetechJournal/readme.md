
# AI-Driven Instagram Auto Publisher

This project automates the publishing of content to Instagram using artificial intelligence and Telegram as the input interface. It enables users to submit photos via Telegram, automatically generate high-quality captions, overlay text on images if necessary, and post them as either stories or feed posts.

## 📦 Architecture Overview

### 1. Telegram Agent (User Interface)
- Built using `python-telegram-bot` with asynchronous handlers.
- Receives user photos and captions via Telegram.
- Handles commands like `/post` and `/stories` to route the content.
- Moves the received images into structured directories and triggers API calls.

### 2. FastAPI Service (`agent_social_media`)
- FastAPI app exposing endpoints:
  - `POST /process/post`
  - `POST /process/story`
- Each endpoint processes one post based on folder structure and content.
- Performs image resizing, OCR, text overlay, and caption generation using CrewAI agents.
- Final images are uploaded to Imgur and published to Instagram.

### 3. Instagram Posting
- Uses Instagram Graph API to publish images.
- Automatically manages `.posted` flags and deletes temporary Imgur uploads after use.
- Includes token expiration handling and refresh with automatic `.env` update.

### 4. Telegram Notification
- The backend can send logs and status updates back to a designated Telegram user or chat via a helper notification function.

## 🐳 Dockerized Deployment

### Services
- `telegram_agent` – Hosts the Telegram bot logic and orchestrates API calls.
- `agent_social_media` – Handles all AI processing and communication with Instagram.

### Volumes
Shared Docker volumes between the two containers allow for live file access and coordination.

```yaml
volumes:
  - ./telegram_agent:/app
  - ./agent_social_media:/agent_social_media
```

### Entrypoint Logic
The `agent_social_media` service uses an `entrypoint.sh` that ensures the Instagram token is always valid on startup:

```bash
#!/bin/bash
python3 autoupdateToken.py
uvicorn autopostapi:app --host 0.0.0.0 --port 1113
```

## 🛠️ Utilities

- `autoupdateToken.py` – Checks and refreshes Instagram API tokens.
- Telegram bot includes chat-based monitoring and log streaming.

## 🧪 Running Locally

To run locally for testing:
```bash
uvicorn autopostapi:app --reload --port 1113
```

Start the Telegram bot with:
```bash
python appAPI.py
```

## ✅ Status

- [x] Fully dockerized
- [x] Telegram bot receiving and routing images
- [x] FastAPI service handling post/story workflows
- [x] AI caption generation via CrewAI
- [x] Instagram posting and cleanup
- [x] Telegram notifications for logs
- [x] Automatic token refresh

## 📁 Structure

```
project-root/
├── telegram_agent/
│   ├── appAPI.py
│   ├── telegramBotAhyApi.py
│   └── ...
├── agent_social_media/
│   ├── autopostapi.py
│   ├── autoupdateToken.py
│   ├── core/
│   ├── infra/
│   └── ...
├── docker-compose.yml
└── README.md
```

---

_Last updated: 2025-05-02_

---