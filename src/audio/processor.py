"""
Audio processing module.
"""
import librosa
import soundfile as sf
import noisereduce as nr
import numpy as np
import traceback
import logging
from typing import List, Callable, Optional
from pydub import AudioSegment
import io
from .task import AudioTask, NoiseReductionLevel

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AudioProcessor:
    """Handles audio processing operations."""
    
    def __init__(self):
        """Initialize the audio processor."""
        self.is_processing = False
        
    def process_audio(self, task: AudioTask, progress_callback: Optional[Callable[[int], None]] = None) -> bool:
        """Process a single audio task with progress updates.
        
        Args:
            task: The audio task to process
            progress_callback: Optional callback function to report progress (0-100)
            
        Returns:
            bool: True if processing was successful, False otherwise
        """
        try:
            logger.info(f"Starting to process task: {task.name}")
            logger.info(f"Input path: {task.input_path}")
            logger.info(f"Output path: {task.output_path}")
            logger.info(f"Noise reduction level: {task.noise_reduction_level}")
            logger.info(f"Speech enhancement enabled: {task.enable_speech_enhancement}")
            logger.info(f"Output format: {task.output_format}")
            
            # Load audio file
            if progress_callback:
                progress_callback(10)
            logger.debug("Loading audio file...")
            try:
                y, sr = librosa.load(task.input_path, sr=None)
                logger.debug(f"Audio loaded successfully. Shape: {y.shape}, Sample rate: {sr}")
            except Exception as e:
                logger.error(f"Failed to load audio file: {str(e)}")
                logger.error(traceback.format_exc())
                raise
            
            # Apply noise reduction
            if progress_callback:
                progress_callback(30)
            logger.debug("Applying noise reduction...")
            try:
                y_clean = self._apply_noise_reduction(y, sr, task.noise_reduction_level)
                logger.debug(f"Noise reduction completed. Output shape: {y_clean.shape}")
            except Exception as e:
                logger.error(f"Failed to apply noise reduction: {str(e)}")
                logger.error(traceback.format_exc())
                raise
            
            # Apply speech enhancement if enabled
            if task.enable_speech_enhancement:
                if progress_callback:
                    progress_callback(60)
                logger.debug("Applying speech enhancement...")
                try:
                    y_clean = self._enhance_speech(y_clean, sr)
                    logger.debug("Speech enhancement completed")
                except Exception as e:
                    logger.error(f"Failed to apply speech enhancement: {str(e)}")
                    logger.error(traceback.format_exc())
                    raise
            
            # Save processed audio
            if progress_callback:
                progress_callback(80)
            logger.debug(f"Saving processed audio to {task.output_path}")
            try:
                if task.output_format.lower() == 'mp3':
                    # For MP3 output, we need to:
                    # 1. Save as WAV to a buffer
                    # 2. Convert to MP3 using pydub
                    wav_buffer = io.BytesIO()
                    sf.write(wav_buffer, y_clean, sr, format='WAV')
                    wav_buffer.seek(0)
                    
                    # Convert to MP3
                    audio_segment = AudioSegment.from_wav(wav_buffer)
                    audio_segment.export(task.output_path, format='mp3')
                else:
                    # Direct WAV output
                    sf.write(task.output_path, y_clean, sr)
                logger.debug("Audio saved successfully")
            except Exception as e:
                logger.error(f"Failed to save audio file: {str(e)}")
                logger.error(traceback.format_exc())
                raise
            
            if progress_callback:
                progress_callback(100)
            logger.info(f"Task {task.name} completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error processing task {task.name}: {str(e)}")
            logger.error(traceback.format_exc())
            return False
        
    def process_tasks(self, tasks: List[AudioTask]) -> None:
        """Process a list of audio tasks."""
        self.is_processing = True
        for task in tasks:
            if not self.is_processing:
                break
            self._process_task(task)
            
    def stop_processing(self) -> None:
        """Stop the current processing operation."""
        self.is_processing = False
        
    def _process_task(self, task: AudioTask) -> None:
        """Process a single audio task."""
        try:
            # Load audio file
            y, sr = librosa.load(task.input_path, sr=None)
            
            # Apply noise reduction
            y_clean = self._apply_noise_reduction(y, sr, task.noise_reduction_level)
            
            # Apply speech enhancement if enabled
            if task.enable_speech_enhancement:
                y_clean = self._enhance_speech(y_clean, sr)
                
            # Save processed audio
            sf.write(task.output_path, y_clean, sr)
            
        except Exception as e:
            print(f"Error processing {task.name}: {str(e)}")
            
    def _apply_noise_reduction(self, y: np.ndarray, sr: int, level: NoiseReductionLevel) -> np.ndarray:
        """Apply noise reduction to audio signal."""
        try:
            # Convert noise reduction level to reduction strength
            reduction_strength = {
                NoiseReductionLevel.LIGHT: 0.5,
                NoiseReductionLevel.MEDIUM: 0.7,
                NoiseReductionLevel.STRONG: 0.9
            }[level]
            
            # Estimate noise from the first second of audio
            noise_clip = y[:sr]
            logger.debug(f"Using noise profile of length: {len(noise_clip)}")
            logger.debug(f"Input signal shape: {y.shape}, Sample rate: {sr}")
            
            # Apply noise reduction using noisereduce's current API
            return nr.reduce_noise(
                y=y,
                sr=sr,
                y_noise=noise_clip,
                prop_decrease=reduction_strength,
                stationary=True,
                n_std_thresh_stationary=1.5
            )
                
        except Exception as e:
            logger.error(f"Error in noise reduction: {str(e)}")
            logger.error(traceback.format_exc())
            raise
            
    def _enhance_speech(self, y: np.ndarray, sr: int) -> np.ndarray:
        """Apply speech enhancement to audio signal."""
        try:
            logger.debug("Speech enhancement called (currently a placeholder)")
            # TODO: Implement VoiceFixer integration
            return y
        except Exception as e:
            logger.error(f"Error in speech enhancement: {str(e)}")
            logger.error(traceback.format_exc())
            raise 