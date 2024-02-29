# Spectrogram

Create spectrograms from audio files and input data.

Streams audio from the specified input devices and generate Mel-frequency spectrograms. The streaming continues indefinitely until interrupted by the user. The spectrogram is displayed in a window and updated in real-time as new audio data is processed. When the user interrupts the streaming (by pressing Ctrl+C), the current spectrogram is saved to a file named `output.png`.


## Requirements:
  ```python
    pip install -e .
  ```

## Usage:
  MP3 processing:
  ```
    spectrogram --mp3=./audio/echo.mp3
  ```

  Real-time audio input:
  ```
    spectrogram --device <device_id>
  ```

  Replace `<device_id>` with the ID of the audio input device to use. To list available audio devices, run the script without the `--device` argument:
  ```
    spectrogram
  ```


## Examples

![Echo](/docs/echo_output.png)

![Alloy](/docs/alloy_output.png)

![CLI](/docs/cli_output.png)


## References
  - [Streaming audio in WSL](https://www.reddit.com/r/bashonubuntuonwindows/comments/hrn1lz/wsl_sound_through_pulseaudio_solved/)
  - [Secure directory creation in Windows](https://github.com/aseering/wsl_gui_autoinstall/issues/8#issuecomment-304552350)
  - [WSL Issue with helpful comments](https://github.com/microsoft/WSL/issues/5816)
