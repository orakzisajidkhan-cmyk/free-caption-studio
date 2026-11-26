#!/usr/bin/env python3
"""Burn captions into a video with local ffmpeg. No keys, no cost.

Usage:
    python3 caption.py input.mp4 --srt captions.srt --out out.mp4
    python3 caption.py input.mp4 --srt captions.srt --style bold \
        --hook "Watch this" --out out.mp4
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

STYLES = {
    "classic": "FontName=DejaVu Sans,FontSize=16,PrimaryColour=&HFFFFFF,"
               "OutlineColour=&H000000,BorderStyle=1,Outline=2,Shadow=0,"
               "Alignment=2,MarginV=36",
    "bold": "FontName=DejaVu Sans,FontSize=19,Bold=1,PrimaryColour=&HFFFFFF,"
            "OutlineColour=&H000000,BorderStyle=1,Outline=3,Shadow=0,"
            "Alignment=2,MarginV=42",
    "box": "FontName=DejaVu Sans,FontSize=16,PrimaryColour=&HFFFFFF,"
           "BackColour=&H80000000,BorderStyle=4,Outline=0,Shadow=0,"
           "Alignment=2,MarginV=36",
}

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
]


def run(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-5:]
        raise SystemExit("ffmpeg failed:\n" + "\n".join(tail))
    return proc


def probe(path):
    out = run([
        "ffprobe", "-v", "error", "-show_entries",
        "stream=width,height,codec_type", "-show_entries",
        "format=duration", "-of", "json", path,
    ]).stdout
    data = json.loads(out)
    video = next(s for s in data["streams"] if s["codec_type"] == "video")
    return {
        "duration": round(float(data["format"]["duration"]), 3),
        "width": video["width"],
        "height": video["height"],
    }


def find_font():
    for candidate in FONT_CANDIDATES:
        if os.path.exists(candidate):
            return candidate
    return None


def main():
    parser = argparse.ArgumentParser(description="Burn captions into a video")
    parser.add_argument("input", help="input video file")
    parser.add_argument("--srt", required=True, help="SRT caption file")
    parser.add_argument("--out", required=True, help="output video file")
    parser.add_argument("--style", choices=sorted(STYLES), default="classic")
    parser.add_argument("--hook", default="", help="hook headline for the opening")
    parser.add_argument("--hook-seconds", type=float, default=3.0)
    args = parser.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise SystemExit(f"{tool} is required but was not found")
    if not os.path.exists(args.input):
        raise SystemExit(f"input video not found: {args.input}")
    if not os.path.exists(args.srt):
        raise SystemExit(f"caption file not found: {args.srt}")

    info = probe(args.input)
    height = info["height"]

    with tempfile.TemporaryDirectory() as tmp:
        # Copy the SRT to a plain path so the subtitles filter needs no escaping.
        srt_copy = os.path.join(tmp, "captions.srt")
        shutil.copyfile(args.srt, srt_copy)
        filters = [f"subtitles='{srt_copy}':force_style='{STYLES[args.style]}'"]

        hook = args.hook.strip()
        if hook:
            hook_file = os.path.join(tmp, "hook.txt")
            with open(hook_file, "w", encoding="utf-8") as fh:
                fh.write(hook)
            font = find_font()
            font_arg = f"fontfile='{font}':" if font else ""
            size = max(int(height * 0.032), 16)
            filters.append(
                f"drawtext={font_arg}textfile='{hook_file}':fontsize={size}:"
                f"fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=16:"
                f"x=(w-text_w)/2:y={int(height * 0.05)}:"
                f"enable='lt(t,{args.hook_seconds})'"
            )

        run([
            "ffmpeg", "-y", "-v", "error", "-i", args.input,
            "-vf", ",".join(filters),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "copy", args.out,
        ])

    result = probe(args.out)
    result["out"] = os.path.abspath(args.out)
    result["style"] = args.style
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
