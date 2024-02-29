import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt


def process_mp3(file_path: str, chunk_size: int = 1024, sample_rate: int = 22050,
                n_fft: int = 2048, hop_length: int = 512, n_mels: int = 128) -> None:
    """
    Processes an MP3 file and generates a spectrogram.

    Parameters:
    - file_path: Path to the MP3 file.
    - chunk_size: Size of each audio chunk to process.
    - sample_rate: Sample rate to read audio.
    - n_fft: Number of FFT components.
    - hop_length: Number of samples between successive frames.
    - n_mels: Number of Mel bands.
    """
    try:
        # Load the MP3 file
        y, sr = librosa.load(file_path, sr=sample_rate, mono=True)

        # Compute the Mel spectrogram
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
        S_dB = librosa.power_to_db(S, ref=np.max)

        # Plot the spectrogram
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(S_dB, sr=sr, hop_length=hop_length, x_axis='time', y_axis='mel')
        plt.colorbar(format='%+2.0f dB')
        plt.title(f"Mel-frequency spectrogram for {file_path}")
        plt.tight_layout()
        plt.savefig("output.png")

    except Exception as e:
        print(f"An error occurred while processing the MP3 file: {e}")
