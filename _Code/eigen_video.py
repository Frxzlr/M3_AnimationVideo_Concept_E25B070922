"""
M3 Animation Video - "Eigenvectors: The Directions a Matrix Doesn't Turn"
Author: Sourav

Every animation is synced to the narration. cues.py looks up the time a phrase is
spoken (from a forced alignment of the recorded voice, align.json); self.at("phrase")
waits until that moment before the next animation starts.

Render one scene:   manim -qh --fps 30 --disable_caching eigen_video.py S3Intuition
Full build:         python build_video.py
"""
import os
import sys
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from style import *  # noqa: E402,F403
from cues import cue  # noqa: E402

A = A_MAT


def audio_len(n):
    with wave.open(os.path.join(HERE, "audio", f"scene{n}.wav")) as w:
        return w.getnframes() / w.getframerate()


class SyncedScene(Scene):
    N = None        # narration scene number (audio/sceneN.wav)
    CHIP = None     # small scene label shown bottom-left
    PAD = 0.4       # seconds of picture before the voice starts

    def setup(self):
        self.chip_m = None
        if self.CHIP:
            self.chip_m = chip(self.CHIP)
            self.add(self.chip_m)

    def now(self):
        return self.renderer.time

    def until(self, t):
        dt = t - self.now()
        if dt > 1e-3:
            self.wait(dt)
        elif dt < -0.3:
            print(f"[sync] {type(self).__name__}: {-dt:.2f}s late for t={t:.2f}")

    def T(self, phrase, after=0.0, end=False):
        return cue(self.N, phrase, after, end) + self.PAD

    def at(self, phrase, after=0.0, end=False, offset=0.0):
        t = self.T(phrase, after, end) + offset
        print(f"[cue] {type(self).__name__} {phrase!r} cue={t:.2f} now={self.now():.2f}")
        self.until(t)
        return t

    def outro(self, hold=0.35, fade=0.5):
        self.until(audio_len(self.N) + self.PAD + hold)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=fade)


# --------------------------------------------------------------------------- #
# 0. Opening frame
# --------------------------------------------------------------------------- #
class S0Title(Scene):
    def construct(self):
        O, u = np.array([0, 0, 0.0]), 0.9
        plane = make_plane(O, u, opacity=0.18, width=1.2)
        plane.axes.set_stroke(opacity=0.25)
        l1 = span_line(O, u, (1, 1), E1_COL, op=0.55, sw=3, dashed=False)
        l2 = span_line(O, u, (1, -1), E2_COL, op=0.55, sw=3, dashed=False)

        title = Text("Eigenvectors", font_size=96, weight=BOLD, gradient=(E1_COL, A_COL))
        sub = Text("The Directions a Matrix Doesn't Turn", font_size=40, color=TXT)
        course = Text("M3 · Linear Algebra & Calculus · Animation Video Project", font_size=26, color=MUTED)
        who = Text(f"{STUDENT_NAME}   ·   Student ID: {STUDENT_ID}", font_size=30, color=V_COL)
        block = VGroup(title, sub, course, who).arrange(DOWN, buff=0.32)
        sub.shift(0.05 * DOWN)
        course.shift(0.25 * DOWN)
        who.shift(0.25 * DOWN)
        back = RoundedRectangle(corner_radius=0.25, width=block.width + 1.2, height=block.height + 0.9,
                                fill_color=BG, fill_opacity=0.82, stroke_color="#2A3245", stroke_width=2)

        self.add(plane)
        self.play(Create(l1), Create(l2), FadeIn(back), run_time=0.8)
        self.play(Write(title), run_time=1.1)
        self.play(FadeIn(sub, shift=0.2 * UP), run_time=0.5)
        self.play(FadeIn(course), FadeIn(who), run_time=0.5)
        self.wait(2.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)


# --------------------------------------------------------------------------- #
# 1. Hook
# --------------------------------------------------------------------------- #
class S1Hook(SyncedScene):
    N, CHIP = 1, "1 · Hook"

    def construct(self):
        O, u = np.array([0.6, -0.25, 0.0]), 1.0
        ghost = make_plane(O, u, opacity=0.12, width=1.2)
        plane = make_plane(O, u)
        base = "#A9C6E8"
        angles = np.arange(0, 360, 22.5)
        dirs = [1.3 * np.array([np.cos(np.radians(a)), np.sin(np.radians(a))]) for a in angles]
        eig = [i for i, a in enumerate(angles) if a % 90 == 45]
        arrows = VGroup(*[arrow_at(O, u, d, base, sw=5) for d in dirs])
        spans = VGroup(*[span_line(O, u, d, base, op=0.28, sw=1.6) for d, a in zip(dirs, angles) if a < 180])
        span_eig = [k for k, a in enumerate([a for a in angles if a < 180]) if a % 90 == 45]

        self.play(FadeIn(ghost), FadeIn(plane), run_time=0.5)
        self.at("puzzle")
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.04),
                  FadeIn(spans), run_time=1.0)

        self.at("matrix")
        mlabel = tag(VGroup(ct("A", "="), mat([["2", "1"], ["1", "2"]], fs=44)).arrange(RIGHT, buff=0.2))
        mlabel.to_corner(UL, buff=0.45).set_z_index(10)
        self.play(FadeIn(mlabel, shift=0.3 * DOWN), run_time=0.6)

        self.at("apply")
        plane.save_state()
        for a in arrows:
            a.saved = a.copy()
        self.play(ApplyMatrix(A, plane, about_point=O),
                  *[Transform(a, moved(a, O, u, A)) for a in arrows], run_time=2.2)

        self.at("knocked")
        off = [a for i, a in enumerate(arrows) if i not in eig]
        self.play(*[a.animate.set_color(OFF_COL) for a in off],
                  spans.animate.set_stroke(opacity=0.6), run_time=0.7)
        self.at("tilts")
        self.play(LaggedStart(*[Wiggle(a, scale_value=1.06, rotation_angle=0.03 * TAU) for a in off],
                              lag_ratio=0.05), run_time=1.6)

        self.at("special")
        hi = []
        for i in eig:
            c = E1_COL if angles[i] in (45, 225) else E2_COL
            arrows[i].col = c
            hi.append(arrows[i].animate.set_color(c))
        for a in off:
            a.op, a.col = 0.15, OFF_COL
        sp_anims = []
        for k, s in enumerate(spans):
            if k in span_eig:
                sp_anims.append(s.animate.set_stroke(color=E1_COL if k == span_eig[0] else E2_COL,
                                                     opacity=0.9, width=2.6))
            else:
                sp_anims.append(s.animate.set_stroke(opacity=0.12))
        self.play(*hi, *[a.animate.set_opacity(0.15) for a in off], *sp_anims, run_time=0.9)
        self.at("turn")
        self.play(*[Indicate(arrows[i], scale_factor=1.15, color=arrows[i].col) for i in eig], run_time=0.6)

        # rewind and replay, now watching only the special arrows
        rw = tag(Text("rewind & replay", font_size=24, color=MUTED)).to_corner(UR, buff=0.4)
        self.at("they", after=14.5)
        self.play(Restore(plane),
                  *[Transform(a, arrow_at(O, u, a.saved.vec, a.col, a.op, 5)) for a in arrows],
                  FadeIn(rw), run_time=0.9)
        for a in arrows:
            a.vec = a.saved.vec
        self.at("longer")
        self.play(ApplyMatrix(A, plane, about_point=O),
                  *[Transform(a, moved(a, O, u, A)) for a in arrows], FadeOut(rw), run_time=1.6)

        self.at("which directions")
        veil = Rectangle(width=16, height=10, fill_color=BG, fill_opacity=0.78, stroke_width=0).set_z_index(15)
        q1 = Text("Which directions don't turn?", font_size=58, weight=BOLD).set_z_index(16)
        q1.shift(0.5 * UP)
        self.play(FadeIn(veil), Write(q1), run_time=1.0)
        self.at("why do they")
        q2 = Text("…and why do they matter?", font_size=38, color=MUTED).next_to(q1, DOWN, buff=0.4)
        q2.set_z_index(16)
        self.play(FadeIn(q2, shift=0.2 * UP), run_time=0.6)

        self.at("mathematicians")
        name = Text("Eigenvectors", font_size=110, weight=BOLD, gradient=(E1_COL, A_COL)).set_z_index(16)
        name.shift(0.4 * UP)
        self.play(FadeOut(q1, shift=0.3 * UP), FadeOut(q2, shift=0.3 * UP), run_time=0.35)
        self.play(FadeIn(name, scale=0.8), run_time=0.55)
        self.at("own")
        g = VGroup(Text("eigen", font_size=40, slant=ITALIC, color=TXT),
                   Text("(German)  =", font_size=34, color=MUTED),
                   Text("“own”", font_size=40, color=L_COL)).arrange(RIGHT, buff=0.25)
        g.next_to(name, DOWN, buff=0.45).set_z_index(16)
        self.play(FadeIn(g, shift=0.2 * UP), run_time=0.6)
        self.outro(hold=0.5)


