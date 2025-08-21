# backend.md

## ElevenLabs backend plan (Python)

### Outcome
A small Python module the frontend calls to:
- Authenticate with ElevenLabs using `xi-api-key` header or the official SDK
- List voices with the v2 endpoint
- Fetch default voice settings
- Convert text to speech with overrideable `voice_settings`, `model_id`, and `output_format` query param
References for endpoints and fields are from ElevenLabs API docs: https://elevenlabs.io/docs/api-reference/authentication
### Files this plan will produce
- `eleven_backend.py` — functions listed below
- `tests/test_eleven_backend.py` — minimal functional tests using a mocked HTTP client
- `requirements.txt` — include `elevenlabs` and `httpx` or `requests`

### Configuration and secrets
- Expect `ELEVENLABS_API_KEY` from `st.secrets` or environment. Do not print it. Streamlit secrets TOML is supported for local dev and Streamlit Cloud deployment.  [oai_citation:13‡Streamlit Docs](https://docs.streamlit.io/develop/concepts/connections/secrets-management?utm_source=chatgpt.com)

### Functions to implement

1) `get_client()`
- If using SDK:
  ```python
  from elevenlabs.client import ElevenLabs
  client = ElevenLabs(api_key=API_KEY)