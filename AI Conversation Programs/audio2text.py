import os
import sys
import wave
import json
from vosk import Model, KaldiRecognizer

def transcribe_audio(model_path, audio_file, output_file):
    # Load the Vosk model
    if not os.path.exists(model_path):
        print(f"Model path {model_path} does not exist")
        return
    print(f"Loading model from {model_path}...")
    model = Model(model_path)
    print("Model loaded successfully.")

    # Open the audio file
    print(f"Opening audio file {audio_file}...")
    wf = wave.open(audio_file, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 32000, 44100, 48000]:
        print("Audio file must be WAV format mono PCM.")
        return
    print("Audio file opened successfully.")

    # Initialize the recognizer
    print("Initializing recognizer...")
    rec = KaldiRecognizer(model, wf.getframerate())
    print("Recognizer initialized.")

    # Read audio data and transcribe
    print("Starting transcription...")
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            results.append(json.loads(result))

    # Get final result
    final_result = rec.FinalResult()
    results.append(json.loads(final_result))

    # Print the transcription
    transcription = " ".join([res['text'] for res in results])
    print("Transcription completed.")
    print("Transcription:", transcription)

    # Save the transcription to a file
    print(f"Saving transcription to {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(transcription)
    print(f"Transcription saved to {output_file}")

if __name__ == "__main__":
    model_path = "C:/Users/18660/Desktop/00dkuclass/info104/vosk-model-en-us-0.22"
    audio_file = "C:/Users/18660/Desktop/00dkuclass/info104/000final/command.wav"
    output_file = "C:/Users/18660/Desktop/00dkuclass/info104/000final/manbo1.txt"
    print(f"Model path: {model_path}")
    print(f"Audio file: {audio_file}")
    print(f"Output file: {output_file}")
    transcribe_audio(model_path, audio_file, output_file)