# --------------------------------------------------------------------------- #
# 2. Concept introduction
# --------------------------------------------------------------------------- #
class S2Concept(SyncedScene):
    N, CHIP = 2, "2 · Concept"

    def construct(self):
        eq = ct("A", r"\mathbf{v}", "=", r"\lambda", r"\mathbf{v}", fs=120).move_to(1.3 * UP)

        def note(text, target, color, shift=0.0):
            t = Text(text, font_size=28, color=color, line_spacing=0.8)
            t.move_to(target.get_bottom() + 1.05 * DOWN + shift * RIGHT)
            line = Line(target.get_bottom() + 0.1 * DOWN, t.get_top() + 0.08 * UP,
                        color=color, stroke_width=2, stroke_opacity=0.7)
            return VGroup(line, t)

        self.at("square")
        nA = note("square matrix\n(n × n)", eq[0], A_COL, shift=-1.3)
        self.play(Write(eq[0]), FadeIn(nA), run_time=0.8)

        self.at("and v")
        nV = note("non-zero\nvector", eq[1], V_COL, shift=0.25)
        self.play(Write(eq[1]), FadeIn(nV), run_time=0.8)

        self.at("we call")
        nE = Text("eigenvector", font_size=32, color=V_COL, weight=BOLD).next_to(eq[1], UP, buff=0.35)
        self.play(FadeIn(nE, shift=0.2 * DOWN), Indicate(eq[1], color=V_COL), run_time=0.9)

        self.at("multiplying")
        self.play(Circumscribe(eq[0:2], color=A_COL, time_width=0.6), run_time=1.1)

        self.at("equals", after=11.0)
        self.play(Write(eq[2]), run_time=0.4)
        self.at("lambda", after=12.0)
        self.play(Write(eq[3]), run_time=0.35)
        self.at("v", after=12.7)
        self.play(Write(eq[4]), run_time=0.35)
        same = Text("same direction, only scaled", font_size=26, color=MUTED).next_to(eq[3:], UP, buff=0.45)
        same.shift(0.7 * RIGHT)
        self.play(FadeIn(same), run_time=0.5)

        self.at("lambda", after=14.5)
        self.play(Indicate(eq[3], color=L_COL, scale_factor=1.3), run_time=0.8)
        self.at("value", after=16.0)
        nL = note("eigenvalue\n(a scalar)", eq[3], L_COL, shift=0.1)
        self.play(FadeIn(nL), run_time=0.6)

        # three small demos: stretch / shrink / flip
        self.at("it tells")
        self.play(FadeOut(VGroup(nA, nV, nE, nL, same)),
                  eq.animate.scale(0.6).move_to(2.75 * UP), run_time=0.9)

        def panel(x, head, word, lam):
            box = RoundedRectangle(corner_radius=0.2, width=3.9, height=3.5, fill_color=PANEL,
                                   fill_opacity=1, stroke_color="#2A3245", stroke_width=2).move_to([x, -0.7, 0])
            h = MathTex(head, font_size=42, color=L_COL).move_to(box.get_top() + 0.45 * DOWN)
            c = box.get_center() + 0.25 * DOWN
            v = np.array([0.8, 0.38, 0])
            base = DashedLine(c - 1.75 * v / np.linalg.norm(v), c + 1.75 * v / np.linalg.norm(v),
                              dash_length=0.1, color=MUTED, stroke_width=1.5, stroke_opacity=0.6)
            ghost = Arrow(c, c + v, buff=0, color=MUTED, stroke_width=5, stroke_opacity=0.5,
                          max_tip_length_to_length_ratio=0.3)
            ghost.tip.set_fill(opacity=0.5)
            s = ValueTracker(1.0)

            def draw():
                k = s.get_value()
                k = k if abs(k) > 0.04 else 0.04 * (1 if k >= 0 else -1)
                return Arrow(c, c + k * v, buff=0, color=V_COL, stroke_width=7,
                             max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=20)
            arr = always_redraw(draw)
            lab = Text(word, font_size=28, color=TXT).move_to(box.get_bottom() + 0.4 * UP)
            val = MathTex(r"\lambda = %s" % lam, font_size=36, color=L_COL).next_to(lab, UP, buff=0.12)
            return VGroup(box, h, base, ghost), arr, s, VGroup(val, lab)

        demos = [(-4.4, r"\lambda > 1", "stretches", "2", 2.0, "stretches", 22.0),
                 (0.0, r"0 < \lambda < 1", "shrinks", r"\tfrac{1}{2}", 0.5, "shrinks", 25.0),
                 (4.4, r"\lambda < 0", "flips", "-1", -1.0, "flips", 28.0)]
        starts = ["bigger", "between", "negative"]
        made = []
        for (x, head, word, lam, k, cueword, aft), st in zip(demos, starts):
            self.at(st)
            stat, arr, s, labs = panel(x, head, word, lam)
            self.play(FadeIn(stat), FadeIn(arr), run_time=0.5)
            self.at(cueword, after=aft - 1.5)
            self.play(s.animate.set_value(k), FadeIn(labs, shift=0.15 * UP), run_time=1.2)
            made.append(VGroup(stat, labs, arr))

        self.at("we need")
        for m in made:
            m[2].clear_updaters()
        self.play(*[FadeOut(m) for m in made], run_time=0.6)
        self.at("non zero", after=32.5)
        nz = ct(r"\mathbf{v}", r"\neq", r"\mathbf{0}", fs=72).move_to(1.1 * UP)
        self.play(Write(nz), run_time=0.8)
        self.at("zero vector", after=35.0)
        zz = ct("A", r"\mathbf{0}", "=", r"\lambda", r"\mathbf{0}", r"\quad\text{for every }", r"\lambda", fs=50)
        zz.move_to(0.4 * DOWN)
        self.play(Write(zz), run_time=1.6)
        self.at("tells us nothing")
        nothing = Text("true for every λ  →  tells us nothing", font_size=30, color=OFF_COL)
        nothing.next_to(zz, DOWN, buff=0.45)
        self.play(FadeIn(nothing, shift=0.2 * UP), zz.animate.set_opacity(0.55), run_time=0.6)

        self.at("by the end")
        self.play(FadeOut(VGroup(nz, zz, nothing)), run_time=0.5)
        card = RoundedRectangle(corner_radius=0.25, width=12.6, height=3.0, fill_color=PANEL,
                                fill_opacity=1, stroke_color=E1_COL, stroke_width=2.5).move_to(0.6 * DOWN)
        gtag = Text("GOAL", font_size=24, weight=BOLD, color=BG)
        gbg = RoundedRectangle(corner_radius=0.1, width=gtag.width + 0.4, height=gtag.height + 0.2,
                               fill_color=E1_COL, fill_opacity=1, stroke_width=0)
        gtag.move_to(gbg)
        gt = VGroup(gbg, gtag).move_to(card.get_corner(UL) + np.array([0.8, 0, 0]))
        self.play(FadeIn(card), FadeIn(gt), run_time=0.6)
        self.at("find")
        g1 = Text("Find the eigenvalues and eigenvectors of a 2 × 2 matrix", font_size=34)
        g1.scale_to_fit_width(min(g1.width, 11.6)).move_to(card.get_center() + 0.45 * UP)
        self.play(Write(g1), run_time=1.6)
        self.at("explain")
        g2 = Text("…and explain what they mean geometrically.", font_size=34, color=E1_COL)
        g2.move_to(card.get_center() + 0.5 * DOWN)
        self.play(FadeIn(g2, shift=0.2 * UP), run_time=0.8)
        self.outro()


