"""
ElevenLabs TTS Backend Module

This module provides a clean interface to the ElevenLabs API for:
- Listing available voices
- Getting voice settings
- Converting text to speech
"""

import os
import logging
from typing import Dict, List, Tuple, Optional, Any
from elevenlabs.client import ElevenLabs
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_client() -> ElevenLabs:
    """
    Initialize and return an ElevenLabs client.
    
    Returns:
        ElevenLabs: Configured client instance
        
    Raises:
        ValueError: If API key is not found
    """
    # Try to get API key from Streamlit secrets first, then environment
    api_key = None
    try:
        api_key = st.secrets.get("ELEVENLABS_API_KEY")
    except:
        pass  # Not running in Streamlit
    
    # If no key from secrets, try environment
    if not api_key:
        api_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not found in secrets or environment variables")
    
    if api_key == "your-api-key-here":
        raise ValueError("Please set your actual ElevenLabs API key in .streamlit/secrets.toml or .env file")
    
    try:
        client = ElevenLabs(api_key=api_key)
        logger.info("ElevenLabs client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize ElevenLabs client: {e}")
        raise


def list_voices(page_size: int = 50) -> List[Dict[str, str]]:
    """
    List available voices from ElevenLabs.
    
    Args:
        page_size (int): Number of voices to return (max 50)
        
    Returns:
        List[Dict[str, str]]: List of voice dictionaries with 'voice_id' and 'name'
        
    Raises:
        Exception: If API call fails
    """
    try:
        elevenlabs_client = get_client()
        voice_list = elevenlabs_client.voices.get_all()
        
        # Convert to expected format
        voices_data = []
        for voice in voice_list.voices[:page_size]:
            voices_data.append({
                "voice_id": voice.voice_id,
                "name": voice.name
            })
        
        logger.info(f"Successfully retrieved {len(voices_data)} voices")
        return voices_data
        
    except Exception as e:
        logger.error(f"Failed to list voices: {e}")
        raise


def get_voice_settings(voice_id: str) -> Dict[str, Any]:
    """
    Get default settings for a specific voice.
    
    Args:
        voice_id (str): The voice ID to get settings for
        
    Returns:
        Dict[str, Any]: Voice settings including stability, similarity_boost, etc.
        
    Raises:
        Exception: If API call fails
    """
    try:
        elevenlabs_client = get_client()
        voice_list = elevenlabs_client.voices.get_all()
        
        # Find the specific voice
        target_voice = None
        for voice in voice_list.voices:
            if voice.voice_id == voice_id:
                target_voice = voice
                break
        
        if not target_voice:
            raise ValueError(f"Voice with ID {voice_id} not found")
        
        # Extract settings
        settings = {
            "stability": getattr(target_voice.settings, 'stability', 0.5),
            "similarity_boost": getattr(target_voice.settings, 'similarity_boost', 0.75),
            "style": getattr(target_voice.settings, 'style', 0.0),
            "use_speaker_boost": getattr(target_voice.settings, 'use_speaker_boost', True)
        }
        
        logger.info(f"Retrieved settings for voice {voice_id}")
        return settings
        
    except Exception as e:
        logger.error(f"Failed to get voice settings for {voice_id}: {e}")
        raise


def synthesize(
    text: str,
    voice_id: str,
    model_id: str = "eleven_turbo_v2_5",
    output_format: str = "mp3_44100_128",
    voice_settings: Optional[Dict[str, Any]] = None,
    seed: Optional[int] = None,
    language_code: Optional[str] = None
) -> Tuple[bytes, str]:
    """
    Convert text to speech using ElevenLabs API.
    
    Args:
        text (str): Text to convert to speech
        voice_id (str): Voice ID to use
        model_id (str): TTS model to use
        output_format (str): Audio output format
        voice_settings (Dict[str, Any], optional): Voice settings overrides
        seed (int, optional): Random seed for consistency
        language_code (str, optional): Language code for multilingual models
        
    Returns:
        Tuple[bytes, str]: Audio bytes and MIME type
        
    Raises:
        Exception: If API call fails
    """
    try:
        elevenlabs_client = get_client()
        
        # Prepare voice settings
        settings = {
            "stability": voice_settings.get("stability", 0.5) if voice_settings else 0.5,
            "similarity_boost": voice_settings.get("similarity_boost", 0.75) if voice_settings else 0.75,
            "style": voice_settings.get("style", 0.0) if voice_settings else 0.0,
            "use_speaker_boost": voice_settings.get("use_speaker_boost", True) if voice_settings else True
        }
        
        # Generate audio
        audio_generator = elevenlabs_client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id=model_id,
            voice_settings=settings,
            output_format=output_format,
            seed=seed,
            language_code=language_code
        )
        
        # Convert generator to bytes
        audio_bytes = b"".join(audio_generator)
        
        # Determine MIME type based on output format
        mime_type = "audio/mpeg" if output_format.startswith("mp3") else "audio/wav"
        
        logger.info(f"Successfully generated audio for text (length: {len(text)})")
        return audio_bytes, mime_type
        
    except Exception as e:
        logger.error(f"Failed to synthesize speech: {e}")
        raise


def list_models() -> List[Dict[str, str]]:
    """
    List available TTS models.
    
    Returns:
        List[Dict[str, str]]: List of model dictionaries with 'model_id' and 'name'
        
    Raises:
        Exception: If API call fails
    """
    # Hardcoded for now - can be enhanced to fetch from API if needed
    models = [
        {"model_id": "eleven_flash_v2_5", "name": "Eleven Flash v2.5 - Lowest Latency"},
        {"model_id": "eleven_turbo_v2_5", "name": "Eleven Turbo v2.5 - Quality/Speed Balance"},
        {"model_id": "eleven_multilingual_v2", "name": "Eleven Multilingual v2 - Highest Quality"}
    ]
    
    logger.info(f"Returned {len(models)} available models")
    return models
