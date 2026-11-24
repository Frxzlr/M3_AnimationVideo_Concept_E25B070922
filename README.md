# Eigenvectors: The Directions a Matrix Doesn't Turn

**M3 (Linear Algebra & Calculus) · Internal Assessment · Project Option 1: Animation Video**
**Student:** Sourav · **Student ID:** E25B070922

**Learning objective:** By the end of this video, the viewer will be able to find the eigenvalues and eigenvectors of a 2 × 2 matrix and explain what they mean geometrically.

**Worked example:** A = [[2, 1], [1, 2]] → eigenvalues λ₁ = 3, λ₂ = 1 with eigenvectors v₁ = (1, 1), v₂ = (1, −1).

## Deliverables in this repository

| File | What it is |
|---|---|
| `Eigenvectors_Video.mp4` | Final video, 1920×1080, 16:9, 30 fps, 5 min 35 s, voice-over narration |
| `Storyboard_and_Script.pdf` | 6-scene storyboard (purpose, visuals, math per scene) and full narration script |
| `_Code/` | Complete animation source code, narration audio and the build pipeline |

## Video structure

| # | Scene | What happens |
|---|---|---|
| 0 | Opening frame | Title, concept, name and student ID |
| 1 | Hook | 16 arrows are transformed by a matrix. Most get knocked off their lines, but a few only stretch. Introduces the word *eigen* (German for "own"). |
| 2 | Concept | Definition Av = λv, with each symbol labelled. Shows stretch (λ>1), shrink (0<λ<1) and flip (λ<0), why v ≠ 0, and the goal. |
| 3 | Visual intuition | A deforms the grid. (1,0) leaves its line, (1,1) lands on (3,3) (×3) and (1,−1) stays put. These are the two eigen-directions. |
| 4 | Worked example | Av = λv → (A − λI)v = 0 → det(A − λI) = 0, shown with a picture of a singular matrix squashing the plane. Then λ² − 4λ + 3 = (λ−3)(λ−1) = 0, solving for both eigenvectors, and a check by substitution. |
| 5 | Interpretation | A = "stretch ×3 along y = x, keep y = −x fixed". (2,0) = (1,1) + (1,−1) explains why other vectors tilt. Area scales by 3 = det A = λ₁λ₂, and tr A = 4 = λ₁ + λ₂. |
| 6 | Summary & credits | Three takeaways, then closing frame: "Thanks for watching!", name/ID, references, tools and AI disclosure |

**Colour code (consistent in every scene):** A blue · v yellow · λ orange · I purple · λ=3 eigen-direction (y = x) green · λ=1 eigen-direction (y = −x) red.

## How the animation is synced to the voice

1. `prep_audio.sh` cleans the recordings in `audio_raw/`: high-pass filter, noise reduction, pause gate, gentle compression and loudness normalisation to −16 LUFS.
2. `align.py` runs **forced alignment** with PocketSphinx. It already knows the script text, so it finds the start and end time of every spoken word and writes them to `align.json`.
3. In `eigen_video.py`, every scene is a `SyncedScene`. A call such as `self.at("lands")` waits until the moment the word *lands* is spoken, then plays the next animation. For example, the matrix entries in Scene 3 appear on "two… one… one… two".
4. `build_video.py` lays each scene's narration under its rendered picture (starting 0.4 s in) and joins the scenes into the final MP4.

## Rebuild from source

```bash
cd _Code
pip install -r requirements.txt          # also needs ffmpeg + LaTeX (dvisvgm) + pango/cairo
./prep_audio.sh                          # cleaned narration -> audio/
python align.py                          # word timings -> align.json (already included)
manim -qh --fps 30 --disable_caching eigen_video.py S0Title S1Hook S2Concept S3Intuition S4Example S5Interpretation S6Summary
python build_video.py                    # -> Eigenvectors_Video.mp4
```

Code files: `eigen_video.py` (all scenes), `style.py` (colours, fonts, helper builders), `cues.py` (phrase → time lookup), `align.py`, `prep_audio.sh`, `build_video.py`, `script_data.py` (narration text used for the alignment).

## Mathematical verification (done by hand)

- det(A − λI) = (2−λ)² − 1 = λ² − 4λ + 3 = (λ−3)(λ−1) ⇒ λ = 3, 1
- λ = 3: A − 3I = [[−1, 1], [1, −1]] ⇒ y = x ⇒ v₁ = (1, 1). Check: A(1,1) = (3,3) = 3(1,1) ✓
- λ = 1: A − I = [[1, 1], [1, 1]] ⇒ y = −x ⇒ v₂ = (1, −1). Check: A(1,−1) = (1,−1) = 1(1,−1) ✓
- (2,0) = (1,1) + (1,−1) ⇒ A(2,0) = 3(1,1) + 1(1,−1) = (4,2). Direct: A(2,0) = (4,2) ✓
- det A = 4 − 1 = 3 = 3 × 1 = λ₁λ₂ · tr A = 2 + 2 = 4 = 3 + 1 = λ₁ + λ₂ ✓
- Scene 3: A(1,0) = (2,1), which is no longer on the x-axis ✓

## References

- Gilbert Strang, *Introduction to Linear Algebra*, Chapter 6: Eigenvalues and Eigenvectors
- 3Blue1Brown, *Essence of Linear Algebra* (visual inspiration only; no footage reused)
- M3 course lecture notes

## Tools, music and AI disclosure

- **Tools:** Manim Community Edition (Python), FFmpeg, PocketSphinx (forced alignment for voice sync)
- **Music:** none
- **AI disclosure:** The script, storyboard and animation code were drafted with the help of Claude (Anthropic) and reviewed by the student. The narration is recorded in the student's own voice. All calculations were verified by hand.