# --------------------------------------------------------------------------- #
# 3. Visual intuition
# --------------------------------------------------------------------------- #
class S3Intuition(SyncedScene):
    N, CHIP = 3, "3 · Visual intuition"

    def construct(self):
        O, u = np.array([0.9, -0.45, 0.0]), 0.85

        # the matrix, entries appear as they are spoken
        mA = mat([["2", "1"], ["1", "2"]], fs=60)
        lhs = ct("A", "=", fs=72)
        grp = VGroup(lhs, mA).arrange(RIGHT, buff=0.3).move_to(0.3 * UP).scale(1.2)
        self.at("matrix")
        self.play(Write(lhs), Create(mA.get_brackets()), run_time=0.7)
        ents = mA.get_entries()
        for e, (w, aft) in zip(ents, [("two", 3.0), ("one", 3.6), ("one", 4.0), ("two", 4.5)]):
            self.at(w, after=aft)
            self.play(FadeIn(e, scale=1.8), run_time=0.22)

        self.at("here's")
        ghost = make_plane(O, u, opacity=0.13, width=1.2)
        plane = make_plane(O, u)
        grp.set_z_index(21)
        self.play(grp.animate.scale(0.55).to_corner(UL, buff=0.5), run_time=0.8)
        mbox = SurroundingRectangle(grp, buff=0.2, corner_radius=0.12, fill_color=BG, fill_opacity=0.9,
                                    stroke_color=A_COL, stroke_width=2).set_z_index(20)
        self.play(FadeIn(ghost), Create(plane, lag_ratio=0.05), FadeIn(mbox), run_time=1.3)

        # three vectors and their (fixed) lines
        specs = [((1, 0), V_COL, UR), ((1, 1), E1_COL, UL), ((1, -1), E2_COL, DR)]
        arrs = [arrow_at(O, u, v, c) for v, c, _ in specs]
        lines = [span_line(O, u, v, c, op=0.5, sw=2) for v, c, _ in specs]
        self.at("few vectors")
        self.play(*[Create(l) for l in lines], LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.25),
                  run_time=1.0)

        def label(arr, txt, direction):
            a, b = txt
            return tag(colvec(a, b, fs=34, color=arr.col), opacity=0.8).next_to(arr.get_end(), direction,
                                                                                    buff=0.12)

        plane.save_state()
        for a in arrs:
            a.orig = a.vec.copy()
        live = list(arrs)

        def apply(rt=1.5, extra=()):
            self.play(ApplyMatrix(A, plane, about_point=O),
                      *[Transform(a, moved(a, O, u, A)) for a in live], *extra, run_time=rt)
            for a in live:
                a.vec = A @ a.vec

        rw = tag(Text("rewind", font_size=24, color=MUTED)).to_corner(UR, buff=0.4).set_z_index(20)

        def rewind(rt=0.8, extra=()):
            self.play(Restore(plane), *[Transform(a, arrow_at(O, u, a.orig, a.col, a.op, a.get_stroke_width()))
                                        for a in live],
                      FadeIn(rw, rate_func=there_and_back), *extra, run_time=rt)
            for a in live:
                a.vec = a.orig.copy()
            self.remove(rw)

        def focus(k, rt=0.5):
            anims = []
            for i, (a, l) in enumerate(zip(arrs, lines)):
                a.op = 1.0 if i == k else 0.18
                anims += [a.animate.set_opacity(a.op), l.animate.set_stroke(opacity=0.75 if i == k else 0.15)]
            self.play(*anims, run_time=rt)

        self.at("when")
        apply(rt=2.3)
        rewind(rt=0.8)

        # yellow: knocked off its line
        self.at("watch the yellow")
        focus(0)
        self.at("one zero")
        ly = label(arrs[0], ("1", "0"), UP)
        self.play(FadeIn(ly), run_time=0.4)
        self.at("lands")
        apply(rt=1.3, extra=[FadeOut(ly)])
        ly2 = label(arrs[0], ("2", "1"), UR)
        self.play(FadeIn(ly2), run_time=0.35)
        self.at("knocked")
        ang = Arc(radius=1.3, start_angle=0, angle=np.arctan2(1, 2), arc_center=O, color=OFF_COL, stroke_width=4)
        offt = tag(Text("knocked off its line", font_size=24, color=OFF_COL)).next_to(ang, DOWN, buff=0.15)
        offt.shift(0.9 * RIGHT)
        self.play(Create(ang), FadeIn(offt), lines[0].animate.set_stroke(opacity=1, width=3), run_time=0.8)

        # green: stays on its line, x3
        self.at("but look")
        rewind(rt=0.8, extra=[FadeOut(VGroup(ang, offt, ly2)), lines[0].animate.set_stroke(width=2)])
        focus(1)
        self.at("one one", after=26.0)
        lg = label(arrs[1], ("1", "1"), LEFT)
        self.play(FadeIn(lg), run_time=0.4)
        before_g = arrow_at(O, u, (1, 1), E1_COL, 0.35)
        self.at("lands", after=26.5)
        self.add(before_g)
        apply(rt=1.2, extra=[FadeOut(lg)])
        lg2 = label(arrs[1], ("3", "3"), RIGHT)
        self.play(FadeIn(lg2), run_time=0.35)
        self.at("same line")
        x3 = tag(MathTex(r"\times 3", font_size=48, color=E1_COL)).next_to(P(O, u, (2, 2)), DR, buff=0.15)
        self.play(lines[1].animate.set_stroke(opacity=1, width=3.5), run_time=0.6)
        self.at("three times")
        self.play(FadeIn(x3, scale=1.4), run_time=0.5)

        # red: stays exactly where it is
        self.at("and along")
        rewind(rt=0.8, extra=[FadeOut(VGroup(lg2, x3, before_g)), lines[1].animate.set_stroke(width=2)])
        focus(2)
        self.at("one minus one")
        lr = label(arrs[2], ("1", "-1"), RIGHT)
        self.play(FadeIn(lr), run_time=0.4)
        self.at("stays")
        apply(rt=1.3)
        x1 = tag(Text("×1 — unchanged", font_size=26, color=E2_COL)).next_to(lr, DOWN, buff=0.15)
        self.play(FadeIn(x1, shift=0.15 * UP), run_time=0.5)

        # the two eigen-directions
        self.at("these two")
        glow1 = span_line(O, u, (1, 1), E1_COL, op=0.25, sw=14, dashed=False)
        glow2 = span_line(O, u, (1, -1), E2_COL, op=0.25, sw=14, dashed=False)
        solid1 = span_line(O, u, (1, 1), E1_COL, op=1, sw=4, dashed=False)
        solid2 = span_line(O, u, (1, -1), E2_COL, op=1, sw=4, dashed=False)
        for a in arrs:
            a.op = 1.0
        live.remove(arrs[0])
        self.play(FadeOut(VGroup(lr, x1)), FadeOut(arrs[0]), lines[0].animate.set_stroke(opacity=0.1),
                  Create(glow1), Create(glow2), Create(solid1), Create(solid2),
                  arrs[1].animate.set_opacity(1), arrs[2].animate.set_opacity(1), run_time=1.0)
        self.at("directions")
        t1 = tag(Text("eigen-direction  (λ = 3)", font_size=26, color=E1_COL))
        t1.rotate(PI / 4).move_to(P(O, u, (-2.1, -2.1)) + np.array([0.27, -0.27, 0]))
        t2 = tag(Text("eigen-direction  (λ = 1)", font_size=26, color=E2_COL))
        t2.rotate(-PI / 4).move_to(P(O, u, (-2.3, 2.3)) + np.array([0.27, 0.27, 0]))
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.6)

        self.at("every")
        extra = [(0.5, 0.5), (-0.7, -0.7), (-0.35, -0.35), (-1.6, 1.6), (0.6, -0.6), (-0.8, 0.8), (1.6, -1.6)]
        smalls = [arrow_at(O, u, v, E1_COL if v[0] * v[1] > 0 else E2_COL, 1.0, sw=5) for v in extra]
        for s in smalls:
            s.orig = s.vec.copy()
        rewind(rt=0.6)
        self.play(LaggedStart(*[GrowArrow(s) for s in smalls], lag_ratio=0.08), run_time=0.5)
        live += smalls
        apply(rt=1.3)
        self.outro(hold=0.4)


