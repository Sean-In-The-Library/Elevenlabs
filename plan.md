 # plan.md
## OU Law ElevenLabs TTS Test Bench — High level plan

### Goal
Build a minimal, OU-Law-branded Streamlit app that lets us:
1) switch between ElevenLabs voices
2) tweak core voice settings
3) generate audio from arbitrary text
4) play and download results, all on one page

### Scope
- Single page Streamlit UI
- Thin Python backend wrapper around the ElevenLabs API
- No persistence of user audio or text beyond the session
- No streaming in v1 (optional in a later phase)

### Deliverables
- `frontend.md` with instructions to generate `app.py` and `.streamlit/config.toml`
- `backend.md` with instructions to generate `eleven_backend.py` and tests
- `requirements.txt` for local run

### Architecture at a glance
- **Frontend (Streamlit)**: Layout with sidebar controls for model, voice, output format, and sliders for voice settings. Main area for text input, Generate button, inline player, and Download button.
- **Backend (Python module)**: Functions to list voices, fetch voice settings, and synthesize speech. All calls authenticated with `xi-api-key`.

### Data flow
1) App loads and reads `ELEVENLABS_API_KEY` from Streamlit secrets or environment.
2) User selects model, voice, output format, and slider values.
3) Frontend sends a `synthesize` request to the backend with text and selected parameters.
4) Backend POSTs to ElevenLabs Text to Speech with `output_format` in the query string and voice settings in the JSON body. 
5) Backend returns raw audio bytes and a MIME hint. 
6) Frontend renders playback using `st.audio` and exposes a Download button.

### UX notes
- Single column layout with a compact header that reads “OU Law TTS Bench (Internal)”.
- Sidebar for models, voices, output format, and settings. Main pane for text and results.
- Brand: use Oklahoma Crimson with neutral grays and white. Do not use Cream in digital UI per OU guidance.

### Configuration
- Secrets: `.streamlit/secrets.toml` contains `ELEVENLABS_API_KEY`. Never commit secrets.
- Theme: `.streamlit/config.toml` sets primary color to OU Crimson and neutral backgrounds.
- Dependencies: `streamlit`, `elevenlabs` SDK or `requests/httpx`, `python-dotenv` optional.

### Backend responsibilities
- `list_voices(page_size=50)` → returns `[{voice_id, name}]`.
- `get_voice_settings(voice_id)` → returns defaults for sliders.
- `synthesize(text, voice_id, model_id, output_format, voice_settings, seed, language_code)` → returns `(audio_bytes, mime)`.

### Frontend responsibilities
- Render controls and validate ranges.
- Cache voice list for a short period with a manual Refresh button.
- Call backend, show spinner, handle errors, and display audio.

### Error handling and logging
- 401 or 403 → surface a clear “API key missing or invalid” error.
- Unknown voice or model → disable Generate and show a brief tip.
- Always allow download if inline playback fails.

### Testing approach
- Unit tests with mocked HTTP for backend functions.
- One optional smoke test that performs a single TTS call when an env flag is set.

### Milestones
- M1: Scaffolding and secrets, static UI, dummy backend stubs.
- M2: Voice list and basic TTS working end to end.
- M3: Settings wiring, caching, download button, OU theme.
- M4 (optional): Add WebSocket streaming in a separate toggle and module.

### Non-goals
- Long-term storage, analytics, or role-based access in v1.
- Voice cloning, dubbing, or speech-to-speech features.

### References (plain URLs)
- ElevenLabs authentication header  
  https://elevenlabs.io/docs/api-reference/authentication
- ElevenLabs Text to Speech create speech  
  https://elevenlabs.io/docs/api-reference/text-to-speech/convert
- ElevenLabs get voice settings  
  https://elevenlabs.io/docs/api-reference/voices/settings/get
- Streamlit audio player  
  https://docs.streamlit.io/develop/api-reference/media/st.audio
- OU design system colors (Cream is print only)  
  https://www.ou.edu/brand/creative-platform/design-system.html