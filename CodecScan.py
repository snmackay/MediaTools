import os
import subprocess

# Change these paths
TV_SHOWS_DIR = r"D:\TV Shows"
OUTPUT_FILE = r"h264_files.txt"

# Video file extensions to check
VIDEO_EXTENSIONS = {
    ".mkv", ".mp4", ".avi", ".mov", ".wmv",
    ".m4v", ".ts", ".m2ts", ".flv", ".webm"
}


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
        print(f"Error occurred in trying to scan:" file_path)
        return None

def main(){
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
    for root, _, files in os.walk(TV_SHOWS_DIR):
        for file in files:
            if os.path.splitext(file)[1].lower() in VIDEO_EXTENSIONS:
                full_path = os.path.join(root, file)
                codec = get_video_codec(full_path)

                if codec == "h264":
                    outfile.write(f"{full_path}\n")
                    print(f"Found H.264: {full_path}")

    print(f"\nDone! Results saved to {OUTPUT_FILE}")
}

if __name__ == "__main__":
    main()
