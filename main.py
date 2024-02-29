#!/usr/bin/env python3

"""
Description:
This script streams audio from the specified input device and generates a real-time Mel-frequency spectrogram. The streaming continues indefinitely until interrupted by the user. The spectrogram is displayed in a window and updated in real-time as new audio data is processed. When the user interrupts the streaming (by pressing Ctrl+C), the current spectrogram is saved to a file named `output.png`.

Requirements:
  ```
    pip install numpy sounddevice librosa matplotlib
  ```

Usage:
  ```
    python main.py --device <device_id>
  ```
  Replace `<device_id>` with the ID of the audio input device to use. To list available audio devices, run the script without the `--device` argument:
  ```
    python main.py
  ```
"""

import numpy as np
import sounddevice as sd
import librosa
import librosa.display
import matplotlib.pyplot as plt
from typing import Optional
import argparse
import sys

def list_audio_devices():
    """Prints a list of available audio devices."""
    print("Available audio devices:")
    try:
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            print(f"ID: {i}, Name: {device['name']}, Channels: {device['max_input_channels']}")
    except Exception as e:
        print(f"An error occurred while retrieving audio devices: {e}")


def stream_audio_to_spectrogram(
    device: Optional[str],
    chunk_size: int = 1024,
    sample_rate: int = 22050,
    n_fft: int = 2048,
    hop_length: int = 512,
    n_mels: int = 128
) -> None:
    """
    Streams audio from the specified device and generates a real-time spectrogram.
    The streaming continues indefinitely until interrupted by the user.

    Parameters:
    - device: The device ID or name for audio input. If None, the default device is used.
    - chunk_size: Size of each audio chunk to process.
    - sample_rate: Sample rate to read audio.
    - n_fft: Number of FFT components.
    - hop_length: Number of samples between successive frames.
    - n_mels: Number of Mel bands.
    """
    try:
        # Initialize the plot
        plt.figure(figsize=(10, 4))

        # Initialize an empty buffer for the spectrogram
        spectrogram = np.zeros((n_mels, chunk_size // hop_length + 1))

        # Audio callback function
        def audio_callback(indata: np.ndarray, frames: int, time, status: sd.CallbackFlags) -> None:
            nonlocal spectrogram
            if status:
                print(status, file=sys.stderr)
            audio = indata.mean(axis=1)
            S = librosa.feature.melspectrogram(audio, sr=sample_rate, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
            S_dB = librosa.power_to_db(S, ref=np.max)
            spectrogram = np.hstack((spectrogram[:, 1:], S_dB))

        # Open the audio stream
        with sd.InputStream(device=device, channels=1, callback=audio_callback, blocksize=chunk_size, samplerate=sample_rate):
            print("Streaming started... Press Ctrl+C to stop.")
            while True:
                plt.clf()
                S_dB = librosa.power_to_db(spectrogram, ref=np.max)
                librosa.display.specshow(S_dB, sr=sample_rate, hop_length=hop_length, x_axis='time', y_axis='mel')
                plt.colorbar(format='%+2.0f dB')
                plt.title("Real-time Mel-frequency spectrogram")
                plt.draw()
                plt.pause(0.01)

    except KeyboardInterrupt:
        # When Ctrl+C is pressed, save the current spectrogram to a file
        plt.savefig("output.png")
        print("Streaming stopped. Spectrogram saved to output.png.")


def is_virtual_env():
    if hasattr(sys, 'base_prefix'):
        return sys.prefix != sys.base_prefix
    elif hasattr(sys, 'real_prefix'):
        return sys.prefix != sys.real_prefix
    else:
        return False


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Real-time audio spectrogram streaming.")
  parser.add_argument("--device", type=str, help="Audio input device ID or name.")
  args = parser.parse_args()

  if not is_virtual_env():
    print("Please run this script in a virtual environment.")
    sys.exit(1)

  if args.device is None:
    parser.print_help()
    list_audio_devices()
  else:
    stream_audio_to_spectrogram(device=args.device)