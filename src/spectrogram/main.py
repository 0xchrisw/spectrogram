import argparse
import sys

from spectrogram.sources import stream
from spectrogram.sources import file


def is_virtual_env():
    if hasattr(sys, 'base_prefix'):
        return sys.prefix != sys.base_prefix
    elif hasattr(sys, 'real_prefix'):
        return sys.prefix != sys.real_prefix
    else:
        return False


def main():
    parser = argparse.ArgumentParser(description="Real-time audio spectrogram streaming.")
    parser.add_argument("--device", type=str, help="Audio input device ID or name.")
    parser.add_argument("--mp3", type=str, help="Path to the MP3 file to process.")
    args = parser.parse_args()

    # if not is_virtual_env():
    #   print("Please run this script in a virtual environment.")
    #   sys.exit(1)

    if args.mp3:
        file.process_mp3(args.mp3)
    elif args.device is None:
        parser.print_help()
        stream.list_audio_devices()

    else:
        stream.stream_audio_to_spectrogram(device=args.device)


if __name__ == "__main__":
    main()
