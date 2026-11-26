#!/usr/bin/env python3
"""Create a small sample video for the caption example."""

import os
import subprocess

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample.mp4")


def main():
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-i", "testsrc2=size=720x1280:rate=30:duration=6",
            "-f", "lavfi", "-i", "sine=frequency=220:duration=6",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
            "-shortest", OUT,
        ],
        check=True,
    )
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
