"""
Tests for the audio processor module.
"""
import pytest
import os
import numpy as np
from src.audio.processor import AudioProcessor
from src.audio.task import AudioTask, NoiseReductionLevel
import soundfile as sf
from pydub import AudioSegment

# Test file paths
TEST_FILE = os.path.join(os.path.dirname(__file__), "test.mp3")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "test_cleaned.wav")

def setup_function():
    """Setup function that runs before each test."""
    # Remove output file if it exists
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

def test_audio_processing():
    """Test the complete audio processing pipeline."""
    # Create processor and task
    processor = AudioProcessor()
    task = AudioTask(
        input_path=TEST_FILE,
        noise_reduction_level=NoiseReductionLevel.MEDIUM,
        enable_speech_enhancement=True,
        output_format="wav"  # Use WAV format
    )
    
    # Process audio with progress tracking
    progress_values = []
    def progress_callback(value):
        progress_values.append(value)
        print(f"Progress: {value}%")
    
    # Run processing
    success = processor.process_audio(task, progress_callback)
    
    # Verify processing succeeded
    assert success, "Audio processing failed"
    
    # Verify output file exists
    assert os.path.exists(OUTPUT_FILE), "Output file was not created"
    
    # Verify output file is valid audio
    try:
        y, sr = sf.read(OUTPUT_FILE)
        assert len(y) > 0, "Output audio is empty"
        assert sr > 0, "Invalid sample rate"
    except Exception as e:
        pytest.fail(f"Failed to read output audio: {str(e)}")
    
    # Verify progress tracking
    assert len(progress_values) > 0, "No progress updates received"
    assert progress_values[-1] == 100, "Processing did not complete"
    assert progress_values == sorted(progress_values), "Progress values not monotonically increasing"

def test_noise_reduction_levels():
    """Test different noise reduction levels."""
    processor = AudioProcessor()
    
    for level in NoiseReductionLevel:
        print(f"\nTesting noise reduction level: {level.value}")
        task = AudioTask(
            input_path=TEST_FILE,
            noise_reduction_level=level,
            enable_speech_enhancement=False,
            output_format="wav"  # Use WAV format
        )
        
        success = processor.process_audio(task)
        assert success, f"Processing failed for level {level.value}"
        
        # Verify output exists and is valid
        assert os.path.exists(OUTPUT_FILE), f"Output file not created for level {level.value}"
        os.remove(OUTPUT_FILE)  # Clean up for next iteration

def test_speech_enhancement():
    """Test speech enhancement functionality."""
    processor = AudioProcessor()
    
    # Test with enhancement enabled
    task_with_enhancement = AudioTask(
        input_path=TEST_FILE,
        noise_reduction_level=NoiseReductionLevel.MEDIUM,
        enable_speech_enhancement=True,
        output_format="wav"  # Use WAV format
    )
    
    print("\nTesting with speech enhancement enabled")
    success = processor.process_audio(task_with_enhancement)
    assert success, "Processing failed with speech enhancement"
    
    # Clean up
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

def test_error_handling():
    """Test error handling for invalid inputs."""
    processor = AudioProcessor()
    
    # Test with non-existent file
    task_invalid = AudioTask(
        input_path="nonexistent.mp3",
        noise_reduction_level=NoiseReductionLevel.MEDIUM,
        output_format="wav"  # Use WAV format
    )
    
    print("\nTesting error handling with invalid file")
    success = processor.process_audio(task_invalid)
    assert not success, "Processing should fail with invalid input file"

def test_output_formats():
    """Test different output formats."""
    processor = AudioProcessor()
    
    # Test MP3 output
    print("\nTesting MP3 output format")
    mp3_output = os.path.join(os.path.dirname(__file__), "test_cleaned.mp3")
    task_mp3 = AudioTask(
        input_path=TEST_FILE,
        noise_reduction_level=NoiseReductionLevel.MEDIUM,
        enable_speech_enhancement=False,
        output_format="mp3"
    )
    
    success = processor.process_audio(task_mp3)
    assert success, "Processing failed for MP3 output"
    assert os.path.exists(mp3_output), "MP3 output file was not created"
    
    # Verify MP3 file is valid using pydub
    try:
        audio = AudioSegment.from_mp3(mp3_output)
        assert len(audio) > 0, "MP3 audio is empty"
    except Exception as e:
        pytest.fail(f"Failed to read MP3 output: {str(e)}")
    finally:
        if os.path.exists(mp3_output):
            os.remove(mp3_output)
    
    # Test WAV output
    print("\nTesting WAV output format")
    task_wav = AudioTask(
        input_path=TEST_FILE,
        noise_reduction_level=NoiseReductionLevel.MEDIUM,
        enable_speech_enhancement=False,
        output_format="wav"
    )
    
    success = processor.process_audio(task_wav)
    assert success, "Processing failed for WAV output"
    assert os.path.exists(OUTPUT_FILE), "WAV output file was not created"
    
    # Verify WAV file is valid
    try:
        y, sr = sf.read(OUTPUT_FILE)
        assert len(y) > 0, "WAV audio is empty"
        assert sr > 0, "Invalid sample rate"
    except Exception as e:
        pytest.fail(f"Failed to read WAV output: {str(e)}")
    finally:
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)

if __name__ == "__main__":
    print("Running audio processor tests...")
    pytest.main([__file__, "-v"]) 