# --------------------------------------------------------------------------- #
# 4. Worked example
# --------------------------------------------------------------------------- #
class S4Example(SyncedScene):
    N, CHIP = 4, "4 · Worked example"

    def construct(self):
        fs = 50
        head = Text("Finding them with algebra", font_size=36, weight=BOLD).to_edge(UP, buff=0.35)
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=0.7)

        X0 = -6.4

        def place(m, y):
            m.move_to([0, y, 0]).to_edge(LEFT, buff=0.0)
            m.shift((X0 - m.get_left()[0]) * RIGHT)
            return m

        L1 = place(ct("A", r"\mathbf{v}", "=", r"\lambda", r"\mathbf{v}", fs=fs), 2.25)
        L2 = place(ct("A", r"\mathbf{v}", "-", r"\lambda", r"\mathbf{v}", "=", r"\mathbf{0}", fs=fs), 1.15)
        L3 = place(ct("A", r"\mathbf{v}", "-", r"\lambda", "I", r"\mathbf{v}", "=", r"\mathbf{0}", fs=fs), 0.05)
        L4 = place(ct("(", "A", "-", r"\lambda", "I", ")", r"\mathbf{v}", "=", r"\mathbf{0}", fs=fs), -1.1)
        L5 = place(ct(r"\det", "(", "A", "-", r"\lambda", "I", ")", "=", "0", fs=fs), -2.55)

        self.at("a v", after=3.5)
        self.play(Write(L1), run_time=1.6)
        self.at("a v", after=9.0)
        self.play(TransformMatchingTex(L1.copy(), L2), run_time=1.6)
        self.at("factor out")
        self.play(Indicate(L2[1], color=V_COL, scale_factor=1.4), Indicate(L2[4], color=V_COL, scale_factor=1.4),
                  run_time=0.9)

        self.at("we write")
        side = VGroup(ct(r"\lambda", r"\mathbf{v}", "=", r"\lambda", "I", r"\mathbf{v}", fs=44),
                      VGroup(ct("I", "=", fs=44), mat([["1", "0"], ["0", "1"]], fs=40, color=I_COL)).arrange(RIGHT))
        side.arrange(DOWN, buff=0.35)
        sideb = RoundedRectangle(corner_radius=0.2, width=4.4, height=side.height + 0.6, fill_color=PANEL,
                                 fill_opacity=1, stroke_color=I_COL, stroke_width=2)
        sidetitle = Text("identity matrix", font_size=22, color=I_COL)
        sideg = VGroup(sideb, side).move_to([3.9, 1.2, 0])
        side.move_to(sideb)
        sidetitle.next_to(sideb, UP, buff=0.1)
        self.play(FadeIn(sideb), FadeIn(side[0]), run_time=0.7)
        self.at("identity")
        self.play(FadeIn(side[1]), FadeIn(sidetitle), run_time=0.7)
        self.play(TransformMatchingTex(L2.copy(), L3), run_time=0.9)

        self.at("so a minus")
        self.play(TransformMatchingTex(L3.copy(), L4), run_time=1.6)
        b4 = SurroundingRectangle(L4, buff=0.15, color=TXT, stroke_width=2, corner_radius=0.08)
        self.play(Create(b4), run_time=0.5)

        self.at("non zero")
        nz = ct(r"\mathbf{v}", r"\neq", r"\mathbf{0}", fs=44).next_to(b4, RIGHT, buff=0.4)
        self.play(FadeIn(nz, shift=0.2 * LEFT), run_time=0.5)

        # mini picture: a singular matrix squashes the plane onto a line
        self.at("that's only")
        self.play(FadeOut(sideg), FadeOut(sidetitle), run_time=0.5)
        bx = RoundedRectangle(corner_radius=0.2, width=5.0, height=3.8, fill_color=PANEL, fill_opacity=1,
                              stroke_color="#2A3245", stroke_width=2).move_to([3.95, 0.55, 0])
        Om, um = bx.get_center() + 0.15 * DOWN, 0.42
        mp = make_plane(Om, um, xr=(-5, 5), yr=(-3, 3), opacity=0.5, width=1.2)
        sq = Polygon(P(Om, um, (0, 0)), P(Om, um, (1, 0)), P(Om, um, (1, 1)), P(Om, um, (0, 1)),
                     fill_color=V_COL, fill_opacity=0.35, stroke_color=V_COL, stroke_width=2)
        vv = arrow_at(Om, um, (1, -2), V_COL, sw=6)
        cap = Text("A − λI squashes a direction to 0", font_size=24, color=MUTED).next_to(bx, DOWN, buff=0.15)
        self.play(FadeIn(bx), FadeIn(mp), FadeIn(sq), GrowArrow(vv), FadeIn(cap), run_time=0.8)
        S = np.array([[0.6, 0.3], [0.0, 0.0]])
        self.at("i", after=30.0)
        self.play(ApplyMatrix(S, mp, about_point=Om), ApplyMatrix(S, sq, about_point=Om),
                  vv.animate.scale(0.02, about_point=Om).set_opacity(0), run_time=2.2)
        dot = Dot(Om, color=V_COL, radius=0.07)
        self.add(dot)
        self.play(Flash(Om, color=V_COL, flash_radius=0.3), run_time=0.6)

        self.at("isn't")
        inv = Text("not invertible  ·  area → 0", font_size=26, color=OFF_COL).move_to(cap)
        self.play(ReplacementTransform(cap, inv), run_time=0.6)
        self.at("determinant", after=36.0)
        d0 = ct(r"\det(A-\lambda I) = 0", fs=40).next_to(bx, UP, buff=0.15)
        self.play(Write(d0), run_time=1.0)

        self.at("characteristic")
        ce = Text("characteristic equation", font_size=28, color=L_COL, weight=BOLD)
        ce.next_to(L5, UP, buff=0.22).align_to(L5, LEFT)
        self.play(FadeIn(ce, shift=0.15 * UP), run_time=0.6)
        self.at("determinant", after=42.0)
        self.play(Write(L5), run_time=2.0)
        b5 = SurroundingRectangle(L5, buff=0.18, color=L_COL, stroke_width=3, corner_radius=0.1)
        self.play(Create(b5), run_time=0.5)

        # ---- part B: solve for lambda ---- #
        self.at("our matrix", offset=-0.8)
        keep = VGroup(L5, b5)
        self.play(*[FadeOut(m) for m in [L1, L2, L3, L4, b4, nz, bx, mp, sq, vv, dot, inv, d0, ce, head]],
                  keep.animate.scale(0.85).move_to(3.15 * UP), run_time=0.9)

        Am = VGroup(ct("A", "=", fs=46), mat([["2", "1"], ["1", "2"]], fs=44)).arrange(RIGHT, buff=0.2)
        Am.move_to([-4.6, 1.55, 0])
        self.play(FadeIn(Am, shift=0.2 * RIGHT), run_time=0.6)

        self.at("a minus lambda i", after=48.0)
        lhs = ct("A", "-", r"\lambda", "I", "=", fs=46)
        M = mat([["2|-|\\lambda", "1"], ["1", "2|-|\\lambda"]], fs=44, h_buff=1.5)
        B2 = VGroup(lhs, M).arrange(RIGHT, buff=0.2).move_to([1.6, 1.55, 0])
        self.play(Write(lhs), Create(M.get_brackets()), run_time=0.8)
        ents = M.get_entries()
        for e, (w, aft) in zip(ents, [("two", 50.5), ("one", 51.8), ("one", 52.4), ("two", 52.7)]):
            self.at(w, after=aft)
            self.play(FadeIn(e, scale=1.5), run_time=0.3)

        self.at("its determinant", after=55.0)
        d1 = Line(ents[0].get_center(), ents[3].get_center(), color=E1_COL, stroke_width=5).set_opacity(0.55)
        d2 = Line(ents[1].get_center(), ents[2].get_center(), color=E2_COL, stroke_width=5).set_opacity(0.55)
        d1.set_z_index(-1), d2.set_z_index(-1)
        adbc = MathTex(r"ad - bc", font_size=34, color=MUTED).next_to(M, RIGHT, buff=0.35)
        self.play(Create(d1), Create(d2), FadeIn(adbc), run_time=0.9)

        B3 = ct(r"\det", "(", "A", "-", r"\lambda", "I", ")", "=", "(", "2", "-", r"\lambda", ")^2", "-", "1",
                fs=46).move_to([0, 0.15, 0])
        self.at("two", after=56.5)
        self.play(Write(B3), run_time=1.8)

        self.at("expanding")
        B4 = ct(r"\lambda^{2}", "-", "4", r"\lambda", "+", "3", "=", "0", fs=46).move_to([0, -0.95, 0])
        self.play(Write(B4), run_time=1.8)

        self.at("factors")
        B5 = ct("(", r"\lambda", "-", "3", ")", "(", r"\lambda", "-", "1", ")", "=", "0", fs=46).move_to([0, -2.0, 0])
        self.play(Write(B5), run_time=2.0)

        self.at("three", after=73.5)
        r1 = ct(r"\lambda_1", "=", "3", fs=52)
        r2 = ct(r"\lambda_2", "=", "1", fs=52)
        VGroup(r1, r2).arrange(RIGHT, buff=1.6).move_to([0, -3.15, 0])
        br1 = SurroundingRectangle(r1, buff=0.15, color=E1_COL, stroke_width=3, corner_radius=0.1)
        br2 = SurroundingRectangle(r2, buff=0.15, color=E2_COL, stroke_width=3, corner_radius=0.1)
        self.play(Write(r1), Create(br1), run_time=0.6)
        self.at("one", after=74.4)
        self.play(Write(r2), Create(br2), run_time=0.6)

        # ---- part C: eigenvectors ---- #
        self.at("now the")
        g1, g2 = VGroup(r1, br1), VGroup(r2, br2)
        head2 = VGroup(Text("Eigenvectors: solve", font_size=34, weight=BOLD),
                       ct("(", "A", "-", r"\lambda", "I", ")", r"\mathbf{v}", "=", r"\mathbf{0}", fs=44))
        head2.arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.35)
        div = DashedLine([0, 2.5, 0], [0, -3.4, 0], color="#2A3245", stroke_width=2)
        self.play(FadeOut(VGroup(keep, Am, B2, d1, d2, adbc, B3, B4, B5)), FadeIn(head2),
                  g1.animate.move_to([-3.5, 2.2, 0]), g2.animate.move_to([3.5, 2.2, 0]), Create(div),
                  run_time=1.0)

        def column(x, k, rows, after_lhs, entry_cues):
            lhs = ct("A", "-", k, "I", "=", fs=44) if k != "1" else ct("A", "-", "I", "=", fs=44)
            m = mat(rows, fs=42, h_buff=1.1)
            g = VGroup(lhs, m).arrange(RIGHT, buff=0.2).move_to([x, 0.9, 0])
            return lhs, m, g

        # lambda = 3
        self.at("for lambda equals three")
        self.play(Indicate(g1, color=E1_COL, scale_factor=1.08), run_time=0.7)
        lhsA, mA3, gA = column(-3.5, "3", [["-1", "1"], ["1", "-1"]], None, None)
        self.at("a minus three")
        self.play(Write(lhsA), Create(mA3.get_brackets()), run_time=0.7)
        for e, (w, aft) in zip(mA3.get_entries(), [("minus", 80.8), ("one", 81.7), ("one", 82.1), ("minus", 82.4)]):
            self.at(w, after=aft)
            self.play(FadeIn(e, scale=1.5), run_time=0.25)
        self.at("both rows")
        rows = mA3.get_rows()
        self.play(Indicate(rows[0], color=E1_COL), Indicate(rows[1], color=E1_COL), run_time=0.8)
        eqA = ct("-x", "+", "y", "=", "0", r"\;\Rightarrow\;", "y", "=", "x", fs=44).move_to([-3.5, -0.45, 0])
        self.play(Write(eqA), run_time=1.3)
        self.at("one one", after=87.0)
        vA = VGroup(ct(r"\mathbf{v}_1", "=", fs=50), colvec("1", "1", fs=48, color=E1_COL)).arrange(RIGHT, buff=0.2)
        vA.move_to([-3.5, -1.75, 0])
        bvA = SurroundingRectangle(vA, buff=0.15, color=E1_COL, stroke_width=3, corner_radius=0.1)
        self.play(Write(vA), Create(bvA), run_time=0.8)
        self.at("or any")
        anyA = Text("(or any non-zero multiple of it)", font_size=24, color=MUTED).next_to(bvA, DOWN, buff=0.2)
        self.play(FadeIn(anyA), run_time=0.6)

        # lambda = 1
        self.at("for lambda equals one")
        self.play(Indicate(g2, color=E2_COL, scale_factor=1.08), run_time=0.7)
        lhsB, mB1, gB = column(3.5, "1", [["1", "1"], ["1", "1"]], None, None)
        self.at("a minus i")
        self.play(Write(lhsB), Create(mB1.get_brackets()), run_time=0.6)
        for e, (w, aft) in zip(mB1.get_entries(), [("one", 94.1), ("one", 94.5), ("one", 94.9), ("one", 95.2)]):
            self.at(w, after=aft)
            self.play(FadeIn(e, scale=1.5), run_time=0.22)
        self.at("gives", after=95.0)
        eqB1 = ct("x", "+", "y", "=", "0", fs=44)
        eqB2 = ct(r"\;\Rightarrow\;", "y", "=", "-x", fs=44)
        VGroup(eqB1, eqB2).arrange(RIGHT, buff=0.3).move_to([3.5, -0.45, 0])
        self.play(Write(eqB1), run_time=1.2)
        self.at("so why")
        self.play(Write(eqB2), run_time=1.0)
        self.at("one minus one", after=102.0)
        vB = VGroup(ct(r"\mathbf{v}_2", "=", fs=50), colvec("1", "-1", fs=48, color=E2_COL)).arrange(RIGHT, buff=0.2)
        vB.move_to([3.5, -1.75, 0])
        bvB = SurroundingRectangle(vB, buff=0.15, color=E2_COL, stroke_width=3, corner_radius=0.1)
        self.play(Write(vB), Create(bvB), run_time=0.8)

        # ---- part D: check ---- #
        self.at("let's check")
        head3 = VGroup(Text("Check by substituting:", font_size=34, weight=BOLD),
                       ct("A", r"\mathbf{v}", "=", r"\lambda", r"\mathbf{v}", fs=46)).arrange(RIGHT, buff=0.3)
        head3.to_edge(UP, buff=0.45)
        self.play(FadeOut(VGroup(head2, div, g1, g2, gA, eqA, vA, bvA, anyA, gB, eqB1, eqB2, vB, bvB)),
                  FadeIn(head3), run_time=0.9)

        def check_line(v, res, lam, col, y):
            Mx = mat([["2", "1"], ["1", "2"]], fs=44, color=A_COL)
            parts = [Mx, colvec(*v, fs=46, color=col), MathTex("=", font_size=50),
                     colvec(*res, fs=46), MathTex("=", font_size=50),
                     VGroup(MathTex(lam, font_size=50, color=L_COL), colvec(*v, fs=46, color=col)).arrange(RIGHT, buff=0.1),
                     MathTex(r"\checkmark", font_size=64, color=E1_COL)]
            g = VGroup(*parts).arrange(RIGHT, buff=0.3).move_to([0, y, 0])
            parts[-1].shift(0.25 * RIGHT)
            return parts

        c1 = check_line(("1", "1"), ("3", "3"), "3", E1_COL, 0.9)
        c2 = check_line(("1", "-1"), ("1", "-1"), "1", E2_COL, -1.5)
        for parts, cues_ in [(c1, [("a times", 107.0), ("three", 108.6), ("that's", 109.7), ("one one", 111.2)]),
                             (c2, [("a times", 112.5), ("one", 114.6), ("that's", 116.3), ("itself", 117.6)])]:
            self.at(*cues_[0])
            self.play(FadeIn(VGroup(parts[0], parts[1]), shift=0.2 * RIGHT), run_time=0.6)
            self.at(*cues_[1])
            self.play(FadeIn(parts[2]), FadeIn(parts[3], shift=0.2 * LEFT), run_time=0.5)
            self.at(*cues_[2])
            self.play(FadeIn(parts[4]), FadeIn(parts[5], shift=0.2 * LEFT), run_time=0.5)
            self.at(*cues_[3], end=True)
            self.play(FadeIn(parts[6], scale=1.6), run_time=0.4)

        self.at("both check")
        self.play(Circumscribe(VGroup(*c1), color=E1_COL, time_width=0.7),
                  Circumscribe(VGroup(*c2), color=E1_COL, time_width=0.7), run_time=1.0)
        self.outro()


