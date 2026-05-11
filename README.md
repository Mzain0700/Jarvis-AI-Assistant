# Jarvis AI Assistant

Jarvis is a local, modular AI assistant that integrates several AI services for chat, decision routing, image generation, and audio I/O. The project is designed to run locally with configurable backends and safe handling of secrets via a local `.env` file.

## Table of Contents

- Project overview
- Detailed feature list
- How Jarvis works (end-to-end)
- Repository layout
- Requirements
- Environment variables (`.env`)
- Quick start
- How to run
- Backend modules (what each does)
- Frontend / GUI
- Development
- Security & secrets
- Contributing
- License
- Troubleshooting & common fixes

---

## Project overview

This repository contains the code for "Jarvis" — a desktop/local AI assistant. The assistant:

- Routes voice/text queries between chat, real-time search, and task automation
- Uses `Cohere` for intent/decision routing and `Groq` for conversational responses
- Calls Hugging Face inference endpoints for image generation
- Provides speech-to-text input and text-to-speech output
- Shows live assistant state and chat history in a responsive PyQt GUI

All credentials live in a local `.env` file (not committed). A safe example is provided in `.env.example`.

## Detailed feature list

### 1) Intelligent decision routing
- `Backend/Model.py` classifies each query into actionable intents such as:
  - `general` (normal chat/explanations)
  - `realtime` (internet-aware queries)
  - `open`, `close`, `play`, `system`, `content`, `google search`, `youtube search`
  - `generate image`, `exit`, and more
- This routing helps Jarvis choose the right module instead of using one generic response path.

### 2) Conversational AI with memory
- `Backend/Chatbot.py` handles standard assistant conversations through Groq.
- Messages are persisted in `Data/ChatLog.json`, so ongoing interaction context is retained.
- Replies are cleaned/formatted before being shown in the UI and spoken aloud.

### 3) Real-time web-aware answers
- `Backend/RealtimeSearchEngine.py` fetches web search results and uses Groq to convert them into readable answers.
- Useful for current events, recent updates, or topics that need fresh information.

### 4) Voice-first interaction
- `Backend/SpeechToText.py` captures microphone input via a browser speech-recognition bridge and normalizes user queries.
- Supports configurable input language using `.env` (`InputLanguage`).

### 5) Natural text-to-speech output
- `Backend/TextToSpeech.py` uses `edge-tts` + `pygame` playback.
- For long answers, Jarvis uses a combined threshold (both conditions must be true): over ~250 characters **and** more than 4 period-delimited segments; when triggered, it speaks roughly the first two sentence segments and appends a short “check chat for the rest” message.

### 6) Automation and desktop actions
- `Backend/Automation.py` executes multi-command actions asynchronously:
  - open/close apps
  - play music on YouTube
  - perform Google/YouTube searches
  - write content files
  - run system volume controls
- This makes Jarvis an assistant for both information and direct task execution.

### 7) AI image generation
- `Backend/ImageGeneration.py` sends prompts to Hugging Face Stable Diffusion XL.
- Generates multiple image outputs per prompt and opens them from local `Data/`.

### 8) Responsive, modern GUI
- `Frontend/GUI.py` provides:
  - animated Jarvis core visualization
  - live status updates (`Listening`, `Thinking`, `Searching`, `Answering`, `Available`)
  - mic toggle control
  - home and message views with custom top bar controls
- Backend and UI communicate through lightweight data files in `Frontend/Files`.

### 9) Privacy-focused local setup
- API keys are stored in local `.env`, not in source files.
- Runtime logs/media are local to your machine.
- Designed for local execution with modular service integrations.

## How Jarvis works (end-to-end)

1. You speak (or provide input) through the GUI mic flow.
2. `SpeechToText` converts speech to text and normalizes the query.
3. `Model.FirstLayerDMM` (First-Layer Decision-Making Model, DMM) classifies the intent(s).
4. `Main.py` orchestrates the action path:
   - `general` → `ChatBot`
   - `realtime` → `RealtimeSearchEngine`
   - task commands → `Automation`
   - image request → `ImageGeneration`
5. Result text is displayed in the GUI and spoken with `TextToSpeech`.
6. Conversation is saved in `Data/ChatLog.json` for continuity.

## Why this assistant is strong

- **Multi-capability in one app:** chat, real-time search, automation, image generation, and voice I/O.
- **Smart routing:** intent classification avoids one-size-fits-all responses.
- **Hands-free workflow:** built for microphone-driven usage with spoken responses.
- **Modular architecture:** each feature lives in a focused backend module, making extension easier.
- **Practical desktop control:** can act on the system/web, not just answer questions.
- **Local-first secret handling:** `.env`-based credential management keeps sensitive keys out of version control.

