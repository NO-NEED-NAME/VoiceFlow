# VoiceFlow 🎙️

VoiceFlow is a modern, full-stack Text-to-Speech (TTS) application that converts text into natural-sounding speech completely for **FREE**. 

It uses **Microsoft Edge TTS** technology to provide high-quality, neural voices without requiring any paid API keys (like OpenAI).

*(Note: You can add a screenshot of your app here)*

## ✨ Features

- **100% Free & Unlimited:** No credit card or API key required.
- **High-Quality Voices:** Uses neural network voices from Microsoft Edge.
- **Speed Control:** Adjust playback speed from 0.25x to 4.0x.
- **Modern UI:** Built with React and Tailwind CSS.
- **Download Audio:** Easily download the generated speech as MP3.
- **Dual Stack:** Python (FastAPI) Backend + React Frontend.

## 🛠️ Tech Stack

- **Frontend:** React.js, Axios, Tailwind CSS, Lucide React
- **Backend:** Python, FastAPI, Edge-TTS, Motor (MongoDB driver)
- **Database:** MongoDB (Optional - for history logs)

---

## 🚀 Installation Guide

Follow these steps to run the project locally.

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.9 or higher)

### 1. Backend Setup (Server)

Navigate to the backend folder:
```bash
cd backend
Install python dependencies:

Bash

pip install -r requirements.txt
Create a .env file in the backend folder (Optional for Edge TTS version, but good practice):

Code snippet

MONGO_URL=mongodb://localhost:27017
DB_NAME=voiceflow_db
CORS_ORIGINS=http://localhost:3000
Run the server:

Bash

python server.py
The server will start at http://localhost:8000

2. Frontend Setup (Client)
Open a new terminal and navigate to the frontend folder:

Bash

cd frontend
Install node modules:

Bash

npm install --legacy-peer-deps
Start the React app:

Bash

npm start
The app will open at http://localhost:3000

📝 Usage
Type or paste your text into the text area.

Select a voice (Male/Female/Different accents).

Adjust the speed if necessary.

Click Generate Speech.

Listen to the preview or download the MP3 file.

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

📄 License
MIT
