# How a session gets written

This is the working method that produced Sessions 1 and 2. It is written down
because the expensive part of this course is not typesetting — it is being right,
and Session 1 needed five rounds of review before it was fit to distribute.

---

## 1. What a session is made of

Not every session needs three documents. Decide first, because it changes what you
research.

| Document | When it earns its place |
|---|---|
| `notes.tex` | The default. A session whose content is a chain of theorems. |
| `problem-class.tex` | When the material is better *rebuilt* than exposed. Session 1 §2 became a problem class because Cybenko's proof is an assembly of M1 results the students already own — they can do it. |
| `lab.tex` + `lab/` | When a computation shows something words cannot. See §5 below: the test is whether one task **establishes** something rather than illustrating it. |

A problem class replaces part of the notes; it does not duplicate them. When
Session 1 §2 became a problem class, that section left the notes.

---

## 2. Order of operations

**Research first, typeset second.** Gather every theorem statement, constant and
citation *before* opening the `.tex`. The failure mode is specific and seductive:
starting to format anchors you on document mechanics while the content is still
soft, and errors get locked in behind nice typography.

1. Fix the mathematical spine of the session: the three or four statements it
   exists to deliver, and which are proved in full, which are quoted.
2. For every quoted result, **open the source**. Not a survey, not a blog, not
   memory. Session 1 quoted Gühring–Kutyniok–Petersen with one logarithm instead of
   two, `s ∈ {0,1}` instead of `s ∈ [0,1]`, and regularity `s ≥ 1` instead of
   `n ≥ 2` — all because the statement was reconstructed rather than read.
3. Run the numbers (§4).
4. Only then write.

---

## 3. Statement hygiene

Every item below corresponds to an error that was actually caught in review.

- **`≤` is not `=`.** Exhibiting a representing measure bounds the Barron seminorm
  from above and nothing more. Write `=` only with a matching lower bound —
  for `sin(Kx₁)` there is one, via the Lipschitz constant, and for the Gaussian
  there is not.
- **`O` is not `≍`.** Barron's theorem gives a *sufficient* width. Writing
  `n ≍ (rC/ε)²` silently promises a lower bound that no theorem provides. A
  Kolmogorov `n`-width, being an infimum over all linear methods, genuinely is
  two-sided — that is the exception, and it is worth pointing out to students.
- **Sufficient is not necessary.** `σ ∈ Cᵐ` is a clean sufficient condition for a
  classical strong residual. ReLU fails the hypotheses of Cybenko's theorem and
  still generates a dense class: a theorem's hypotheses often describe its proof
  rather than its truth, and saying so is good teaching.
- **Quantify over the right class.** "A polynomial activation is never universal"
  is false for the union over all depths and true at fixed depth. Always name the
  class a statement ranges over.
- **Attribute what you did not verify.** Where you have not read the literal
  statement, label the box *simplified asymptotic form* and add a remark saying
  what the real one contains. This is honest, and it is more useful than a
  confident paraphrase.
- **Endpoints are not decoration.** ReLU is precisely the exception in the
  `L^∞` non-closedness result; `p ∈ [1,∞]` quietly absorbed it.
- **Separate what is proved from what is observed.** Spectral bias is a theorem in
  the wide-network NTK regime and an observation outside it. Say which.

---

## 4. Verify every constant you assert

Three errors in Session 1 and 2 were arithmetic, and all three would have survived
any amount of rereading. A thirty-second computation caught each.

| Claimed | Correct | How it was caught |
|---|---|---|
| `(ReLU(wx+b))'' = w²δ` | `\|w\|δ` | jump of the first derivative, evaluated numerically for `w = ±3` |
| Taylor remainder `u⁴/12` | `u⁴/24` | it is `1/4!`, once per expansion |
| optimal step `h⁴ = 24εM₀/M₄` | `48εM₀/M₄` | one-dimensional minimisation, compared to the formula |

And one example was simply wrong: a "double well" `(x²−1)² + ½(x+1)²` whose
derivative factors as `(x+1)(2x−1)²` and therefore has a single minimum. Plotting
it would have taken a minute.

**Rule.** Any constant, any worked example, any numerical claim in the text gets
computed before it is written. `session-NN/lab/experiments.py` is the place for it,
even when the session has no lab.

---

## 5. When a lab is worth building

A lab that confirms what was just proved is pleasant and optional. A lab that
**establishes something no theorem of the session addresses** is worth a slot.

The test applied to Session 1: four tasks illustrate (gradient directions, the
degree bound, the nonconvexity segment, rank saturation), and one does not. Freezing
the inner parameters turns the loss into a convex least-squares problem, solved to
`1.4e-10` at `n = 256`; training all the parameters over the same class stalls at
`9.9e-03`. That gap is `E_app` against `E_opt`, measured two sessions before the
course has a name for it. The lab exists for that task; the other four are the
warm-up around it.

Two rules that follow:

- **Predict before you run.** Every task asks for a written prediction first. A
  computation that confirms teaches little; one that contradicts teaches a lot.
- **Invite the objection.** The last item of the decisive task asks students to
  attack the experiment — more steps, a schedule, L-BFGS. What survives their best
  effort is the lesson, and inviting the attack is what makes it a lesson rather
  than a demonstration.

---

## 6. The review loop

Write, then hand it to someone whose job is to find errors — a colleague, a
careful student, or an assistant you have explicitly instructed to be adversarial.
Then do it again. Session 1 took five passes:

1. structure and coverage
2. ten substantive mathematical errors, five critical
3. three remaining errors plus over-claiming
4. two corrections of scope and one false statement about Barron's class
5. two residual `≍`-for-`O` slips

Passes 2 and 3 are where the value is. Do not stop at one.

What a reviewer should be asked for, explicitly: wrong statements first, then
statements that are correct but stronger than their proof, then attributions, then
style. In that order — a reviewer who starts with style will not get to the
coefficient of the Dirac mass.

---

## 7. Mechanics

```sh
make new-session N=03 SLUG=pinn-method   # scaffold from session-template/
make                                      # teacher build
make student                              # student build
make release                              # dist/ for publication
```

Cross-references between sessions are textual, not `\ref` — the documents are
compiled separately. Cite as *"Session 1, Proposition 1.5"*, and get the numbers
from the `.aux`:

```sh
grep -E 'newlabel\{(prop|th|lem|rem|def|cor|ex):' session-01-*/notes.aux
```

Renumbering happens. After any substantial edit to a session, re-grep and check the
references pointing *into* it from later sessions.
