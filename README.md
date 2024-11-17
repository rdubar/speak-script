
# Speak Script: gh auth loginWorkout Audio Script Generator

This Python project generates audio workout scripts with options for text-to-speech synthesis, silent mode, and customizable gaps. It supports both online (`gTTS`) and offline (`pyttsx3`) text-to-speech engines.

## Features

- Generate workout audio scripts from a text file.
- Create silent gaps as audio files without real-time waiting.
- Choose between online and offline TTS options.
- Save generated audio files to a temporary directory.
- Display total audio duration and file size after generation.

## Requirements

This project requires:
- **Python 3.11.x** (Ensure compatibility; avoid using unstable Python versions like 3.13).
- **pip**, **setuptools**, and **wheel** (latest versions recommended).
- `ffmpeg` (for `pydub`).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/speak-script
   cd speak-script
   ```

2. **Set Up Python Environment**:
   - Ensure you are using Python 3.11.x:
     ```bash
     python --version
     ```
   - If necessary, install or activate Python 3.11.x using tools like `pyenv` or your system's package manager.

3. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. **Upgrade `pip`, `setuptools`, and `wheel`**:
   ```bash
   pip install --upgrade pip setuptools wheel
   ```

5. **Install Dependencies**:
   - Generate the `requirements.txt` file using `pipreqs` if needed:
     ```bash
     pipreqs /path/to/your/project --force
     ```
   - Install all required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

6. **Install `ffmpeg`**:
   - Required for `pydub`. Install using your package manager:
     - On macOS (Homebrew):
       ```bash
       brew install ffmpeg
       ```
     - On Ubuntu:
       ```bash
       sudo apt update && sudo apt install ffmpeg
       ```
     - On Windows:
       Download and add `ffmpeg` to your system PATH:
       [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

## Usage

### Command-Line Options
Run the script with various options:
```bash
python speak_script.py [OPTIONS]
```

#### Options
- `--script`: Path to the text file containing the workout script. Default: `default_script.txt`.
- `--gap`: Time gap (in seconds) between exercises. Default: `25`.
- `--local`: Use offline TTS (`pyttsx3`) instead of online TTS (`gTTS`).
- `--rate`: Speech rate for offline TTS (words per minute). Default: `120`.
- `--silent`: Generate audio files without playing them during execution.

### Example Commands
1. Generate workout audio with silent mode:
   ```bash
   python speak_script.py --script workout_script.txt --silent
   ```

2. Use offline TTS with a slower speech rate:
   ```bash
   python speak_script.py --local --rate 100
   ```

3. Generate and play audio in real-time:
   ```bash
   python speak_script.py
   ```

## Troubleshooting

### Common Issues
1. **`audioop` or `pyaudioop` Missing**:
   - Ensure you are using a compatible Python version (e.g., Python 3.11.x).
   - Reinstall `pyaudio`:
     ```bash
     brew install portaudio
     pip install pyaudio
     ```

2. **`ffmpeg` Not Found**:
   - Ensure `ffmpeg` is installed and accessible in your PATH.
   - Verify installation with:
     ```bash
     ffmpeg -version
     ```

3. **Installation Fails for `playsound`**:
   - Upgrade `pip`, `setuptools`, and `wheel`:
     ```bash
     pip install --upgrade pip setuptools wheel
     ```
   - Use a compatible version of `playsound`:
     ```bash
     pip install playsound==1.2.2
     ```

4. **Python Version Compatibility**:
   - Downgrade or switch to Python 3.11.x if using an unstable version like Python 3.13.

## Development

### Regenerate `requirements.txt`
To regenerate `requirements.txt` using `pipreqs`:
```bash
pipreqs /path/to/your/project --force
```

### Test the Script
Run the script with sample inputs and ensure that:
- Audio files are generated correctly.
- Silent gaps work as expected.
- Total duration and file size are calculated.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
