#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Terminal-based Kokoro TTS Generator (Saving to Codespaces Workspace)
"""
import os
import numpy as np
from kokoro import KPipeline
import soundfile as sf

pipeline = KPipeline(lang_code='a') # <= make sure lang_code matches voice

# Voice options from the image you provided
VOICE_OPTIONS = [
    "af_heart", "af_alloy", "af_aoede", "af_bella", "af_jessica", "af_kore",
    "af_nicole", "af_nova", "af_river", "af_sarah", "af_sky",
    "am_adam", "am_echo", "am_eric", "am_fenrir", "am_liam", "am_michael",
    "am_onyx", "am_puck", "am_santa"
]

def read_text_from_file(filepath):
    """Reads text content from a file.

    Args:
        filepath (str): The path to the text file.

    Returns:
        str: The text content of the file, or None if an error occurred.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            text_content = file.read()
            return text_content
    except FileNotFoundError:
        print(f"Error: File not found at path: {filepath}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def generate_audio_terminal():
    print("Kokoro TTS Generator (Terminal Version)\n")

    audio_name = input("Enter audio name: ")

    print("\nSelect voice (enter number):")
    for i, voice_option in enumerate(VOICE_OPTIONS):
        print(f"{i+1}. {voice_option}")

    while True:
        try:
            voice_index_input = input("Enter voice number: ")
            voice_index = int(voice_index_input) - 1 # Adjust to 0-based index
            if 0 <= voice_index < len(VOICE_OPTIONS):
                selected_voice = VOICE_OPTIONS[voice_index]
                break
            else:
                print(f"Invalid voice number. Please enter a number between 1 and {len(VOICE_OPTIONS)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    text_input = ""
    while True:
        input_mode = input("\nChoose input mode:\n1. Type text in terminal\n2. Read text from .txt file\nEnter 1 or 2: ")
        if input_mode == '1':
            print("\nEnter text to synthesize (press Enter twice to finish):\n")
            text_input_lines = []
            while True:
                line = input()
                if not line: # Empty line indicates end of input
                    break
                text_input_lines.append(line)
            text_input = "\n".join(text_input_lines) # Join lines with newline characters
            break
        elif input_mode == '2':
            filepath = input("Enter the path to your .txt file: ")
            text_input = read_text_from_file(filepath)
            if text_input: # Proceed only if text was successfully read from file
                break
            else:
                print("Failed to read text from file. Please try again or choose terminal input.")
        else:
            print("Invalid input mode. Please enter 1 or 2.")

    if not audio_name:
        print("Error: Audio name cannot be empty.")
        return
    if not text_input or not text_input.strip(): # Check if text_input is None or empty string after file read
        print("Error: Text input cannot be empty.")
        return
    if not selected_voice:
        print("Error: Voice must be selected.")
        return

    generator = pipeline(
        text_input, voice=selected_voice,
        speed=1, split_pattern=r'\n+'
    )

    all_audio_segments = []
    for i, (gs, ps, audio) in enumerate(generator):
        print(f"Segment {i+1}:")
        print(f"  Grapheme Sequence: {gs}")
        print(f"  Phoneme Sequence: {ps}")
        all_audio_segments.append(audio)

    combined_audio = np.concatenate(all_audio_segments, axis=0)

    # --- Modified Output Directory ---
    # Save to a subdirectory named 'audio_output' within your Codespaces workspace
    output_dir = "audio_output"
    os.makedirs(output_dir, exist_ok=True) # Create the directory if it doesn't exist
    output_filename = f"{audio_name}.wav"
    output_path = os.path.join(output_dir, output_filename)
    # --- End of Modified Output Directory ---

    try:
        sf.write(output_path, combined_audio, 24000)
        print(f"\nSuccess! Audio saved to: {output_path}")
        print(f"File is located in the '{output_dir}' directory within your Codespaces workspace.") # Helpful message
    except Exception as e:
        print(f"Error saving audio: {e}")

if __name__ == "__main__":
    generate_audio_terminal()