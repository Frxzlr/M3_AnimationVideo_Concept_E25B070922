"""Word-level timing lookup from the forced alignment of the narration (align.json)."""
import json, re, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_W = {int(k): [(a, b, re.sub(r"\(\d+\)$", "", t)) for a, b, t in v if t not in ("<sil>", "<s>", "</s>", "[NOISE]")]
      for k, v in json.load(open(os.path.join(_HERE, "align.json"))).items()}
_REPL = {"eigenvector": "i gun vector", "eigenvectors": "i gun vectors", "eigenvalue": "i gun value",
         "eigenvalues": "i gun values", "eigendirections": "i gun directions", "x": "ex", "y": "why"}
def _norm(t):
    t = re.sub(r"[^a-z' ]", " ", t.lower().replace("-", " "))
    out = []
    for w in t.split(): out += _REPL.get(w, w).split()
    return out
def cue(scene, phrase, after=0.0, end=False):
    """Time (s) when `phrase` starts (or ends) in scene's narration, searching after `after`."""
    words, ph = _W[scene], _norm(phrase)
    for i in range(len(words) - len(ph) + 1):
        if words[i][0] >= after and [w[2] for w in words[i:i + len(ph)]] == ph:
            return words[i + len(ph) - 1][1] if end else words[i][0]
    raise KeyError(f"scene {scene}: phrase not found: {phrase!r} after {after}")
