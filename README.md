# Spectrogram

Create spectrograms from audio files and input data.

This script streams audio from the specified input device and generates Mel-frequency spectrograms. The streaming continues indefinitely until interrupted by the user. The spectrogram is displayed in a window and updated in real-time as new audio data is processed. When the user interrupts the streaming (by pressing Ctrl+C), the current spectrogram is saved to a file named `output.png`.

## Requirements:
  ```python
    pip install -e .
  ```

## Usage:
  ```
    spectrogram --device <device_id>
  ```
  Replace `<device_id>` with the ID of the audio input device to use. To list available audio devices, run the script without the `--device` argument:
  ```
    spectrogram
  ```
