# Running the Session 1 problem class in ninety minutes

The sheet has seven exercises. **You cannot do seven exercises in ninety minutes**,
and pretending otherwise is how a problem class turns into a lecture delivered at
speed. What follows is the triage that works.

---

## What actually fits

| | | |
|---|---|---|
| 0–10 | **Ex. 1** — warm-up: the bump, and why it fails in `d ≥ 2` | pairs, then board |
| 10–25 | **Ex. 2** — polynomial activations | pairs, then board |
| 25–40 | **Ex. 3** — the Hahn–Banach skeleton | pairs, then board |
| 40–78 | **Ex. 4** — sigmoidal ⇒ discriminatory | the heart; see below |
| 78–88 | **Ex. 5** — assemble Cybenko, then read it critically | whole class |
| 88–90 | hand out what goes home | |

**Goes home: Exercises 6 and 7.** Exercise 6 (the smooth case of LLPS) is a full
session on its own — it is written out in detail precisely so that it can be done
alone. Exercise 7 probes the hypotheses and is the best homework on the sheet.

If you are running late, cut Exercise 2, not Exercise 3. Exercise 2 is
self-contained and genuinely doable alone; Exercise 3 is the scaffold that makes
Exercise 4 intelligible, and students who miss it will spend Exercise 4 wondering
where the measure came from.

---

## How to run each block

The pattern throughout: **8–10 minutes in pairs, then one student at the board**.
Not individual work — the exercises are written in numbered steps precisely so two
people can argue about step 3 while a third pair is still on step 2.

Three items are **whole-class discussion, not pair work**, and they are the ones
that carry the ideas:

- **Ex. 1, item 5** — why the one-dimensional staircase does not transpose to
  `d ≥ 2`. Ask for the answer out loud. Someone will say "take a product of
  bumps"; the answer is that `Σ(σ)` is a *linear span* and intersecting slabs is
  not a linear operation. That exchange is worth five minutes.
- **Ex. 4, Step 3 (item 11)** — auditing the hypotheses. Put *bounded*,
  *measurable*, *sigmoidal* on the board and have the room place each one. The
  punchline, that continuity is used nowhere in this exercise, should come from
  them.
- **Ex. 5, item 4** — ReLU does not satisfy Cybenko's hypotheses and still
  generates a dense class. The lesson is that a theorem's hypotheses often
  describe its proof rather than its truth. Say it explicitly; it is one of the
  most useful things a student takes from this session.

### Exercise 4 in detail — the only block that needs managing

Thirty-eight minutes, eleven numbered items. Split it at Step 2 and take stock on
the board in between, otherwise the fast pairs are at item 9 while others are at
item 3.

Two places where you should be ready to give the move rather than wait:

- **Item 1** — feeding `λw` and `λb + φ` back into the hypothesis. If nobody has it
  after three minutes, give it. It is bookkeeping, not insight, and the insight is
  downstream.
- **Item 4** — the two limits `φ → ±∞`. This is *the* clever step of the whole
  proof: the limit function does not depend on `φ`, but the expression does, and
  that is what makes two passages informative instead of one. Give it five minutes.
  If it has not come, do it at the board and make sure everyone sees why it works.

Item 5 is a one-line trap worth letting them fall into: the image of `K` under
`x ↦ w·x` is *contained in* a compact interval, not equal to one, because `K` may
be disconnected. Ask for an example. `K = {0} ∪ {1}` is the answer.

---

## Logistics

**What to print.** The handout — `session-01-problem-class-handout.pdf` — which is
the same sheet without §9. The hints in §8 *are* in the handout, deliberately:
they are on a separate page, and a student who turns to them has already decided to.

**When to distribute.** At the end of the previous session, not at the start of
this one. Say: "Part A is a warm-up, look at it before Friday if you have twenty
minutes." Those who do will carry the first fifteen minutes.

**The solutions.** Everything is public in this repository, including §9. That is
deliberate: the assessment is the mini-project, not the problem class, so the
solutions protect nothing that is graded. Tag the release *after* the session if
you would rather they not read ahead; the handout is what you put in their hands
either way.

---

## The lab

The computational lab is a *third* document and does not fit in the same slot.
Three options, in decreasing order of what they cost you:

1. **Its own session.** The honest choice if you can find an eleventh slot. See
   the pacing note at the end of `docs/syllabus.md`.
2. **Take-home, with ten minutes of demo.** Run Task 4 — the convex solve against
   full training — live at the end of the problem class. It takes two minutes to
   execute, the result is an eight-order-of-magnitude gap, and it is the single
   most useful thing in the lab. Then send them the notebook.
3. **Purely optional.** The notebook is self-contained and the solutions notebook
   carries the commentary; motivated students will do it.

Option 2 is what I would recommend. The lab exists for Task 4, and Task 4 survives
being shown rather than done — the other four tasks are the warm-up around it, and
they are genuinely better done alone at one's own pace.
