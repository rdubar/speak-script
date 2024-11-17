import argparse
import time
from gtts import gTTS
import playsound
import os
import re
import pyttsx3
import tempfile
from pathlib import Path
import shutil
from pydub import AudioSegment
from pydub.generators import Sine

DEFAULT_WORDS_PER_MINUTE = 120

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate workout audio from a script with timed gaps and countdowns."
    )
    parser.add_argument(
        "--script",
        type=str,
        default="default_script.txt",
        help="Path to the text file containing the workout script. Default is 'default_script.txt'."
    )
    parser.add_argument(
        "--gap",
        type=int,
        default=25,
        help="Time gap (in seconds) between exercises. Default is 25 seconds."
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help="Use local text-to-speech (pyttsx3) instead of online (gTTS)."
    )
    parser.add_argument(
        "--rate",
        type=int,
        default=DEFAULT_WORDS_PER_MINUTE,
        help=f"Speech rate for offline text-to-speech. Default is {DEFAULT_WORDS_PER_MINUTE} words per minute."
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Generate audio files without playing them during execution."
    )
    return parser.parse_args()

def load_script(script_path):
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Script file '{script_path}' not found.")
    with open(script_path, "r") as file:
        return [line.strip() for line in file if line.strip()]

def configure_pyttsx3(rate):
    """Configure pyttsx3 engine with a slower speech rate and female voice."""
    engine = pyttsx3.init()
    # Set speech rate
    engine.setProperty("rate", rate)
    # Set female voice
    voices = engine.getProperty("voices")
    for voice in voices:
        if "female" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break
    return engine

def generate_silent_audio(duration, output_file):
    """Generate a silent audio file for the specified duration."""
    print(f"Generating silent gap audio: {duration} seconds")
    silent_audio = AudioSegment.silent(duration=duration * 1000)  # duration in ms
    silent_audio.export(output_file, format="mp3")

def generate_audio(script, countdown, local, rate, silent):
    start_time = time.time()
    total_size = 0
    output_folder = tempfile.mkdtemp(prefix="generated_audio_")

    print(f"Temporary files will be stored in: {output_folder}")

    try:
        engine = None
        if local:
            engine = configure_pyttsx3(rate)

        output_files = []

        for idx, line in enumerate(script):
            # Strip and skip empty lines
            line = line.strip()
            if not line:
                continue  # Skip processing for empty lines

            # Handle `[Gap: X seconds]` markers explicitly
            if line.startswith("[Gap:"):
                match = re.match(r"\[Gap:\s*(\d+)\s*seconds\]", line)
                if match:
                    gap_duration = int(match.group(1))
                    gap_file = os.path.join(output_folder, f"gap_{idx}.mp3")
                    generate_silent_audio(gap_duration, gap_file)
                    output_files.append(gap_file)
                continue  # Skip further processing for this line

            # Generate audio file
            filename = os.path.join(output_folder, f"audio_{idx}.mp3")
            print(f"Generating: {line}")

            if not local:
                # Online TTS with gTTS
                for attempt in range(3):
                    try:
                        tts = gTTS(text=line, lang="en")
                        tts.save(filename)
                        break  # Exit retry loop if successful
                    except Exception as e:
                        print(f"Error generating TTS for line '{line}': {e}")
                        if attempt == 2:  # Retry up to 3 times
                            raise
            else:
                # Offline TTS with pyttsx3
                engine.save_to_file(line, filename)
                engine.runAndWait()

            output_files.append(filename)
            total_size += os.path.getsize(filename)

            if not silent:
                # Play the audio file if not in silent mode
                playsound.playsound(filename)

        # Calculate and display total time and file size
        end_time = time.time()
        total_time = end_time - start_time
        print("\n--- Generation Complete ---")
        print(f"Output Folder: {output_folder}")
        print(f"Total Time: {time.strftime('%H:%M:%S', time.gmtime(total_time))}")
        print(f"Total Size: {total_size / (1024 ** 2):.2f} MB")
        print("Generated Files:")
        for file in output_files:
            print(file)

    except Exception as e:
        print(f"Error during audio generation: {e}")
    finally:
        print("\n--- Cleanup Complete ---")

def main():
    args = parse_arguments()
    try:
        script = load_script(args.script)
    except FileNotFoundError as e:
        print(e)
        return

    print("Starting workout audio generation...")
    generate_audio(script, args.gap, args.local, args.rate, args.silent)
    print("Workout audio generation complete!")

if __name__ == "__main__":
    main()