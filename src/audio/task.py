"""
Audio task management module.
"""
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

class NoiseReductionLevel(Enum):
    """Noise reduction intensity levels."""
    LIGHT = "light"
    MEDIUM = "medium"
    STRONG = "strong"

class SpeechEnhancementLevel(Enum):
    """Speech enhancement intensity levels."""
    LIGHT = "light"
    MEDIUM = "medium"
    STRONG = "strong"

class BackgroundNoiseLevel(Enum):
    """Background noise suppression levels."""
    MINIMAL = "minimal"  # Preserve some background noise for natural sound
    MODERATE = "moderate"  # Balance between noise reduction and natural sound
    AGGRESSIVE = "aggressive"  # Maximum noise reduction

@dataclass
class AudioTask:
    """Represents an audio processing task."""
    input_path: str
    name: str = ""
    noise_reduction_level: NoiseReductionLevel = NoiseReductionLevel.MEDIUM
    enable_speech_enhancement: bool = True
    speech_enhancement_level: SpeechEnhancementLevel = SpeechEnhancementLevel.MEDIUM
    voice_clarity_boost: bool = True
    background_noise_level: BackgroundNoiseLevel = BackgroundNoiseLevel.MODERATE
    
    def __post_init__(self):
        """Initialize task name from input path if not provided."""
        if not self.name:
            self.name = Path(self.input_path).stem
            
    @property
    def output_path(self) -> str:
        """Generate output path based on input path."""
        input_path = Path(self.input_path)
        return str(input_path.parent / f"{input_path.stem}_cleaned{input_path.suffix}")
        
    @property
    def output_format(self) -> str:
        """Get the output format based on input file extension."""
        input_path = Path(self.input_path)
        ext = input_path.suffix.lower()
        
        # Map of input extensions to output formats
        format_map = {
            '.wav': 'wav',
            '.mp3': 'mp3',
            '.m4a': 'm4a',
            '.aac': 'aac',
            '.ogg': 'ogg',
            '.flac': 'flac'
        }
        
        # If input format is supported, use the same format
        if ext in format_map:
            return format_map[ext]
            
        # For unsupported formats, use WAV as default (lossless)
        return 'wav' 