# VoiceFlow 🎙️

<p align="center">
  <strong>Modern Full-Stack Text-to-Speech Web Application — Free to Use Without API Keys</strong>
</p>

<p align="center">
  <a href="https://github.com/NO-NEED-NAME/VoiceFlow/releases">
    <img src="https://img.shields.io/github/v/tag/NO-NEED-NAME/VoiceFlow?color=7c3aed&label=Version&style=flat-square" alt="Version">
  </a>
  <a href="https://github.com/NO-NEED-NAME/VoiceFlow/actions/workflows/ci.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/NO-NEED-NAME/VoiceFlow/ci.yml?branch=main&label=CI%20Build&style=flat-square" alt="CI Status">
  </a>
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="License: MIT">
  <img src="https://img.shields.io/badge/React-18-61dafb?style=flat-square&logo=react" alt="React">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Edge--TTS-Community-0078d4?style=flat-square" alt="Edge TTS">
</p>

---

VoiceFlow is an open-source, full-stack Text-to-Speech (TTS) application that converts written text into natural-sounding speech **without requiring paid API keys or subscription tokens** (such as OpenAI or ElevenLabs). 

It connects to Microsoft's neural voice technology using the community-maintained `edge-tts` engine, providing a decoupled FastAPI backend and React frontend.

---

## 📸 Interface Preview

<p align="center">
  <img src="assets/voiceflow-ui-preview.png" alt="VoiceFlow User Interface" width="900" style="border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
</p>

---

## 📦 Releases

- 🚀 **[Releases & Tags Overview](https://github.com/NO-NEED-NAME/VoiceFlow/releases)**
- 🏷️ **Current Tag:** [`v1.0.0`](https://github.com/NO-NEED-NAME/VoiceFlow/releases/tag/v1.0.0)

---

## ✨ Features

- **No Paid API Keys Required:** Free to run locally for testing, research, and personal use without billing or token metering.
- **Natural Neural Voices:** Leverages neural voice synthesis models with multi-accent support.
- **Dynamic Speech Rate:** Fine-tune playback speed from 0.25x up to 4.0x.
- **Modern UI:** Built with React, Tailwind CSS, and Lucide icons.
- **Instant Audio Player & Download:** Listen to the generated speech directly in-browser or download as MP3.
- **Decoupled Architecture:** Clean separation between Python (FastAPI) API and React frontend.

---

## ⚠️ Architecture Note & Limitations

> [!WARNING]
> **Unofficial Upstream Endpoint:**
> VoiceFlow utilizes the open-source `edge-tts` Python library, which interfaces with the public endpoints powering Microsoft Edge's "Read Aloud" browser capability.
>
> **Considerations for Evaluators & Production Use:**
> 1. **No SLA Guarantee:** Because this relies on an unofficial upstream service, it does not provide an enterprise Service Level Agreement (SLA). The endpoint may be subject to occasional rate limiting, connection throttling, or upstream protocol updates by Microsoft.
> 2. **Network Dependency:** Stable internet connectivity is required to reach the TTS endpoints.
> 3. **Production Recommendation:** For commercial or high-availability deployments, the modular backend can be transitioned to official cloud SDKs (e.g., Azure Speech Services) or self-hosted offline engines (e.g., Piper, Coqui TTS).

---

## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React.js, Tailwind CSS, Lucide React, Axios |
| **Backend** | Python 3.9+, FastAPI, Edge-TTS, Motor (Async MongoDB Driver) |
| **Database** | MongoDB *(Optional — used for logging conversion history)* |
| **CI / CD** | GitHub Actions Workflow (`ci.yml`) |

---

## 🚀 Installation & Getting Started

Follow the steps below to run VoiceFlow on your local machine.

### Prerequisites
- **Node.js** (v16.x or higher)
- **Python** (v3.9 or higher)
- **Git**

---

### 1. Backend Setup (API Server)

1. Open a terminal and navigate to the `backend` folder:
   ```bash
   cd backend
   ```

2. (Recommended) Create and activate a virtual environment:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create an environment configuration file `.env` inside `backend/` *(Optional if using default settings)*:
   ```env
   MONGO_URL=mongodb://localhost:27017
   DB_NAME=voiceflow_db
   CORS_ORIGINS=http://localhost:3000
   ```

5. Run the FastAPI development server:
   ```bash
   python server.py
   ```
   > The API will start at: **http://localhost:8000** (Swagger documentation at `http://localhost:8000/docs`)

---

### 2. Frontend Setup (React Client)

1. Open a new terminal window and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install --legacy-peer-deps
   ```

   > **💡 Why is `--legacy-peer-deps` required?**
   > Starting from **npm v7+**, npm automatically resolves and enforces peer dependencies strictly. If any nested package specifies a peer dependency for an older React major version (for instance, older icon packages or Tailwind utilities expecting `react@^17.0.0` while the project uses `react@^18.0.0`), standard `npm install` halts with an `ERESOLVE unable to resolve dependency tree` error.
   > 
   > The `--legacy-peer-deps` flag instructs npm to revert to npm v4–v6 peer dependency resolution behavior, safely bypassing non-breaking transitive version discrepancies so installation finishes smoothly.
   > 
   > *Tip:* If you prefer running plain `npm install` without typing the flag each time, you can create a `.npmrc` file in your `frontend/` directory with:
   > ```ini
   > legacy-peer-deps=true
   > ```

3. Launch the development server:
   ```bash
   npm start
   ```
   > The application will open automatically in your browser at: **http://localhost:3000**

---

## 📝 How to Use

1. **Enter Text:** Paste or type the text you want converted into speech.
2. **Select Voice:** Choose your preferred neural voice (Male / Female, accents).
3. **Adjust Speed:** Set the desired speech rate between 0.25x and 4.0x.
4. **Generate:** Click **⚡ Generate Speech**.
5. **Listen & Export:** Stream audio playback directly or click **⬇ Download MP3** to save the file.

---

## 🗺️ Roadmap & Active Development

VoiceFlow is actively evolving. The following items represent our current development roadmap:

- [x] **v1.0.0 Tag:** Initial dual-stack architecture (FastAPI backend + React frontend).
- [ ] **Pitch & Volume Controls:** Extend UI controls to expose Edge-TTS pitch and volume adjustment flags.
- [ ] **Smart Text Chunking:** Split lengthy text into paragraph chunks to avoid stream timeouts on long conversions.
- [ ] **Persistent Audio History:** Option to store past generations locally or in MongoDB.
- [ ] **Subtitle Export:** Support generating word-level timestamps and SRT/VTT subtitle files.
- [ ] **Containerization:** Provide Dockerfile and Docker Compose configurations for one-command deployment.

👉 **View all open issues or request a feature at [VoiceFlow Issues Tracker](https://github.com/NO-NEED-NAME/VoiceFlow/issues)**.

---

## 🤝 Contributing

Contributions, bug reports, and feature suggestions are welcome!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
