import argparse
import time
from gtts import gTTS
import playsound
import os
import re
import pyttsx3
import tempfile
from pathlib import Path
from pydub import AudioSegment

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
    if not os.path.exists(output_file):
        silent_audio = AudioSegment.silent(duration=duration * 1000)  # duration in ms
        silent_audio.export(output_file, format="mp3")
        print(f"Generated silent audio for {duration} seconds: {output_file}")
    else:
        print(f"Reusing existing silent audio for {duration} seconds: {output_file}")

def generate_tts_audio(line, output_file, local, engine=None):
    """Generate TTS audio for a line."""
    if not os.path.exists(output_file):
        print(f"Generating audio: {line}")
        if not local:
            for attempt in range(3):
                try:
                    tts = gTTS(text=line, lang="en")
                    tts.save(output_file)
                    break
                except Exception as e:
                    print(f"Error generating TTS for line '{line}': {e}")
                    if attempt == 2:
                        raise
        else:
            engine.save_to_file(line, output_file)
            engine.runAndWait()
    else:
        print(f"Reusing existing audio for: {line}")

def combine_audio_files(input_folder, output_file):
    """Combine all generated audio files into one."""
    audio_files = sorted(
        [f for f in os.listdir(input_folder) if f.endswith(".mp3")]
    )

    if not audio_files:
        print("No audio files found to combine.")
        return False

    print("Combining the following files:")
    combined_audio = AudioSegment.empty()

    for file in audio_files:
        print(f"  - {file}")
        file_path = os.path.join(input_folder, file)
        audio_segment = AudioSegment.from_file(file_path)
        combined_audio += audio_segment

    combined_audio.export(output_file, format="mp3")
    print(f"Combined audio saved as: {output_file}")
    return True

def generate_audio(script, countdown, local, rate, silent):
    start_time = time.time()
    output_folder = tempfile.mkdtemp(prefix="generated_audio_")

    print(f"Temporary files will be stored in: {output_folder}")

    try:
        engine = None
        if local:
            engine = configure_pyttsx3(rate)

        for idx, line in enumerate(script):
            line = line.strip()
            if not line:
                continue

            if line.startswith("[Gap:"):
                match = re.match(r"\[Gap:\s*(\d+)\s*seconds\]", line)
                if match:
                    gap_duration = int(match.group(1))
                    gap_file = os.path.join(output_folder, f"gap_{gap_duration}.mp3")
                    generate_silent_audio(gap_duration, gap_file)
                continue

            audio_file = os.path.join(output_folder, f"audio_{hash(line)}.mp3")
            generate_tts_audio(line, audio_file, local, engine)

            if not silent:
                playsound.playsound(audio_file)

        final_audio_path = os.path.join(os.getcwd(), "final_workout_audio.mp3")
        if combine_audio_files(output_folder, final_audio_path):
            print(f"Final combined audio file saved at: {final_audio_path}")

        total_time = time.time() - start_time
        print(f"Total generation time: {time.strftime('%H:%M:%S', time.gmtime(total_time))}")

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