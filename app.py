"""
OU Law ElevenLabs TTS Test Bench

A Streamlit application for testing and experimenting with ElevenLabs text-to-speech
capabilities using OU Law branding.
"""

import streamlit as st
import os
from typing import Dict, Any, Optional
from eleven_backend import (
    list_voices, 
    get_voice_settings, 
    synthesize, 
    list_models
)

# Page configuration
st.set_page_config(
    page_title="OU Law TTS Bench",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for OU branding
st.markdown("""
<style>
    .main-header {
        color: #841617;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #666;
        font-size: 1rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background-color: #841617;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #6b1214;
    }
    .sidebar .sidebar-content {
        background-color: #F0F0F0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">OU Law TTS Bench</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Internal test bench for ElevenLabs text-to-speech</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Controls")
        
        # API Status
        st.write("🔍 Debug: Testing API connection...")
        st.write(f"🔍 Debug: Environment ELEVENLABS_API_KEY: {os.getenv('ELEVENLABS_API_KEY', 'NOT_SET')[:10] if os.getenv('ELEVENLABS_API_KEY') else 'NOT_SET'}...")
        st.write(f"🔍 Debug: Streamlit secrets ELEVENLABS_API_KEY: {st.secrets.get('ELEVENLABS_API_KEY', 'NOT_SET')[:10] if st.secrets.get('ELEVENLABS_API_KEY') else 'NOT_SET'}...")
        try:
            # Try to get a voice to test API connectivity
            st.write("🔍 Debug: Calling list_voices...")
            voices = list_voices(page_size=1)
            st.write(f"🔍 Debug: Got {len(voices) if voices else 0} voices")
            if voices:
                st.success("✅ API connected - voices available")
            else:
                st.warning("⚠️ API connected but no voices found")
        except Exception as e:
            st.error("❌ API connection failed")
            st.info("Check ELEVENLABS_API_KEY in .streamlit/secrets.toml or .env file")
            st.code(str(e))
            st.write(f"🔍 Debug: Exception type: {type(e).__name__}")
            st.write(f"🔍 Debug: Exception details: {e}")
        
        # Model Selection
        st.subheader("Model")
        models = list_models()
        model_options = {model["name"]: model["model_id"] for model in models}
        selected_model_name = st.selectbox(
            "Select TTS Model",
            options=list(model_options.keys()),
            index=1,  # Default to Turbo v2.5
            help="Choose the TTS model based on your needs"
        )
        selected_model_id = model_options[selected_model_name]
        
        # Output Format
        st.subheader("Output Format")
        output_format = st.selectbox(
            "Audio Format",
            options=[
                "mp3_22050_32",
                "mp3_44100_128", 
                "wav_44100"
            ],
            index=1,  # Default to mp3_44100_128
            help="Audio quality and file size trade-offs"
        )
        
        # Voice List Controls
        st.subheader("Voices")
        if st.button("🔄 Refresh Voices", help="Reload available voices from ElevenLabs"):
            st.cache_data.clear()
            st.rerun()
        
        # Get voices with caching
        @st.cache_data(ttl=600)  # Cache for 10 minutes
        def get_cached_voices():
            try:
                return list_voices(page_size=50)
            except Exception as e:
                st.error(f"Failed to load voices: {e}")
                return []
        
        voices = get_cached_voices()
        
        if voices:
            voice_options = {voice["name"]: voice["voice_id"] for voice in voices}
            selected_voice_name = st.selectbox(
                "Select Voice",
                options=list(voice_options.keys()),
                help="Choose from available ElevenLabs voices"
            )
            selected_voice_id = voice_options[selected_voice_name]
        else:
            st.warning("No voices available")
            return
        
        # Voice Settings
        st.subheader("Voice Settings")
        
        # Get default settings for selected voice
        try:
            default_settings = get_voice_settings(selected_voice_id)
        except Exception as e:
            st.error(f"Failed to get voice settings: {e}")
            default_settings = {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True
            }
        
        stability = st.slider(
            "Stability",
            min_value=0.0,
            max_value=1.0,
            value=default_settings.get("stability", 0.5),
            step=0.05,
            help="Higher values = more consistent voice, lower = more expressive"
        )
        
        similarity_boost = st.slider(
            "Similarity Boost",
            min_value=0.0,
            max_value=1.0,
            value=default_settings.get("similarity_boost", 0.75),
            step=0.05,
            help="Higher values = more similar to original voice"
        )
        
        style = st.slider(
            "Style",
            min_value=0.0,
            max_value=1.0,
            value=default_settings.get("style", 0.0),
            step=0.05,
            help="Higher values = more expressive and emotional"
        )
        
        speed = st.slider(
            "Speed",
            min_value=0.5,
            max_value=1.5,
            value=1.0,
            step=0.1,
            help="Speech rate multiplier"
        )
        
        use_speaker_boost = st.checkbox(
            "Speaker Boost",
            value=default_settings.get("use_speaker_boost", True),
            help="Enhance speaker clarity"
        )
        
        # Advanced Settings
        with st.expander("Advanced Settings"):
            seed = st.number_input(
                "Seed (for consistency)",
                min_value=0,
                max_value=999999,
                value=None,
                help="Optional: Set for reproducible results"
            )
            
            language_code = st.text_input(
                "Language Code",
                value="",
                help="Optional: Force specific language (e.g., 'en', 'es')"
            )
    
    # Main Content Area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Text Input")
        
        # Sample text
        sample_text = """Welcome to the OU Law TTS Test Bench. This is a sample text that demonstrates the text-to-speech capabilities of ElevenLabs. You can replace this with any text you'd like to convert to speech."""
        
        text_input = st.text_area(
            "Enter text to convert to speech",
            value=sample_text,
            height=150,
            placeholder="Type or paste your text here..."
        )
        
        if not text_input.strip():
            st.warning("Please enter some text to convert to speech")
            return
        
        # Generate button
        if st.button("🎙️ Generate Speech", type="primary", use_container_width=True):
            if not text_input.strip():
                st.error("Please enter some text")
                return
            
            try:
                with st.spinner("Generating speech..."):
                    # Prepare voice settings
                    voice_settings = {
                        "stability": stability,
                        "similarity_boost": similarity_boost,
                        "style": style,
                        "use_speaker_boost": use_speaker_boost
                    }
                    
                    # Generate audio
                    audio_bytes, mime_type = synthesize(
                        text=text_input,
                        voice_id=selected_voice_id,
                        model_id=selected_model_id,
                        output_format=output_format,
                        voice_settings=voice_settings,
                        seed=seed if seed is not None else None,
                        language_code=language_code if language_code.strip() else None,
                        speed=speed
                    )
                    
                    st.success("✅ Speech generated successfully!")
                    
                    # Store in session state for download
                    st.session_state.audio_bytes = audio_bytes
                    st.session_state.mime_type = mime_type
                    st.session_state.output_format = output_format
                    
            except Exception as e:
                st.error(f"Failed to generate speech: {e}")
                st.info("Check your API key and try again")
    
    with col2:
        st.header("🎵 Playback")
        
        # Audio player
        if hasattr(st.session_state, 'audio_bytes') and st.session_state.audio_bytes:
            st.audio(
                st.session_state.audio_bytes,
                format=st.session_state.mime_type
            )
            
            # Download button
            file_extension = "mp3" if output_format.startswith("mp3") else "wav"
            filename = f"ou_law_tts_output.{file_extension}"
            
            st.download_button(
                label="💾 Download Audio",
                data=st.session_state.audio_bytes,
                file_name=filename,
                mime=st.session_state.mime_type,
                use_container_width=True
            )
            
            # Audio info
            st.info(f"Format: {output_format}\nSize: {len(st.session_state.audio_bytes):,} bytes")
        else:
            st.info("Generate speech to see the audio player here")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>OU Law TTS Test Bench - Internal Use Only</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
