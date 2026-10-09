# Physics-Informed Neural Networks for PDEs

Lecture notes, problem classes and computational labs for **M2 MACIA**,
AGM — CY Cergy Paris University. Paul Boureau.

Ten ninety-minute sessions on what can and cannot be proved about solving partial
differential equations with neural networks. The entry point assumes a solid M1 in
mathematics and **no prior exposure to machine learning**: the class of networks is
built from scratch in Session 1, as an object of approximation theory.

The organising principle is a distinction the field often blurs — between what is
**proved**, what is **observed**, and what is merely **asserted**. Theorems quoted
without having been read in the original are labelled as such. Every constant
asserted in the text was computed before it was written.

---

## Download

Permanent links, always pointing at the latest release:

| Session | Notes | Problem class | Lab |
|---|---|---|---|
| 1 — The neural network as an approximation class | [pdf](../../releases/latest/download/session-01-notes.pdf) | [pdf](../../releases/latest/download/session-01-problem-class.pdf) | [pdf](../../releases/latest/download/session-01-lab.pdf) |
| 2 — Automatic differentiation and nonconvex optimisation | [pdf](../../releases/latest/download/session-02-notes.pdf) | — | — |
| 3–10 | *in preparation* | | |

Each document also comes as a `-handout.pdf`: the same text with the solutions
removed, which is what gets printed for the session itself. See
[`docs/syllabus.md`](docs/syllabus.md) for the full ten-session plan.

## Labs

Open a lab in Google Colab — nothing to install:

[![Session 1 lab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/api-pbe/pinns-m2-macia/blob/main/session-01-approximation-class/lab/lab1-student.ipynb)

Or locally:

```sh
pip install -r requirements.txt
jupyter lab session-01-approximation-class/lab/
```

CPU only; no GPU is used anywhere in this course. The labs set
`torch.set_default_dtype(torch.float64)` at the top, and this matters: several
tasks measure errors below `1e-8`, which single precision cannot represent.

---

## Building from source

Requires TeX Live and Python 3.

```sh
make                                      # every document, with solutions
make handout                              # every document, solutions stripped
make notebooks                            # regenerate the lab notebooks
make release                              # everything, collected into dist/
make new-session N=03 SLUG=pinn-method    # scaffold the next session
make clean
```

### How the two variants stay consistent

One source per document. `common/pinns-course.sty` defines

```latex
\newif\ifsolutions
\ifdefined\HandoutBuild \solutionsfalse \else \solutionstrue \fi
```

and every solutions section is wrapped in `\ifsolutions ... \fi`. The Makefile
passes `\def\HandoutBuild{}` for the handout, so the two PDFs cannot drift apart.
CI greps each handout and fails the build if a solutions heading survived.

The lab notebooks follow the same discipline: `lab/build_notebooks.py` emits both
the student and the solutions notebook from one source. They are committed, so
Colab can open them, and CI regenerates them and fails if a committed file no
longer matches its generator. **Edit the generator, never the `.ipynb`.**

### The shared style

`common/pinns-course.sty` carries the palette, fonts, geometry, running headers,
theorem environments, boxes and the notation set. A document declares only its
metadata:

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[flat]{pinns-course}     % 'flat' = continuous theorem numbering
\coursemeta{PDF title}{header tail}{keywords}
\begin{document}
\coursetitle{Session 1}{The neural network\\ as an approximation class}{}
```

---

## For other lecturers

The material is reusable under CC BY-NC-SA. Two documents may be of more use than
the course itself:

- [`docs/authoring.md`](docs/authoring.md) — the working method. Section 3 lists
  the statement-hygiene rules, each corresponding to an error actually caught in
  review; section 4 is the argument that every asserted constant must be computed
  before it is written, with the three that were wrong.
- [`docs/running-a-problem-class.md`](docs/running-a-problem-class.md) — how the
  Session 1 problem class is actually run in ninety minutes, including what does
  not fit.

## Corrections

Please open an [issue](../../issues). The Session 1 notes went through five rounds
of review before first distribution and that review caught real errors — a wrong
coefficient in a distributional derivative, a Barron class defined so narrowly
that its own examples fell outside it, an unproved claim about equal-weight
averages. Further corrections are welcome, and credited.

## Licence

Course text under **CC BY-NC-SA 4.0**, code under the **MIT licence**; see
[`LICENSE`](LICENSE) and [`CITATION.cff`](CITATION.cff). Results quoted from the
literature remain the property of their authors and are cited in each session's
reference list.
