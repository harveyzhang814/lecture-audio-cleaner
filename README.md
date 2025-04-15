# Lecture Audio Cleaner

An open-source audio processing tool designed to enhance and clean speech in lecture recordings, featuring a simple GUI for general users.

## Features

- Noise reduction with adjustable levels (Light/Medium/Strong)
- Speech enhancement using VoiceFixer
- Batch processing of multiple audio files
- Export cleaned audio in WAV or MP3 format
- User-friendly GUI interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lecture-audio-cleaner.git
cd lecture-audio-cleaner
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Launch the application:
```bash
python src/main.py
```

2. Using the GUI:
   - Click "Add Task" to add audio files for processing
   - Configure noise reduction level and speech enhancement
   - Select output format
   - Click "Start" to begin processing
   - Monitor progress in the task list

## Project Structure

```
lecture-audio-cleaner/
├── src/                    # Source code
│   ├── main.py            # Main application entry point
│   ├── gui/               # GUI components
│   ├── audio/             # Audio processing modules
│   └── utils/             # Utility functions
├── tests/                 # Test files
├── docs/                  # Documentation
├── data/                  # Data files (not tracked by git)
├── requirements.txt       # Project dependencies
└── setup.py              # Package installation script
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 