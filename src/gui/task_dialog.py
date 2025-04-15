"""
Task configuration dialog implementation.
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QCheckBox, QPushButton, QFileDialog,
    QLineEdit, QGroupBox
)
from audio.task import (
    NoiseReductionLevel,
    SpeechEnhancementLevel,
    BackgroundNoiseLevel
)

class TaskDialog(QDialog):
    """Dialog for configuring audio processing tasks."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Audio Task")
        self.setMinimumWidth(400)
        
        # Create layout
        layout = QVBoxLayout()
        
        # File selection
        file_layout = QHBoxLayout()
        file_label = QLabel("Audio File:")
        self.file_path = QLineEdit()
        self.file_path.setReadOnly(True)
        self.browse_button = QPushButton("Browse...")
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(self.browse_button)
        layout.addLayout(file_layout)
        
        # Noise reduction settings
        noise_group = QGroupBox("Noise Reduction")
        noise_layout = QVBoxLayout()
        
        noise_level_layout = QHBoxLayout()
        noise_label = QLabel("Reduction Level:")
        self.noise_combo = QComboBox()
        self.noise_combo.addItems([level.value for level in NoiseReductionLevel])
        self.noise_combo.setCurrentText(NoiseReductionLevel.MEDIUM.value)
        noise_level_layout.addWidget(noise_label)
        noise_level_layout.addWidget(self.noise_combo)
        noise_layout.addLayout(noise_level_layout)
        
        noise_group.setLayout(noise_layout)
        layout.addWidget(noise_group)
        
        # Speech enhancement settings
        speech_group = QGroupBox("Speech Enhancement")
        speech_layout = QVBoxLayout()
        
        # Enable/disable speech enhancement
        self.speech_check = QCheckBox("Enable Speech Enhancement")
        self.speech_check.setChecked(True)
        speech_layout.addWidget(self.speech_check)
        
        # Enhancement level
        enhancement_layout = QHBoxLayout()
        enhancement_label = QLabel("Enhancement Level:")
        self.enhancement_combo = QComboBox()
        self.enhancement_combo.addItems([level.value for level in SpeechEnhancementLevel])
        self.enhancement_combo.setCurrentText(SpeechEnhancementLevel.MEDIUM.value)
        enhancement_layout.addWidget(enhancement_label)
        enhancement_layout.addWidget(self.enhancement_combo)
        speech_layout.addLayout(enhancement_layout)
        
        # Voice clarity boost
        self.clarity_check = QCheckBox("Enable Voice Clarity Boost")
        self.clarity_check.setChecked(True)
        speech_layout.addWidget(self.clarity_check)
        
        # Background noise level
        noise_suppression_layout = QHBoxLayout()
        noise_suppression_label = QLabel("Background Noise:")
        self.noise_suppression_combo = QComboBox()
        self.noise_suppression_combo.addItems([level.value for level in BackgroundNoiseLevel])
        self.noise_suppression_combo.setCurrentText(BackgroundNoiseLevel.MODERATE.value)
        noise_suppression_layout.addWidget(noise_suppression_label)
        noise_suppression_layout.addWidget(self.noise_suppression_combo)
        speech_layout.addLayout(noise_suppression_layout)
        
        speech_group.setLayout(speech_layout)
        layout.addWidget(speech_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")
        self.ok_button = QPushButton("OK")
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)
        layout.addLayout(button_layout)
        
        # Set layout
        self.setLayout(layout)
        
        # Connect signals
        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.accept)
        self.browse_button.clicked.connect(self.browse_file)
        
    def browse_file(self):
        """Open file dialog to select audio file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            "Audio Files (*.wav *.mp3 *.m4a *.aac *.ogg *.flac)"
        )
        if file_path:
            self.file_path.setText(file_path)
            
    def get_configuration(self):
        """Get the task configuration."""
        return {
            "input_path": self.file_path.text(),
            "noise_reduction_level": NoiseReductionLevel(self.noise_combo.currentText()),
            "enable_speech_enhancement": self.speech_check.isChecked(),
            "speech_enhancement_level": SpeechEnhancementLevel(self.enhancement_combo.currentText()),
            "voice_clarity_boost": self.clarity_check.isChecked(),
            "background_noise_level": BackgroundNoiseLevel(self.noise_suppression_combo.currentText())
        } 