# --------------------------------------------------------------------------- #
# 5. Interpretation
# --------------------------------------------------------------------------- #
class S5Interpretation(SyncedScene):
    N, CHIP = 5, "5 · Interpretation"

    def construct(self):
        O, u = np.array([-3.35, -0.55, 0.0]), 0.85
        ghost = make_plane(O, u, opacity=0.12, width=1.2)
        plane = make_plane(O, u)
        e1 = span_line(O, u, (1, 1), E1_COL, op=0.85, sw=3, dashed=False)
        e2 = span_line(O, u, (1, -1), E2_COL, op=0.85, sw=3, dashed=False)

        panel = RoundedRectangle(corner_radius=0.25, width=6.3, height=7.4, fill_color=PANEL, fill_opacity=0.97,
                                 stroke_color="#2A3245", stroke_width=2).move_to([3.85, 0, 0]).set_z_index(10)
        PX = 3.85

        def pz(m):
            return m.set_z_index(11)

        self.play(FadeIn(ghost), Create(plane, lag_ratio=0.05), Create(e1), Create(e2), FadeIn(panel), run_time=1.3)
        self.at("the matrix")
        h = pz(Text("What A really does", font_size=32, weight=BOLD, t2c={"A": A_COL})).move_to([PX, 3.2, 0])
        self.play(FadeIn(h, shift=0.15 * DOWN), run_time=0.6)

        # 1) stretch x3 along y = x
        self.at("it stretches")
        i1 = pz(VGroup(Text("1", font_size=28, weight=BOLD, color=E1_COL),
                       Text("stretch ×3 along  y = x", font_size=28, color=E1_COL)).arrange(RIGHT, buff=0.3))
        i1.move_to([PX, 2.35, 0])
        gs = [arrow_at(O, u, (1, 1), E1_COL), arrow_at(O, u, (-0.7, -0.7), E1_COL)]
        self.play(FadeIn(i1), *[GrowArrow(a) for a in gs], run_time=0.6)
        self.at("factor")
        self.play(*[Transform(a, moved(a, O, u, A)) for a in gs], e1.animate.set_stroke(width=6), run_time=1.3)

        # 2) keep y = -x fixed
        self.at("and it leaves")
        i2 = pz(VGroup(Text("2", font_size=28, weight=BOLD, color=E2_COL),
                       Text("keep  y = −x  fixed  (×1)", font_size=28, color=E2_COL)).arrange(RIGHT, buff=0.3))
        i2.move_to([PX, 1.7, 0]).align_to(i1, LEFT)
        rs = [arrow_at(O, u, (1, -1), E2_COL), arrow_at(O, u, (-0.8, 0.8), E2_COL)]
        self.play(FadeIn(i2), *[GrowArrow(a) for a in rs], e1.animate.set_stroke(width=3), run_time=0.6)
        self.at("unchanged")
        self.play(*[Indicate(a, color=E2_COL, scale_factor=1.1) for a in rs], e2.animate.set_stroke(width=6),
                  run_time=1.0)

        # every other vector = mix of the two
        self.at("every other")
        self.play(*[FadeOut(a) for a in gs + rs], e2.animate.set_stroke(width=3), run_time=0.4)
        y0 = arrow_at(O, u, (2, 0), V_COL)
        self.play(GrowArrow(y0), run_time=0.5)
        self.at("mix")
        cg = arrow_at(O, u, (1, 1), E1_COL, sw=6)
        cr = Arrow(P(O, u, (1, 1)), P(O, u, (2, 0)), buff=0, color=E2_COL, stroke_width=6,
                   max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=14)
        para = DashedVMobject(Polygon(P(O, u, (0, 0)), P(O, u, (1, 1)), P(O, u, (2, 0)), P(O, u, (1, -1))),
                              num_dashes=30).set_stroke(MUTED, 1.5, opacity=0.8)
        mixeq = pz(VGroup(colvec("2", "0", fs=38, color=V_COL), MathTex("=", font_size=44),
                          colvec("1", "1", fs=38, color=E1_COL),
                          MathTex("+", font_size=44),
                          colvec("1", "-1", fs=38, color=E2_COL)).arrange(RIGHT, buff=0.18))
        mixeq.move_to([PX, 0.45, 0])
        self.play(GrowArrow(cg), Create(para), run_time=0.7)
        self.play(GrowArrow(cr), Write(mixeq), run_time=1.0)

        self.at("that's why")
        plane.save_state()
        cg_t = arrow_at(O, u, (3, 3), E1_COL, sw=6)
        cr_t = Arrow(P(O, u, (3, 3)), P(O, u, (4, 2)), buff=0, color=E2_COL, stroke_width=6,
                     max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=14)
        para_t = DashedVMobject(Polygon(P(O, u, (0, 0)), P(O, u, (3, 3)), P(O, u, (4, 2)), P(O, u, (1, -1))),
                                num_dashes=40).set_stroke(MUTED, 1.5, opacity=0.8)
        res = pz(VGroup(MathTex("A", font_size=44, color=A_COL), colvec("2", "0", fs=38, color=V_COL),
                        MathTex("=", font_size=44), MathTex("3", font_size=44, color=L_COL),
                        colvec("1", "1", fs=38, color=E1_COL), MathTex("+", font_size=44),
                        MathTex("1", font_size=44, color=L_COL),
                        colvec("1", "-1", fs=38, color=E2_COL), MathTex("=", font_size=44),
                        colvec("4", "2", fs=38, color=V_COL)).arrange(RIGHT, buff=0.14))
        res.scale_to_fit_width(min(res.width, 5.8)).move_to([PX, -0.75, 0])
        res2 = pz(Text("yellow tilts: only its green part stretches", font_size=24, color=MUTED))
        res2.scale_to_fit_width(min(res2.width, 5.5)).next_to(res, DOWN, buff=0.3)
        self.play(ApplyMatrix(A, plane, about_point=O), Transform(cg, cg_t), Transform(cr, cr_t),
                  Transform(para, para_t), Transform(y0, arrow_at(O, u, (4, 2), V_COL)), Write(res), run_time=1.6)
        self.play(FadeIn(res2), run_time=0.4)

        # area and determinant, trace
        self.at("notice")
        self.play(FadeOut(VGroup(cg, cr, para, y0, i1, i2, mixeq, res, res2)), Restore(plane), run_time=0.8)
        self.at("unit")
        sq = Polygon(P(O, u, (0, 0)), P(O, u, (1, 0)), P(O, u, (1, 1)), P(O, u, (0, 1)), fill_color=V_COL,
                     fill_opacity=0.45, stroke_color=V_COL, stroke_width=3)
        a1 = tag(MathTex(r"\text{area} = 1", font_size=32, color=V_COL)).next_to(sq, DL, buff=0.1)
        self.play(DrawBorderThenFill(sq), FadeIn(a1), run_time=0.8)
        self.at("multiplied")
        a3 = tag(MathTex(r"\text{area} = 3", font_size=36, color=V_COL)).move_to(P(O, u, (1.5, 1.5)))
        self.play(ApplyMatrix(A, plane, about_point=O), ApplyMatrix(A, sq, about_point=O),
                  FadeOut(a1), run_time=1.4)
        self.play(FadeIn(a3, scale=1.3), run_time=0.4)

        self.at("determinant")
        dA = pz(ct(r"\det A", "=", r"2\cdot 2 - 1\cdot 1", "=", "3", fs=44)).move_to([PX, 1.9, 0])
        self.play(Write(dA), run_time=1.3)
        self.at("product")
        dB = pz(ct("=", r"\lambda_1 \lambda_2", "=", r"3 \times 1", fs=44))
        dB.next_to(dA, DOWN, buff=0.35).align_to(dA[1], LEFT)
        self.play(Write(dB), run_time=1.3)
        bd = pz(SurroundingRectangle(VGroup(dA, dB), buff=0.2, color=V_COL, stroke_width=2, corner_radius=0.12))
        self.play(Create(bd), run_time=0.5)

        self.at("trace")
        tA = pz(ct(r"\operatorname{tr} A", "=", "2 + 2", "=", "4", fs=44)).move_to([PX, -0.7, 0])
        self.play(Write(tA), run_time=1.5)
        self.at("sum")
        tB = pz(ct("=", r"\lambda_1 + \lambda_2", "=", "3 + 1", fs=44))
        tB.next_to(tA, DOWN, buff=0.35).align_to(tA[1], LEFT)
        self.play(Write(tB), run_time=1.2)
        bt = pz(SurroundingRectangle(VGroup(tA, tB), buff=0.2, color=L_COL, stroke_width=2, corner_radius=0.12))
        self.play(Create(bt), run_time=0.5)

        self.at("vectors are the")
        ban = Text("Eigenvectors are the natural axes of a transformation", font_size=30, weight=BOLD,
                   gradient=(E1_COL, A_COL))
        banb = RoundedRectangle(corner_radius=0.2, width=ban.width + 0.7, height=ban.height + 0.45, fill_color=BG,
                                fill_opacity=0.95, stroke_color=E1_COL, stroke_width=2)
        ban.move_to(banb)
        bang = VGroup(banb, ban).move_to([0, -3.35, 0]).set_z_index(25)
        self.play(FadeIn(bang, shift=0.2 * UP), FadeOut(self.chip_m), e1.animate.set_stroke(width=7),
                  e2.animate.set_stroke(width=7), run_time=0.9)
        self.outro()


