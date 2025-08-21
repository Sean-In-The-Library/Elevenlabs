# frontend.md

## OU Law ElevenLabs Test Bench — Frontend plan (Streamlit)

### Outcome
A single-page Streamlit UI that:
- Lists available ElevenLabs voices and lets the user switch between them
- Lets the user adjust voice settings (stability, similarity, style, speed, speaker boost) and choose a TTS model and output format
- Generates audio from arbitrary text and plays it inline
- Is branded to OU Law using official web color guidance (Oklahoma Crimson #841617; avoid Cream on web)  [oai_citation:0‡University of Oklahoma](https://www.ou.edu/brand/creative-platform/design-system/colors.html)

### Files this plan will produce
- `app.py` — the Streamlit app
- `.streamlit/config.toml` — theme
- `.streamlit/secrets.toml` — local dev secret store for API key (never commit)  [oai_citation:1‡Streamlit Docs](https://docs.streamlit.io/develop/api-reference/connections/secrets.toml?utm_source=chatgpt.com)
- `requirements.txt` — deps

### Dependencies
- `streamlit` for UI and audio component (`st.audio`)  [oai_citation:2‡Streamlit Docs](https://docs.streamlit.io/develop/api-reference/media/st.audio?utm_source=chatgpt.com)
- `elevenlabs` official Python SDK, or fallback to `requests` if you prefer raw HTTP (both supported)  [oai_citation:3‡ElevenLabs](https://elevenlabs.io/docs/api-reference/introduction)
- `python-dotenv` optional for local env loading

### Page config and theme
- In `app.py`, set page config: title "OU Law TTS Bench", layout "wide".
- Create `.streamlit/config.toml` using OU web palette:
  - `primaryColor = "#841617"` (Oklahoma Crimson)
  - `backgroundColor = "#FFFFFF"`
  - `secondaryBackgroundColor = "#F0F0F0"`
  - `textColor = "#000000"`
- Do not use Oklahoma Cream in the digital UI per brand guidance.  [oai_citation:4‡University of Oklahoma](https://www.ou.edu/brand/creative-platform/design-system/colors.html)

### UI layout
- **Header**: OU Law wordmark text (no logo file needed), small caption: “Internal test bench”.
- **Sidebar**:
  - API status chip: show “API key loaded” if present in `st.secrets["ELEVENLABS_API_KEY"]` or `os.environ`.
  - Model radio: `eleven_flash_v2_5`, `eleven_turbo_v2_5`, `eleven_multilingual_v2`. Provide short hints based on docs:
    - Flash v2.5: lowest latency
    - Turbo v2.5: quality-speed balance
    - Multilingual v2: richest long-form quality
    (Model availability can also be fetched from `/v1/models` in backend.)  [oai_citation:5‡ElevenLabs](https://elevenlabs.io/docs/models?utm_source=chatgpt.com)
  - Output format select: at minimum `mp3_22050_32`, `mp3_44100_128`, `wav_44100`. These are valid formats on the TTS endpoint.  [oai_citation:6‡ElevenLabs](https://elevenlabs.io/docs/api-reference/text-to-speech/convert)
  - Voice list controls: Refresh button to requery voices.
- **Main column**:
  1) **Voice chooser**: dropdown from backend `list_voices()` returning `(voice_id, name)`. Uses v2 `/voices` endpoint.  [oai_citation:7‡ElevenLabs](https://elevenlabs.io/docs/api-reference/voices/search)
  2) **Text input**: `st.text_area` with default sample paragraph.
  3) **Voice settings**:
     - `stability` slider [0.0..1.0], step 0.05
     - `similarity_boost` slider [0.0..1.0]
     - `style` slider [0.0..1.0]
     - `speed` slider [0.5..1.5], default 1.0
     - `use_speaker_boost` checkbox
     These map to “voice_settings” on TTS, and are documented in Voice Settings API. Provide simple tooltips summarizing effects.  [oai_citation:8‡ElevenLabs](https://elevenlabs.io/docs/api-reference/voices/settings/get)
  4) **Advanced**:
     - Optional `seed` int to improve repeatability
     - Optional `language_code` for models that support language enforcement (note that only some models accept it)  [oai_citation:9‡ElevenLabs](https://elevenlabs.io/docs/api-reference/text-to-speech/convert)
  5) **Generate** button: calls backend `synthesize()`; shows spinner.
  6) **Playback**: render audio bytes with `st.audio(..., format="audio/mp3")` or wav depending on chosen output format.  [oai_citation:10‡Streamlit Docs](https://docs.streamlit.io/develop/api-reference/media/st.audio?utm_source=chatgpt.com)
  7) **Download**: `st.download_button` to save the generated audio.

### Client-backend contract
- `list_voices(page_size=50)` → `List[{"voice_id", "name"}]`
- `get_default_settings(voice_id)` → `{"stability","similarity_boost","style","speed","use_speaker_boost"}`
- `synthesize(payload)` → `{"audio_bytes": bytes, "mime": "audio/mpeg" or "audio/wav", "request_id": str}`
- `list_models()` optional to populate model select with real data

### State and caching
- Cache voices for 10 minutes with `@st.cache_data` and manual "Refresh" to avoid rate or credit waste.  [oai_citation:11‡Streamlit Docs](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_data?utm_source=chatgpt.com)
- Persist last-used settings in `st.session_state`.

### Error handling UX
- Show `st.error` for HTTP 401/403 (missing or invalid key).
- Show concise validation hints if sliders out of range.
- If API returns bytes but playback fails, present a link to download anyway.

### Definition of done
- App loads with no secrets in repo
- With valid `ELEVENLABS_API_KEY`, the app lists voices, generates audio, plays it inline, and allows download
- Settings adjust audible output as expected
- OU branding applied per web guidance, no Cream used