## Repository layout

- `Main.py` — application entrypoint and orchestrator
- `Backend/` — core logic and integrations
	- `Automation.py` — automation routines and content generation helpers
	- `Chatbot.py` — chat orchestration and prompt wiring
	- `ImageGeneration.py` — utilities to generate and open images
	- `Model.py` — model client wiring and helpers
	- `RealtimeSearchEngine.py` — routing for queries that need live data
	- `SpeechToText.py` — speech recognition utilities
	- `TextToSpeech.py` — text-to-speech helpers using `edge_tts`
	- `test.py` — quick experiments and local tests
- `Frontend/` — GUI scripts and assets
- `Data/` — runtime data, chat logs, generated assets
- `.env.example` — example environment variables (safe to commit)
- `.gitignore` — ignores `.env` and other artifacts
- `Requirements.txt` — python dependencies

## Requirements

- Python 3.10+ recommended. Confirm with `python --version`.
- Install dependencies:

```bash
python -m pip install -r Requirements.txt
```

Use a virtual environment (recommended):

```bash
python -m venv .venv
# PowerShell
.\\.venv\\Scripts\\Activate.ps1
# then
pip install -r Requirements.txt
```

## Environment variables (`.env`)

Create a `.env` by copying the provided `.env.example` and filling in real values. DO NOT commit `.env`.

Example (copy then edit):

```bash
Copy-Item -Path .env.example -Destination .env
```

Key variables currently used by the codebase:

- `Username` — displayed assistant username
- `Assistantname` — assistant name
- `GroqApiKey` — API key for Groq integrations
- `CohereApiKey` — API key for Cohere
- `HuggingFaceAPIKey` — Hugging Face token for inference
- `InputLanguage` — language code for speech recognition (e.g., `en`)
- `AssistantVoice` — TTS voice id (e.g., `en-US-AriaNeural`)

Files and modules load `.env` using `python-dotenv` (`dotenv_values`) so values are accessed via `env_vars.get("VAR_NAME")`.

## Quick start

1. Clone:

```bash
git clone https://github.com/Mzain0700/Jarvis-AI-Assistant.git
cd Jarvis-AI-Assistant
```

2. Copy `.env.example` → `.env` and fill in keys.
3. Install dependencies.
4. Run the main program:

```bash
python Main.py
```

## How to run

- The primary entrypoint is `Main.py`. Depending on how that script is written, it will launch the GUI or start backend services. If your environment has GUI dependencies, ensure the required display libraries are available.
- For quick backend checks, run individual modules directly, for example:

```bash
python Backend/test.py
```

## Backend modules (summary)

- `Automation.py`: builds prompts and automates tasks — uses `Username` from `.env` for personalization.
- `Chatbot.py`: loads `GroqApiKey`, `Username`, and `Assistantname` for chat context.
- `RealtimeSearchEngine.py`: routes queries and uses `CohereApiKey`.
- `ImageGeneration.py`: calls Hugging Face APIs and expects `HuggingFaceAPIKey`.
- `SpeechToText.py` & `TextToSpeech.py`: TTS and STT integrations using `InputLanguage` and `AssistantVoice`.

Read top-of-file comments in each module for implementation-specific notes.

## Frontend / GUI

- The GUI files live in `Frontend/` and are built with `PyQt5`.
- Ensure your environment supports desktop rendering for Python GUI applications.

## Development

- When adding dependencies, update `Requirements.txt`.
- Keep secrets in `.env` only. Use environment-specific secret stores for CI/CD.

## Security & secrets

- This repository enforces push protection and secret scanning. Never commit `.env` or API keys.
- If a secret is accidentally committed, immediately rotate the secret and remove it from history. Example steps:

```bash
# remove the file from history (careful! rewrites history)
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch .env" --prune-empty --tag-name-filter cat -- --all
git push origin --force --all
```

Note: Rewriting history affects collaborators. Coordinate before doing that.

## Contributing

- Fork the repository and create feature branches.
- Open a pull request describing your changes.

## License

Add a license file if you want to make the project open-source. Common choices: MIT, Apache-2.0.

## Troubleshooting & common fixes

- `detected dubious ownership`: run

```powershell
git config --global --add safe.directory "G:/Project/Jarvis"
```

- `push declined due to secret scanning`: remove secrets from commits, rotate keys, and push a clean branch.
- `error: src refspec main does not match any`: ensure you have a `main` branch locally or create it with `git branch -M main`.

---

If you'd like I can also:

- Add badges and quick commands at the top of the README.
- Create helper scripts `run.bat` / `run.sh` to start the app.
- Add `CONTRIBUTING.md` and `LICENSE` files.

Tell me which additions you'd like and I will add them.
