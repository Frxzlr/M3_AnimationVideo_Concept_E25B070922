#!/usr/bin/env bash
# Clean the raw phone recordings: remove rumble + hiss, gate the pauses, even out the level, -16 LUFS.
# Also makes 16 kHz mono copies used by align.py for the word-timing alignment.
set -e
cd "$(dirname "$0")"
mkdir -p audio
for n in 1 2 3 4 5 6; do
  ffmpeg -v error -y -i audio_raw/scene$n.m4a \
    -af "highpass=f=75,anlmdn=s=3:p=0.002:r=0.006,agate=threshold=0.012:ratio=3:attack=5:release=180:range=0.12,acompressor=threshold=-18dB:ratio=1.8:attack=10:release=150,loudnorm=I=-16:TP=-1.5:LRA=11" \
    -ac 2 -ar 48000 audio/scene$n.wav
  ffmpeg -v error -y -i audio_raw/scene$n.m4a -ac 1 -ar 16000 audio_raw/scene$n.16k.wav
done
echo "audio ready"