# --------------------------------------------------------------------------- #
# 6. Summary + closing frame
# --------------------------------------------------------------------------- #
class S6Summary(SyncedScene):
    N, CHIP = 6, "6 · Summary"

    def construct(self):
        head = Text("Summary", font_size=46, weight=BOLD).to_edge(UP, buff=0.4)
        self.play(FadeIn(head, shift=0.2 * DOWN), run_time=0.6)

        def card(y, num, color):
            b = RoundedRectangle(corner_radius=0.22, width=12.6, height=1.85, fill_color=PANEL, fill_opacity=1,
                                 stroke_color=color, stroke_width=2.5).move_to([0, y, 0])
            c = Circle(radius=0.36, fill_color=color, fill_opacity=1, stroke_width=0)
            c.move_to(b.get_left() + 0.75 * RIGHT)
            n = Text(num, font_size=34, weight=BOLD, color=BG).move_to(c)
            return b, VGroup(c, n)

        ys = [1.85, -0.25, -2.35]
        cols = [V_COL, L_COL, E1_COL]

        # 1
        self.at("one")
        b1, n1 = card(ys[0], "1", cols[0])
        t1 = Text("An eigenvector is a non-zero vector whose direction A doesn't change",
                  font_size=29, t2c={" A ": A_COL})
        t1.scale_to_fit_width(min(t1.width, 10.6)).move_to(b1.get_center() + 0.4 * UP + 0.35 * RIGHT)
        self.play(FadeIn(b1), FadeIn(n1, scale=0.6), run_time=0.5)
        self.play(Write(t1), run_time=1.8)
        self.at("only scaled")
        e1 = VGroup(Text("it is only scaled:", font_size=27, color=MUTED),
                    ct("A", r"\mathbf{v}", "=", r"\lambda", r"\mathbf{v}", fs=44)).arrange(RIGHT, buff=0.3)
        e1.move_to(b1.get_center() + 0.4 * DOWN + 0.35 * RIGHT)
        self.play(FadeIn(e1, shift=0.15 * UP), run_time=0.7)

        # 2
        self.at("two")
        b2, n2 = card(ys[1], "2", cols[1])
        r1 = VGroup(Text("eigenvalues:", font_size=27, color=MUTED),
                    ct(r"\det", "(", "A", "-", r"\lambda", "I", ")", "=", "0", fs=44)).arrange(RIGHT, buff=0.3)
        r2 = VGroup(Text("then eigenvectors:", font_size=27, color=MUTED),
                    ct("(", "A", "-", r"\lambda", "I", ")", r"\mathbf{v}", "=", r"\mathbf{0}", fs=44)).arrange(RIGHT, buff=0.3)
        VGroup(r1, r2).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(b2.get_center() + 0.35 * RIGHT)
        self.play(FadeIn(b2), FadeIn(n2, scale=0.6), run_time=0.5)
        self.at("determinant")
        self.play(FadeIn(r1, shift=0.15 * UP), run_time=0.8)
        self.at("then")
        self.play(FadeIn(r2, shift=0.15 * UP), run_time=0.8)

        # 3
        self.at("three")
        b3, n3 = card(ys[2], "3", cols[2])
        t3a = Text("Eigenvectors are the natural axes of a transformation;", font_size=27)
        t3b = Text("eigenvalues tell how much it stretches along each one.", font_size=27, color=MUTED)
        VGroup(t3a, t3b).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(b3.get_center() + 0.35 * RIGHT)
        self.play(FadeIn(b3), FadeIn(n3, scale=0.6), run_time=0.5)
        self.play(Write(t3a), run_time=1.5)
        self.at("and", after=24.5)
        self.play(FadeIn(t3b, shift=0.15 * UP), run_time=0.8)

        self.at("thanks")
        thanks = Text("Thanks for watching!", font_size=60, weight=BOLD, gradient=(E1_COL, A_COL))
        allc = VGroup(head, b1, n1, t1, e1, b2, n2, r1, r2, b3, n3, t3a, t3b)
        self.play(allc.animate.set_opacity(0.15), FadeIn(thanks, scale=0.85), run_time=0.8)

        # closing frame: credits & disclosure
        self.until(audio_len(self.N) + self.PAD + 0.6)
        self.play(FadeOut(allc), FadeOut(self.chip_m), thanks.animate.scale(0.6).to_edge(UP, buff=0.4), run_time=0.8)
        ttl = Text("Credits & Disclosure", font_size=36, weight=BOLD, color=TXT).next_to(thanks, DOWN, buff=0.35)

        def row(k, v, kc):
            return VGroup(Text(k, font_size=24, weight=BOLD, color=kc),
                          Text(v, font_size=23, color=TXT, line_spacing=0.9)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        rows = [
            row("Student", f"{STUDENT_NAME}  ·  Student ID: {STUDENT_ID}  ·  M3 Animation Video Project", V_COL),
            row("References", "Gilbert Strang, Introduction to Linear Algebra, Ch. 6 (Eigenvalues and Eigenvectors)\n"
                              "3Blue1Brown, Essence of Linear Algebra (visual inspiration only)  ·  M3 lecture notes", A_COL),
            row("Tools", "Manim Community Edition (Python)  ·  FFmpeg  ·  PocketSphinx (voice-to-animation sync)", E1_COL),
            row("AI disclosure", "Script, storyboard and animation code drafted with Claude (Anthropic) and\n"
                                 "reviewed by the student. Narration recorded in the student's own voice.\n"
                                 "All calculations verified by hand. No background music.", L_COL),
        ]
        body = VGroup(*rows).arrange(DOWN, buff=0.32, aligned_edge=LEFT).next_to(ttl, DOWN, buff=0.4)
        body.shift(-body.get_center()[0] * RIGHT)
        self.play(FadeIn(ttl), LaggedStart(*[FadeIn(r, shift=0.15 * UP) for r in rows], lag_ratio=0.25), run_time=1.6)
        self.wait(7.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
