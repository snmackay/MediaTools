import os
import argparse
import subprocess
import xml.etree.ElementTree as ET

# Path to the config file (place it next to this script, or change this path)
CONFIG_FILE = "config.xml"

# Video file extensions to check
VIDEO_EXTENSIONS = {
    ".mkv", ".mp4", ".avi", ".mov", ".wmv",
    ".m4v", ".ts", ".m2ts", ".flv", ".webm"
}

# Map user-facing codec names to what ffprobe reports in codec_name
CODEC_NAME_MAP = {
    "h264": "h264",
    "x265": "hevc",
    "av1": "av1",
}


def load_config(config_path):
    """Read scan_path from an XML config file."""
    try:
        tree = ET.parse(config_path)
        root = tree.getroot()

        scan_path = root.findtext("scan_path")

        if not scan_path:
            raise ValueError(
                "config.xml must contain a <scan_path> element"
            )

        return scan_path.strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {config_path}")
    except ET.ParseError as e:
        raise ValueError(f"Could not parse {config_path}: {e}")


def get_video_codec(file_path):
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=codec_name",
                "-of", "default=noprint_wrappers=1:nokey=1",
                file_path,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout.strip().lower()
    except Exception:
        print(f"Error occurred in trying to scan: {file_path}")
        return None


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scan a directory for video files encoded with a given codec."
    )
    parser.add_argument(
        "codec",
        choices=sorted(CODEC_NAME_MAP.keys()),
        help="Codec to scan for: h264, x265, or av1",
    )
    parser.add_argument(
        "output_file",
        help="Path to the file where matching video paths will be written",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    target_codec = CODEC_NAME_MAP[args.codec]

    scan_path = load_config(CONFIG_FILE)

    with open(args.output_file, "w", encoding="utf-8") as outfile:
        for root, _, files in os.walk(scan_path):
            for file in files:
                if os.path.splitext(file)[1].lower() in VIDEO_EXTENSIONS:
                    full_path = os.path.join(root, file)
                    codec = get_video_codec(full_path)
                    if codec == target_codec:
                        outfile.write(f"{full_path}\n")
                        print(f"Found {args.codec}: {full_path}")

    print(f"\nDone! Results saved to {args.output_file}")


if __name__ == "__main__":
    main()