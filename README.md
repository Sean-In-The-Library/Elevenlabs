# OU Law ElevenLabs TTS Test Bench

A Streamlit-based test bench application for experimenting with ElevenLabs text-to-speech capabilities, branded for OU Law use.

## 🎯 Features

- **Voice Selection**: Browse and select from available ElevenLabs voices
- **Model Options**: Choose between Flash (fast), Turbo (balanced), and Multilingual (quality) models
- **Voice Settings**: Fine-tune stability, similarity boost, style, and speed
- **Audio Formats**: Support for MP3 and WAV output formats
- **Real-time Generation**: Convert text to speech with live preview
- **Download Support**: Save generated audio files locally
- **OU Branding**: Consistent with OU Law visual identity

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- ElevenLabs API key ([Get one here](https://elevenlabs.io/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Elevenlabs
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key**
   
   **Option A: Streamlit secrets (recommended)**
   ```bash
   # Edit .streamlit/secrets.toml
   ELEVENLABS_API_KEY = "your-actual-api-key-here"
   ```
   
   **Option B: Environment variable**
   ```bash
   export ELEVENLABS_API_KEY="your-actual-api-key-here"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 🏗️ Architecture

### Backend (`eleven_backend.py`)
- **Client Management**: Handles ElevenLabs API authentication
- **Voice Operations**: Lists voices and retrieves default settings
- **TTS Engine**: Converts text to speech with configurable parameters
- **Error Handling**: Comprehensive error handling and logging

### Frontend (`app.py`)
- **Streamlit UI**: Single-page application with sidebar controls
- **State Management**: Caches voice lists and persists user preferences
- **Audio Playback**: Inline audio player with download functionality
- **Responsive Design**: Mobile-friendly layout with OU branding

### Configuration
- **Theme**: OU Crimson (#841617) with neutral backgrounds
- **Secrets**: Secure API key management via Streamlit secrets
- **Caching**: 10-minute TTL for voice lists to minimize API calls

## 🎛️ Usage

### Basic Workflow

1. **Select Model**: Choose your preferred TTS model
2. **Pick Voice**: Select from available ElevenLabs voices
3. **Adjust Settings**: Fine-tune voice parameters as needed
4. **Enter Text**: Type or paste your text content
5. **Generate**: Click "Generate Speech" to create audio
6. **Play & Download**: Listen inline and download the file

### Voice Settings

- **Stability** (0.0-1.0): Higher values = more consistent voice
- **Similarity Boost** (0.0-1.0): Higher values = more similar to original
- **Style** (0.0-1.0): Higher values = more expressive
- **Speed** (0.5-1.5): Speech rate multiplier
- **Speaker Boost**: Enhances speaker clarity

### Advanced Options

- **Seed**: Set for reproducible results
- **Language Code**: Force specific language (model-dependent)
- **Output Format**: Choose audio quality and file size

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

Or run individual tests:

```bash
python -m pytest tests/test_eleven_backend.py -v
```

## 🔧 Configuration

### Environment Variables

- `ELEVENLABS_API_KEY`: Your ElevenLabs API key

### Streamlit Configuration

- **Port**: 8501 (configurable in `.streamlit/config.toml`)
- **Theme**: OU branding colors
- **Layout**: Wide layout with expanded sidebar

## 🚨 Troubleshooting

### Common Issues

1. **"API key not found"**
   - Ensure `ELEVENLABS_API_KEY` is set in secrets or environment
   - Check that the key is valid and active

2. **"No voices available"**
   - Verify API key permissions
   - Check ElevenLabs service status
   - Try refreshing the voice list

3. **Audio playback issues**
   - Check browser audio support
   - Verify output format compatibility
   - Try downloading the file instead

4. **Generation failures**
   - Check text length limits
   - Verify voice and model compatibility
   - Review API rate limits

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📁 Project Structure

```
Elevenlabs/
├── app.py                 # Main Streamlit application
├── eleven_backend.py      # ElevenLabs API wrapper
├── requirements.txt       # Python dependencies
├── .streamlit/
│   ├── config.toml       # Streamlit configuration
│   └── secrets.toml      # API keys (template)
├── tests/
│   └── test_eleven_backend.py  # Unit tests
├── plan.md               # Project planning document
├── frontend.md           # Frontend specifications
├── backend.md            # Backend specifications
├── progress.md           # Development progress log
└── README.md             # This file
```

## 🔒 Security Notes

- **Never commit API keys** to version control
- **Use environment variables** or Streamlit secrets for sensitive data
- **Validate user inputs** to prevent injection attacks
- **Monitor API usage** to stay within rate limits

## 📚 API Reference

### Backend Functions

- `get_client()` → ElevenLabs client instance
- `list_voices(page_size=50)` → List of available voices
- `get_voice_settings(voice_id)` → Default settings for a voice
- `synthesize(text, voice_id, ...)` → Audio bytes and MIME type
- `list_models()` → Available TTS models

### ElevenLabs Endpoints

- [Authentication](https://elevenlabs.io/docs/api-reference/authentication)
- [Text-to-Speech](https://elevenlabs.io/docs/api-reference/text-to-speech/convert)
- [Voice Settings](https://elevenlabs.io/docs/api-reference/voices/settings/get)

## 🤝 Contributing

1. Follow the existing code style
2. Add tests for new functionality
3. Update documentation as needed
4. Test thoroughly before submitting

## 📄 License

This project is for internal OU Law use only.

## 🆘 Support

For technical issues:
1. Check the troubleshooting section
2. Review ElevenLabs API documentation
3. Check Streamlit documentation
4. Contact the development team

---

**Last Updated**: Initial release  
**Version**: 1.0.0  
**Status**: Development Phase 1 Complete
