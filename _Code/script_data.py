TITLE = "Eigenvectors: The Directions a Matrix Doesn't Turn"
OBJECTIVE = ("By the end of this video, the viewer will be able to find the eigenvalues and "
             "eigenvectors of a 2x2 matrix and explain what they mean geometrically.")
MATRIX = "A = [[2, 1], [1, 2]]  →  eigenvalues 3 and 1, eigenvectors (1, 1) and (1, −1)"

SCENES = [
    {
        "n": "0", "name": "Opening Frame", "time": "0:00 – 0:06", "purpose": "Title card (no narration).",
        "visual": "Title, 'M3 · Linear Algebra', Student Name: Sourav, Student ID: E25B070922.",
        "math": "—",
        "narration": "(No narration — title on screen for 5 seconds.)",
    },
    {
        "n": "1", "name": "Hook / Context", "time": "0:06 – 0:32",
        "purpose": "Spark curiosity: why do some arrows not turn?",
        "visual": "Grid with 16 arrows and their dashed lines. A = [[2,1],[1,2]] acts; arrows knocked off their lines turn "
                  "coral, the diagonal arrows glow green/red and only stretch (rewind & replay). Question card, then "
                  "'Eigenvectors' with eigen (German) = 'own'.",
        "math": "Generic linear transformation of the plane.",
        "narration": (
            "Here's a puzzle. Take a matrix and apply it to the whole plane. Almost every arrow gets knocked "
            "off its line — it tilts and points somewhere new. But for many matrices, a few special directions "
            "don't turn at all. They only get longer or shorter. Which directions are these? And why do they "
            "matter so much that mathematicians gave them their own name?"
        ),
    },
    {
        "n": "2", "name": "Concept Introduction", "time": "0:32 – 1:24",
        "purpose": "Define eigenvector and eigenvalue; state the learning goal.",
        "visual": "Equation Av = λv written term by term, with A, v and λ labelled in consistent colours. "
                  "Small arrows show λ > 1 (stretch), 0 < λ < 1 (shrink), λ < 0 (flip).",
        "math": "A is n×n, v ≠ 0, Av = λv. λ is the eigenvalue (a scalar).",
        "narration": (
            "Let A be a square matrix, and v a non-zero vector. We call v an eigenvector of A if multiplying by A "
            "only scales it: A v equals lambda v. The number lambda is called the eigenvalue — it tells us how much "
            "the vector stretches. If lambda is bigger than one, it stretches. Between zero and one, it shrinks. "
            "If it's negative, the vector flips to point the opposite way. We need v to be non-zero, because the "
            "zero vector satisfies this for every lambda and tells us nothing. By the end of this video, you'll be "
            "able to find the eigenvalues and eigenvectors of a two by two matrix, and explain what they mean "
            "geometrically."
        ),
    },
    {
        "n": "3", "name": "Visual Intuition", "time": "1:24 – 2:09",
        "purpose": "Show eigen-directions geometrically before any algebra.",
        "visual": "Matrix A shown in corner. Grid transforms by A. Yellow vector (1,0) → (2,1) leaves its line "
                  "(dashed line stays behind). Green (1,1) → (3,3) stays on its line. Red (1,−1) stays fixed. "
                  "The two eigen-lines are highlighted.",
        "math": "A(1,0) = (2,1);  A(1,1) = (3,3);  A(1,−1) = (1,−1).",
        "narration": (
            "Let's watch this happen with the matrix A equals two, one, one, two. Here's the plane with a grid "
            "and a few vectors. When A acts, the whole grid stretches and slants. Watch the yellow vector, one "
            "zero. It lands at two one — it's been knocked off its original line. Most vectors behave like this. "
            "But look along the diagonal. The green vector, one one, lands on three three. Same line, just three "
            "times longer. And along the other diagonal, the red vector one, minus one, stays exactly where it "
            "is. These two lines are the eigen-directions of A. Every vector on them stays on them."
        ),
    },
    {
        "n": "4", "name": "Worked Example", "time": "2:09 – 4:10",
        "purpose": "Derive the characteristic equation and solve it step by step.",
        "visual": "Equations build line by line: Av = λv → (A − λI)v = 0 → det(A − λI) = 0. Then the 2×2 "
                  "determinant, expansion, factorisation, and two eigenvector solves. Final substitution checks "
                  "highlighted with ticks.",
        "math": ("(A − λI)v = 0, v ≠ 0  ⇒  det(A − λI) = 0.\n"
                 "det[[2−λ, 1],[1, 2−λ]] = (2−λ)² − 1 = λ² − 4λ + 3 = (λ−3)(λ−1) = 0  ⇒  λ = 3, 1.\n"
                 "λ=3: [[−1,1],[1,−1]]v = 0 ⇒ y = x ⇒ v = (1,1).\n"
                 "λ=1: [[1,1],[1,1]]v = 0 ⇒ y = −x ⇒ v = (1,−1).\n"
                 "Check: A(1,1) = (3,3) = 3(1,1) ✓;  A(1,−1) = (1,−1) = 1(1,−1) ✓."),
        "narration": (
            "Now let's find them with algebra. Start from A v equals lambda v. Move everything to one side: "
            "A v minus lambda v equals zero. To factor out v, we write lambda as lambda times the identity "
            "matrix I. So, A minus lambda I, times v, equals zero. "
            "We want a non-zero v that solves this. That's only possible if the matrix A minus lambda I squashes "
            "some direction down to zero — which means it isn't invertible, so its determinant must be zero. "
            "This is the characteristic equation: determinant of A minus lambda I equals zero. "
            "For our matrix, A minus lambda I is two minus lambda, one, one, two minus lambda. Its determinant "
            "is two minus lambda, squared, minus one. Expanding gives lambda squared, minus four lambda, plus "
            "three, equals zero. This factors as lambda minus three, times lambda minus one. So the eigenvalues "
            "are three and one. "
            "Now the eigenvectors. For lambda equals three, A minus three I is minus one, one, one, minus one. "
            "Both rows say y equals x, so the eigenvector is one one — or any non-zero multiple of it. "
            "For lambda equals one, A minus I is one, one, one, one. That gives x plus y equals zero, so y equals "
            "minus x, and the eigenvector is one, minus one. "
            "Let's check by substituting. A times one one is three three — that's three times one one. A times "
            "one, minus one is one, minus one — that's one times itself. Both check out."
        ),
    },
    {
        "n": "5", "name": "Interpretation", "time": "4:10 – 4:54",
        "purpose": "Connect the numbers back to the geometry.",
        "visual": "Eigen-lines drawn as the new 'axes': vectors on y = x stretch ×3, vectors on y = −x stay. (2,0) split "
                  "into (1,1) + (1,−1); after A it becomes 3(1,1) + (1,−1) = (4,2), which explains the tilt. Unit square → "
                  "parallelogram of area 3. Side panel: det A = 3 = λ₁λ₂, tr A = 4 = λ₁ + λ₂.",
        "math": "(2,0) = (1,1) + (1,−1)  ⇒  A(2,0) = 3(1,1) + 1(1,−1) = (4,2).\ndet A = 2·2 − 1·1 = 3 = λ₁λ₂;  tr A = 2 + 2 = 4 = λ₁ + λ₂.",
        "narration": (
            "So what do these numbers tell us? The matrix A is really doing two simple things at once. It "
            "stretches by a factor of three along the line y equals x, and it leaves the line y equals minus x "
            "completely unchanged. Every other vector is a mix of these two directions — that's why it seems to "
            "tilt. Notice two more things. The unit square's area gets multiplied by three — and three is exactly "
            "the determinant of A, which equals the product of the eigenvalues, three times one. And the trace "
            "of A, two plus two, is four — the sum of the eigenvalues. Eigenvectors are the natural axes of a "
            "transformation."
        ),
    },
    {
        "n": "6", "name": "Summary & Credits", "time": "4:54 – 5:35",
        "purpose": "Recap 3 takeaways; closing frame with credits and AI disclosure.",
        "visual": "Three numbered takeaways appear one by one, then a 'Thanks for watching!' end card. References and "
                  "AI disclosure are given in this storyboard and the repository README.",
        "math": "Av = λv;  det(A − λI) = 0;  (A − λI)v = 0.",
        "narration": (
            "To summarise. One: an eigenvector is a non-zero vector whose direction doesn't change under A — it's "
            "only scaled by its eigenvalue, lambda. Two: we find eigenvalues by solving determinant of A minus "
            "lambda I equals zero, and then eigenvectors by solving A minus lambda I, times v, equals zero. "
            "Three: eigenvectors are the natural axes of a transformation, and eigenvalues tell us how much it "
            "stretches along each one. Thanks for watching."
        ),
    },
]

CREDITS = [
    "References: Gilbert Strang, Introduction to Linear Algebra (Ch. 6, Eigenvalues and Eigenvectors); "
    "3Blue1Brown, Essence of Linear Algebra (visual inspiration only); M3 course lecture notes.",
    "Tools: Manim Community Edition (Python), FFmpeg, PocketSphinx (forced alignment for voice sync). No background music.",
    "AI disclosure: Script, storyboard and animation code were drafted with the help of Claude (Anthropic) and "
    "reviewed by the student. Narration is recorded in the student's own voice. All calculations verified by hand.",
]
