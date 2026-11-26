# Free Caption Studio

Burn readable captions into any video. No API keys, no credits.
Everything runs locally with ffmpeg.

Give it a video and an SRT caption file. It burns the captions
into the picture in one of three styles, adds an optional hook
headline for the opening seconds, and prints the real duration
and resolution read back from the finished file.

Captions are burned in, so viewers cannot switch them off. Keep
a clean copy of the video when you also need selectable
subtitles. The SRT timing must match the video; this skill does
not transcribe speech.

## Install

Copy this folder into your agent skills folder, for example:

```bash
git clone https://github.com/orakzisajidkhan-cmyk/free-caption-studio ~/.claude/skills/free-caption-studio
```

## Use

```bash
python3 scripts/caption.py input.mp4 --srt captions.srt --out out.mp4
python3 scripts/caption.py input.mp4 --srt captions.srt --style bold --hook "Watch this" --out out.mp4
```

Styles: `classic` (clean outline), `bold` (large text for Shorts
and reels), `box` (dark band behind the text).

## Example

```bash
cd examples/hello
python3 make_sample.py
python3 ../../scripts/caption.py sample.mp4 --srt sample.srt --style bold --hook "Captions in seconds" --out captioned.mp4
```

## Requirements

Python 3.10 or newer, ffmpeg and ffprobe. No API keys, no
accounts, no GPU. Works on Windows, macOS and Linux.

## Licence

MIT. See `LICENSE`.
