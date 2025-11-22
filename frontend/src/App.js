import { useState, useRef, useEffect } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Download, Play, Pause, Volume2, Loader2 } from "lucide-react";
import { toast } from "sonner";

const BACKEND_URL = "http://127.0.0.1:8000";
const API = `${BACKEND_URL}/api`;

const VoiceFlowApp = () => {
  const [text, setText] = useState("");
  const [voice, setVoice] = useState("alloy");
  const [speed, setSpeed] = useState([1.0]);
  const [loading, setLoading] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [voices, setVoices] = useState([]);
  const [audioProgress, setAudioProgress] = useState(0);
  const audioRef = useRef(null);

  useEffect(() => {
    fetchVoices();
  }, []);

  const fetchVoices = async () => {
    try {
      const response = await axios.get(`${API}/voices`);
      setVoices(response.data.voices);
    } catch (error) {
      console.error("Failed to fetch voices", error);
    }
  };

  const generateSpeech = async () => {
    if (!text.trim()) {
      toast.error("Please enter some text");
      return;
    }

    if (text.length > 4096) {
      toast.error("Text is too long. Maximum 4096 characters.");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API}/generate-speech`, {
        text,
        voice,
        speed: speed[0],
        model: "tts-1"
      });

      const audioBase64 = response.data.audio_base64;
      const audioBlob = base64ToBlob(audioBase64, "audio/mp3");
      const url = URL.createObjectURL(audioBlob);
      setAudioUrl(url);
      toast.success("Speech generated successfully!");
    } catch (error) {
      console.error("Speech generation failed", error);
      toast.error(error.response?.data?.detail || "Failed to generate speech");
    } finally {
      setLoading(false);
    }
  };

  const base64ToBlob = (base64, type) => {
    const byteCharacters = atob(base64);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type });
  };

  const togglePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const downloadAudio = () => {
    if (audioUrl) {
      const a = document.createElement("a");
      a.href = audioUrl;
      a.download = `voiceflow_${Date.now()}.mp3`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      toast.success("Audio downloaded!");
    }
  };

  useEffect(() => {
    const audio = audioRef.current;
    if (audio) {
      const updateProgress = () => {
        if (audio.duration) {
          setAudioProgress((audio.currentTime / audio.duration) * 100);
        }
      };
      const handleEnded = () => setIsPlaying(false);
      
      audio.addEventListener("timeupdate", updateProgress);
      audio.addEventListener("ended", handleEnded);
      
      return () => {
        audio.removeEventListener("timeupdate", updateProgress);
        audio.removeEventListener("ended", handleEnded);
      };
    }
  }, [audioUrl]);

  return (
    <div className="voice-flow-container">
      <div className="voice-flow-content">
        <div className="header-section">
          <div className="icon-wrapper">
            <Volume2 className="header-icon" />
          </div>
          <h1 className="app-title">VoiceFlow</h1>
          <p className="app-subtitle">Transform your text into natural, expressive speech</p>
        </div>

        <div className="main-card">
          <div className="input-section">
            <Label htmlFor="text-input" className="input-label">Your Text</Label>
            <Textarea
              id="text-input"
              data-testid="text-input"
              placeholder="Enter the text you want to convert to speech..."
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="text-area"
              rows={6}
              maxLength={4096}
            />
            <div className="char-count">{text.length} / 4096 characters</div>
          </div>

          <div className="controls-grid">
            <div className="control-item">
              <Label className="control-label">Voice Style</Label>
              <Select value={voice} onValueChange={setVoice}>
                <SelectTrigger data-testid="voice-select" className="select-trigger">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {voices.map((v) => (
                    <SelectItem key={v.id} value={v.id} data-testid={`voice-option-${v.id}`}>
                      <div className="voice-option">
                        <span className="voice-name">{v.name}</span>
                        <span className="voice-desc">{v.description}</span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="control-item">
              <Label className="control-label">
                Speed: {speed[0].toFixed(2)}x
              </Label>
              <Slider
                data-testid="speed-slider"
                value={speed}
                onValueChange={setSpeed}
                min={0.25}
                max={4.0}
                step={0.25}
                className="speed-slider"
              />
              <div className="speed-markers">
                <span>0.25x</span>
                <span>2x</span>
                <span>4x</span>
              </div>
            </div>
          </div>

          <Button
            data-testid="generate-button"
            onClick={generateSpeech}
            disabled={loading || !text.trim()}
            className="generate-button"
            size="lg"
          >
            {loading ? (
              <>
                <Loader2 className="button-icon animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Volume2 className="button-icon" />
                Generate Speech
              </>
            )}
          </Button>

          {audioUrl && (
            <div className="audio-player-section">
              <div className="audio-visualizer">
                <div className="progress-bar" style={{ width: `${audioProgress}%` }} />
              </div>
              
              <div className="player-controls">
                <Button
                  data-testid="play-pause-button"
                  onClick={togglePlayPause}
                  className="control-btn"
                  size="icon"
                  variant="outline"
                >
                  {isPlaying ? <Pause className="icon" /> : <Play className="icon" />}
                </Button>
                
                <Button
                  data-testid="download-button"
                  onClick={downloadAudio}
                  className="control-btn"
                  size="icon"
                  variant="outline"
                >
                  <Download className="icon" />
                </Button>
              </div>
              
              <audio ref={audioRef} src={audioUrl} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<VoiceFlowApp />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;