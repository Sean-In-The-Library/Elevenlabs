#!/usr/bin/env python3
"""
Integration test script for ElevenLabs backend functions.

This script tests the real API integration to validate that our backend
functions work correctly with the actual ElevenLabs service.

Usage:
    python3 test_integration.py
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
sys.path.insert(0, current_dir)

from eleven_backend import get_client, list_voices, get_voice_settings, synthesize, list_models


def test_api_connection():
    """Test basic API connection and authentication."""
    print("🔐 Testing API connection...")
    
    try:
        client = get_client()
        print("✅ API connection successful")
        return client
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return None


def test_list_voices(client):
    """Test voice listing with real API."""
    print("\n🎭 Testing voice listing...")
    
    try:
        voices = list_voices(page_size=10)  # Limit to 10 for testing
        
        if voices:
            print(f"✅ Successfully retrieved {len(voices)} voices:")
            for i, voice in enumerate(voices[:5], 1):  # Show first 5
                print(f"   {i}. {voice['name']} (ID: {voice['voice_id'][:8]}...)")
            
            if len(voices) > 5:
                print(f"   ... and {len(voices) - 5} more voices")
            
            return voices[0] if voices else None  # Return first voice for further testing
        else:
            print("❌ No voices returned")
            return None
            
    except Exception as e:
        print(f"❌ Voice listing failed: {e}")
        return None


def test_voice_settings(client, voice_id):
    """Test voice settings retrieval with real API."""
    print(f"\n⚙️ Testing voice settings for voice ID: {voice_id[:8]}...")
    
    try:
        settings = get_voice_settings(voice_id)
        
        if settings:
            print("✅ Successfully retrieved voice settings:")
            for key, value in settings.items():
                print(f"   {key}: {value}")
            return settings
        else:
            print("❌ No voice settings returned")
            return None
            
    except Exception as e:
        print(f"❌ Voice settings retrieval failed: {e}")
        return None


def test_tts_generation(client, voice_id, voice_settings):
    """Test text-to-speech generation with real API."""
    print(f"\n🎙️ Testing TTS generation...")
    
    test_text = "Hello! This is a test of the ElevenLabs text-to-speech integration."
    
    try:
        audio_bytes, mime_type = synthesize(
            text=test_text,
            voice_id=voice_id,
            model_id="eleven_turbo_v2_5",  # Use a reliable model
            output_format="mp3_44100_128",
            voice_settings=voice_settings
        )
        
        if audio_bytes and mime_type:
            print(f"✅ TTS generation successful!")
            print(f"   Audio size: {len(audio_bytes):,} bytes")
            print(f"   MIME type: {mime_type}")
            print(f"   Text length: {len(test_text)} characters")
            
            # Save a small test file
            with open("test_output.mp3", "wb") as f:
                f.write(audio_bytes)
            print("   💾 Test audio saved as 'test_output.mp3'")
            
            return True
        else:
            print("❌ TTS generation returned empty data")
            return False
            
    except Exception as e:
        print(f"❌ TTS generation failed: {e}")
        return False


def test_models():
    """Test model listing."""
    print("\n🤖 Testing model listing...")
    
    try:
        models = list_models()
        
        if models:
            print(f"✅ Successfully retrieved {len(models)} models:")
            for model in models:
                print(f"   - {model['name']} (ID: {model['model_id']})")
            return True
        else:
            print("❌ No models returned")
            return False
            
    except Exception as e:
        print(f"❌ Model listing failed: {e}")
        return False


def main():
    """Run all integration tests."""
    print("🚀 Starting ElevenLabs Backend Integration Tests")
    print("=" * 50)
    
    # Test API connection
    client = test_api_connection()
    if not client:
        print("\n❌ Cannot proceed without API connection")
        return False
    
    # Test models
    models_ok = test_models()
    
    # Test voice listing
    first_voice = test_list_voices(client)
    if not first_voice:
        print("\n❌ Cannot proceed without voice data")
        return False
    
    # Test voice settings
    voice_settings = test_voice_settings(client, first_voice['voice_id'])
    if not voice_settings:
        print("\n❌ Cannot proceed without voice settings")
        return False
    
    # Test TTS generation
    tts_ok = test_tts_generation(client, first_voice['voice_id'], voice_settings)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Integration Test Summary")
    print("=" * 50)
    
    tests = [
        ("API Connection", client is not None),
        ("Model Listing", models_ok),
        ("Voice Listing", first_voice is not None),
        ("Voice Settings", voice_settings is not None),
        ("TTS Generation", tts_ok)
    ]
    
    passed = 0
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All integration tests passed! Backend is ready for production use.")
        return True
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
