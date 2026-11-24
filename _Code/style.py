"""Shared colours, fonts and helper builders for the eigenvector video.

Colour code used throughout the video (consistent in every scene):
    A (the matrix)          -> blue
    v (a vector)            -> yellow
    lambda (the eigenvalue) -> orange
    I (identity matrix)     -> purple
    eigenvector for lambda=3, the line y = x   -> green
    eigenvector for lambda=1, the line y = -x  -> red/pink
"""
from manim import *
import numpy as np

STUDENT_NAME = "Sourav"
STUDENT_ID = "E25B070922"

BG = "#0E1117"
PANEL = "#161B26"
A_COL = "#58C4DD"
V_COL = "#FFD166"
L_COL = "#FF9F1C"
I_COL = "#B388FF"
E1_COL = "#06D6A0"   # lambda = 3, direction (1, 1)
E2_COL = "#EF476F"   # lambda = 1, direction (1, -1)
OFF_COL = "#F78C6B"  # "knocked off its line"
TXT = "#E8ECF1"
MUTED = "#8B95A5"
FONT = "Fira Sans"

A_MAT = np.array([[2.0, 1.0], [1.0, 2.0]])

config.background_color = BG
Text.set_default(font=FONT, color=TXT)
MathTex.set_default(color=TXT)

# tex part -> colour, used by ct()
COLMAP = {
    "A": A_COL, r"\mathbf{v}": V_COL, r"\lambda": L_COL, "I": I_COL,
    r"\lambda_1": L_COL, r"\lambda_2": L_COL, r"\lambda^{2}": L_COL,
    r"\mathbf{v}_1": E1_COL, r"\mathbf{v}_2": E2_COL, r"\checkmark": E1_COL,
}


def ct(*parts, fs=48, color=TXT):
    """Coloured MathTex: every part listed in COLMAP gets its colour."""
    m = MathTex(*parts, font_size=fs, color=color)
    for i, p in enumerate(parts):
        if p in COLMAP:
            m[i].set_color(COLMAP[p])
    return m


def _entry(s, **kw):
    return ct(*s.split("|"), fs=kw.get("font_size", 48))


def mat(rows, fs=48, h_buff=1.1, color=None):
    """Matrix whose entries may be split into coloured parts with '|', e.g. '2|-|\\lambda'."""
    m = Matrix(rows, element_to_mobject=_entry, element_to_mobject_config={"font_size": fs},
               h_buff=h_buff, v_buff=0.8 * fs / 48)
    if color:
        m.get_brackets().set_color(color)
    return m


def colvec(a, b, fs=40, color=TXT):
    return MathTex(r"\begin{bmatrix}%s\\%s\end{bmatrix}" % (a, b), font_size=fs, color=color)


def tag(mob, color=BG, opacity=0.85, buff=0.1):
    """Put a dark rounded backing behind a label so it stays readable over the grid."""
    bg = SurroundingRectangle(mob, buff=buff, corner_radius=0.08, stroke_width=0,
                              fill_color=color, fill_opacity=opacity)
    return VGroup(bg, mob)


def make_plane(O, u, xr=(-12, 12), yr=(-8, 8), opacity=0.5, width=1.6):
    plane = NumberPlane(
        x_range=[xr[0], xr[1], 1], y_range=[yr[0], yr[1], 1],
        x_length=(xr[1] - xr[0]) * u, y_length=(yr[1] - yr[0]) * u,
        background_line_style={"stroke_color": A_COL, "stroke_width": width, "stroke_opacity": opacity},
        axis_config={"stroke_color": TXT, "stroke_width": 2.5, "stroke_opacity": 0.9},
    )
    plane.shift(O - plane.c2p(0, 0))
    return plane


def P(O, u, v):
    """Plane coordinates (x, y) -> screen point, for a plane with origin O and unit length u."""
    return O + u * np.array([v[0], v[1], 0.0])


def arrow_at(O, u, v, color, op=1.0, sw=7):
    a = Arrow(O, P(O, u, v), buff=0, color=color, stroke_width=sw,
              max_tip_length_to_length_ratio=0.28, max_stroke_width_to_length_ratio=14)
    a.set_opacity(op)
    a.vec, a.col, a.op = np.array(v, dtype=float), color, op
    return a


def moved(arrow, O, u, M):
    """Target arrow after applying matrix M (keeps colour + opacity)."""
    return arrow_at(O, u, M @ arrow.vec, arrow.col, arrow.op, arrow.get_stroke_width())


def span_line(O, u, v, color, length=14, op=0.45, sw=2, dashed=True):
    d = np.array([v[0], v[1], 0.0]) / np.linalg.norm(v)
    cls = DashedLine if dashed else Line
    kw = {"dash_length": 0.14} if dashed else {}
    return cls(O - length * d, O + length * d, color=color, stroke_width=sw, stroke_opacity=op, **kw)


def chip(text):
    t = Text(text, font_size=22, color=MUTED)
    bg = RoundedRectangle(corner_radius=0.12, width=t.width + 0.4, height=t.height + 0.24,
                          fill_color=PANEL, fill_opacity=0.92, stroke_color="#2A3245", stroke_width=1.5)
    t.move_to(bg)
    g = VGroup(bg, t).to_corner(DL, buff=0.28)
    g.set_z_index(30)
    return g
