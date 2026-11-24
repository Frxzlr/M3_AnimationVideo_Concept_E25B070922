"""
Assemble the final video: put each scene's narration under its rendered picture, then join the scenes.

    1. Render scenes (1080p, 30 fps):
         manim -qh --fps 30 --disable_caching eigen_video.py S0Title S1Hook ... S6Summary
    2. python build_video.py
Narration starts PAD seconds into each scene (same PAD as SyncedScene in eigen_video.py).
"""
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCENES = ["S0Title", "S1Hook", "S2Concept", "S3Intuition", "S4Example", "S5Interpretation", "S6Summary"]
PAD_MS = 400
OUT = os.path.join(HERE, "Eigenvectors_Video.mp4")


def find_video(name):
    hits = sorted(glob.glob(os.path.join(HERE, "media*", "videos", "eigen_video", "1080p30", f"{name}.mp4")),
                  key=os.path.getmtime)
    if not hits:
        sys.exit(f"missing render for {name}")
    return hits[-1]


def run(cmd):
    subprocess.run(cmd, check=True)


os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
parts = []
for i, name in enumerate(SCENES):
    vid = find_video(name)
    out = os.path.join(HERE, "build", f"{i}_{name}.mp4")
    common = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
              "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart"]
    if i == 0:  # title card: silent track
        run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
             "-map", "0:v", "-map", "1:a", *common, out])
    else:
        wav = os.path.join(HERE, "audio", f"scene{i}.wav")
        run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", wav, "-filter_complex",
             f"[1:a]adelay={PAD_MS}|{PAD_MS},apad[a]", "-map", "0:v", "-map", "[a]", *common, out])
    parts.append(out)

lst = os.path.join(HERE, "build", "list.txt")
with open(lst, "w") as f:
    f.writelines(f"file '{p}'\n" for p in parts)
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
     "-movflags", "+faststart", OUT])
dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", OUT],
                     capture_output=True, text=True).stdout.strip()
print(f"wrote {OUT}  ({float(dur) / 60:.2f} min)")
