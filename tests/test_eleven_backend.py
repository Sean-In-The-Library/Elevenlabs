"""
Unit tests for the ElevenLabs backend module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eleven_backend import get_client, list_voices, get_voice_settings, synthesize, list_models


class TestElevenBackend:
    """Test cases for the ElevenLabs backend module."""
    
    def test_list_models(self):
        """Test that list_models returns expected model data."""
        models = list_models()
        
        assert isinstance(models, list)
        assert len(models) >= 3  # At least the expected models
        
        # Check model structure
        for model in models:
            assert "model_id" in model
            assert "name" in model
            assert isinstance(model["model_id"], str)
            assert isinstance(model["name"], str)
        
        # Check that expected models are present
        model_ids = [model["model_id"] for model in models]
        assert "eleven_flash_v2_5" in model_ids
        assert "eleven_turbo_v2_5" in model_ids
        assert "eleven_multilingual_v2" in model_ids
    
    @patch('eleven_backend.st.secrets')
    @patch('eleven_backend.os.getenv')
    @patch('eleven_backend.ElevenLabs')
    def test_get_client_success(self, mock_elevenlabs, mock_getenv, mock_secrets):
        """Test successful client initialization."""
        # Mock secrets
        mock_secrets.get.return_value = "test-api-key"
        mock_getenv.return_value = None
        
        # Mock ElevenLabs client
        mock_client = Mock()
        mock_elevenlabs.return_value = mock_client
        
        client = get_client()
        
        assert client == mock_client
        mock_elevenlabs.assert_called_once_with(api_key="test-api-key")
    
    @patch('eleven_backend.st.secrets')
    @patch('eleven_backend.os.getenv')
    def test_get_client_no_api_key(self, mock_getenv, mock_secrets):
        """Test client initialization fails when no API key is found."""
        # Mock no secrets or environment variables
        mock_secrets.get.return_value = None
        mock_getenv.return_value = None
        
        with pytest.raises(ValueError, match="ELEVENLABS_API_KEY not found"):
            get_client()
    
    @patch('eleven_backend.st.secrets')
    @patch('eleven_backend.os.getenv')
    def test_get_client_placeholder_key(self, mock_getenv, mock_secrets):
        """Test client initialization fails with placeholder API key."""
        # Mock placeholder key
        mock_secrets.get.return_value = "your-api-key-here"
        mock_getenv.return_value = None
        
        with pytest.raises(ValueError, match="Please set your actual ElevenLabs API key"):
            get_client()
    
    @patch('eleven_backend.get_client')
    def test_list_voices_success(self, mock_get_client):
        """Test successful voice listing."""
        # Mock client
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Mock voices response
        mock_voices_response = Mock()
        mock_voice1 = Mock()
        mock_voice1.voice_id = "voice1"
        mock_voice1.name = "Test Voice 1"
        
        mock_voice2 = Mock()
        mock_voice2.voice_id = "voice2"
        mock_voice2.name = "Test Voice 2"
        
        mock_voices_response.voices = [mock_voice1, mock_voice2]
        mock_client.voices.get_all.return_value = mock_voices_response
        
        voices = list_voices(page_size=50)
        
        assert len(voices) == 2
        assert voices[0]["voice_id"] == "voice1"
        assert voices[0]["name"] == "Test Voice 1"
        assert voices[1]["voice_id"] == "voice2"
        assert voices[1]["name"] == "Test Voice 2"
        
        mock_client.voices.get_all.assert_called_once()
    
    @patch('eleven_backend.get_client')
    def test_list_voices_api_error(self, mock_get_client):
        """Test voice listing fails when API call fails."""
        # Mock client
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Mock API error
        mock_client.voices.get_all.side_effect = Exception("API Error")
        
        with pytest.raises(Exception, match="API Error"):
            list_voices()
    
    @patch('eleven_backend.get_client')
    def test_get_voice_settings_success(self, mock_get_client):
        """Test successful voice settings retrieval."""
        # Mock client
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Mock voices response
        mock_voices_response = Mock()
        
        # Mock voice with settings
        mock_voice = Mock()
        mock_voice.voice_id = "test_voice"
        mock_voice.name = "Test Voice"
        
        # Mock settings
        mock_settings = Mock()
        mock_settings.stability = 0.7
        mock_settings.similarity_boost = 0.8
        mock_settings.style = 0.3
        mock_settings.use_speaker_boost = False
        
        mock_voice.settings = mock_settings
        mock_voices_response.voices = [mock_voice]
        mock_client.voices.get_all.return_value = mock_voices_response
        
        settings = get_voice_settings("test_voice")
        
        assert settings["stability"] == 0.7
        assert settings["similarity_boost"] == 0.8
        assert settings["style"] == 0.3
        assert settings["use_speaker_boost"] == False
    
    @patch('eleven_backend.get_client')
    def test_get_voice_settings_voice_not_found(self, mock_get_client):
        """Test voice settings retrieval fails when voice not found."""
        # Mock client
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Mock empty voice list
        mock_voices_response = Mock()
        mock_voices_response.voices = []
        mock_client.voices.get_all.return_value = mock_voices_response
        
        with pytest.raises(ValueError, match="Voice with ID test_voice not found"):
            get_voice_settings("test_voice")
    
    @patch('eleven_backend.get_client')
    def test_synthesize_success(self, mock_get_client):
        """Test successful speech synthesis."""
        # Mock client
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Mock text-to-speech response
        mock_audio = [b"fake_audio_data"]
        mock_client.text_to_speech.convert.return_value = mock_audio
        
        # Test parameters
        text = "Hello, world!"
        voice_id = "test_voice"
        model_id = "eleven_turbo_v2_5"
        output_format = "mp3_44100_128"
        voice_settings = {
            "stability": 0.7,
            "similarity_boost": 0.8,
            "style": 0.3,
            "use_speaker_boost": False
        }
        
        audio_bytes, mime_type = synthesize(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            output_format=output_format,
            voice_settings=voice_settings,
            speed=1.0
        )
        
        assert audio_bytes == b"fake_audio_data"
        assert mime_type == "audio/mpeg"  # mp3 format
        
        # Verify convert was called with correct parameters
        mock_client.text_to_speech.convert.assert_called_once()
        call_args = mock_client.text_to_speech.convert.call_args
        assert call_args[1]["text"] == text
        assert call_args[1]["voice_id"] == voice_id
        assert call_args[1]["model_id"] == model_id
        assert call_args[1]["output_format"] == output_format
    
    @patch('eleven_backend.get_client')
    def test_synthesize_wav_format(self, mock_get_client):
        """Test speech synthesis with WAV output format."""
        # Mock client
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Mock audio generation
        mock_audio = [b"fake_wav_data"]
        mock_client.text_to_speech.convert.return_value = mock_audio
        
        audio_bytes, mime_type = synthesize(
            text="Test",
            voice_id="test_voice",
            output_format="wav_44100",
            speed=1.0
        )
        
        assert audio_bytes == b"fake_wav_data"
        assert mime_type == "audio/wav"
    
    @patch('eleven_backend.get_client')
    def test_synthesize_api_error(self, mock_get_client):
        """Test speech synthesis fails when API call fails."""
        # Mock client
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Mock API error
        mock_client.text_to_speech.convert.side_effect = Exception("Synthesis failed")
        
        with pytest.raises(Exception, match="Synthesis failed"):
            synthesize("Test", "test_voice", speed=1.0)


if __name__ == "__main__":
    pytest.main([__file__])
