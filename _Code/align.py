"""Forced alignment: find when each word of the script is spoken in each recording -> align.json.
Uses PocketSphinx's bundled US-English model. Words missing from its dictionary are skipped."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import re, json, wave, os, sys
from pocketsphinx import Decoder, get_model_path
from script_data import SCENES
mp = get_model_path()
dic = set()
for line in open(os.path.join(mp, "en-us", "cmudict-en-us.dict")):
    dic.add(line.split()[0])
REPL = {"eigenvector":"i gun vector","eigenvectors":"i gun vectors","eigenvalue":"i gun value","eigenvalues":"i gun values",
        "eigendirections":"i gun directions","summarise":"summarize","x":"ex","y":"why","i":"i"}
def norm(t):
    t = t.lower().replace("—"," ").replace("-"," ").replace("eigen directions","eigendirections")
    t = re.sub(r"[^a-z' ]"," ",t)
    out=[]
    for w in t.split():
        w = REPL.get(w,w)
        out += w.split()
    return out
def run(n):
    text = SCENES[n]["narration"]
    toks = norm(text)
    oov = [w for w in toks if w not in dic]
    if oov: print("OOV", n, oov)
    toks = [w for w in toks if w in dic]
    d = Decoder(samprate=16000, bestpath=False, beam=1e-80, wbeam=1e-60, pbeam=1e-80)
    with wave.open(f"audio_raw/scene{n}.16k.wav","rb") as w: data = w.readframes(w.getnframes())
    d.set_align_text(" ".join(toks))
    d.start_utt(); d.process_raw(data, full_utt=True); d.end_utt()
    print("hyp", n, (d.hyp().hypstr[:80] if d.hyp() else None))
    words = [[round(s.start_frame/100,2), round((s.end_frame+1)/100,2), s.word] for s in d.seg()]
    return words
res = {}
for n in range(1,7):
    w = run(n)
    res[n] = w
    sp = [x for x in w if x[2] not in ("<sil>","<s>","</s>")]
    print(n, len(sp), "first", sp[:3], "last", sp[-3:])
json.dump(res, open("align.json","w"))
