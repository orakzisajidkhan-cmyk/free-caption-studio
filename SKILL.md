---
name: free-caption-studio
description: Burn readable captions into any video for free with local ffmpeg, no API keys and no credits. Takes a video plus an SRT file, applies a classic, bold or boxed caption style, adds an optional hook headline for the opening seconds, and verifies the real duration and resolution of the finished file. Use for "add captions", "burn subtitles", Shorts, reels and explainers that need on-screen text.
---

# Free caption studio

One video and one SRT file become a captioned video that plays
with readable text on every platform. Everything runs locally
with ffmpeg.

## Know the limits first

- Captions are burned into the picture. They cannot be switched
  off by the viewer, so keep a clean copy of the video when you
  also need selectable subtitles.
- The SRT timing must match the video. This skill does not
  transcribe speech or fix timing drift.
- Caption text comes from your SRT file. Check spelling and
  line breaks before burning, because burned text is final.

## Caption the video

- Prepare an SRT file with short cues, one or two lines each,
  timed to the speech.
- Run the builder with `python3 scripts/caption.py input.mp4
  --srt captions.srt --out out.mp4` from the skill folder, or
  pass the full path to `caption.py` from anywhere.
- Pick a style with `--style`: `classic` for a clean outline,
  `bold` for Shorts and reels, `box` for a dark band behind the
  text.
- Add `--hook "Your headline"` to show a hook headline for the
  opening seconds. Set `--hook-seconds` when the default three
  seconds is not right.
- Read the JSON summary the builder prints. It reports the real
  duration, width and height from the finished file.

## Verify before delivery

- Extract frames at the start, middle and end with ffmpeg and
  look at them. Captions must sit inside the frame, stay clear
  of faces and important action, and remain readable at small
  size.
- Check the hook headline shows only during the opening seconds
  and does not cover the first caption.
- Confirm the printed duration matches the input video. A
  shorter output means the encode failed partway.
- Fix the SRT or the style and rebuild when a frame fails. Do
  not stretch the video to hide a caption problem.

## Requirements

- Install ffmpeg and ffprobe. The builder checks for both and
  stops with a clear message when they are missing.
- Use Python 3.10 or newer. No other packages are needed.
- Run the example in `examples/hello` to confirm the setup. Run
  `make_sample.py` there first to create a sample video, then
  run the builder on it with `sample.srt`.
