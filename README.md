# Physics-Informed Neural Networks for PDEs

Course materials for **M2 MACIA**, AGM — CY Cergy Paris University.
Paul Boureau.

Ten ninety-minute sessions on what can and cannot be proved about solving partial
differential equations with neural networks. The entry point assumes a solid M1 in
mathematics and **no prior exposure to machine learning**: the class of networks is
built from scratch in Session 1, as an object of approximation theory.

> **This repository is private.** It contains the solutions. Student material is
> published through public releases — see [Releases](#releases) below.

---

## Contents

| Session | Topic | Materials |
|---|---|---|
| 1 | The neural network as an approximation class | `notes.tex`, `problem-class.tex`, `lab.tex` + notebooks |
| 2 | Automatic differentiation and nonconvex optimisation | `notes.tex` |
| 3 | The PINN method: formulation and status | *to come* |
| 4 | Error decomposition; the approximation error | *to come* |
| 5 | From residual to error: PDE stability | *to come* |
| 6 | Training pathologies | *to come* |
| 7 | Weak and variational formulations | *to come* |
| 8 | Inverse problems and data assimilation | *to come* |
| 9 | Operator learning | *to come* |
| 10 | Defences and critical assessment | *to come* |

Each session directory holds its own `figures/` and, where there is a lab, a `lab/`
with the notebook generator and the scripts that produce the figures.

---

## Building

Requires a TeX Live installation and Python 3.

```sh
make            # every document, teacher version (solutions included)
make student    # every document, solutions stripped
make notebooks  # regenerate the lab notebooks from their generator
make release    # student PDFs + student notebooks, collected in dist/
make clean      # remove LaTeX auxiliaries
```

Nothing compiled is versioned: `.gitignore` excludes PDFs, and CI builds them.

### How the solutions switch works

One source per document. `common/pinns-course.sty` defines a boolean:

```latex
\newif\ifsolutions
\ifdefined\StudentBuild \solutionsfalse \else \solutionstrue \fi
```

and every solutions section is wrapped in `\ifsolutions ... \fi`. The Makefile
passes `\def\StudentBuild{}` on the command line for the student variant, so the
two PDFs can never drift apart. CI additionally greps each student PDF and
**fails the build** if a solutions heading survived.

### The shared style

`common/pinns-course.sty` carries the palette, fonts, page geometry, running
headers, theorem environments, boxes and the whole notation set. Documents declare
only their metadata:

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[flat]{pinns-course}     % 'flat' = continuous theorem numbering
\coursemeta{PDF title}{header tail}{keywords}
\begin{document}
\coursetitle{Session 1}{The neural network\\ as an approximation class}{}
```

Option `flat` numbers the theorem family continuously (problem classes, labs);
without it, numbering is by section (lecture notes).

---

## Labs

Labs are generated, not hand-maintained: `lab/build_notebooks.py` emits **both**
the student notebook and the solutions notebook from a single source, exactly as
the LaTeX flag emits both PDFs. Edit the generator, never the `.ipynb`.

```sh
pip install -r requirements.txt
cd session-01-approximation-class/lab && python3 build_notebooks.py
```

CPU only — no GPU is used anywhere in this course. The Session 1 lab runs end to
end in about three minutes on a laptop.

A word of warning that belongs in the lab itself and is repeated here: the
notebooks set `torch.set_default_dtype(torch.float64)`. Two of the tasks measure
errors below `1e-8`, which single precision cannot represent.

---

## Releases

Tagging a commit `v*` triggers a public release containing **only** the student
material: documents without solutions, and notebooks with the gaps to fill.

```sh
git tag -a v1.0-session1 -m "Session 1: notes, problem class, lab"
git push origin v1.0-session1
```

Send students the release URL. Solutions stay in this repository.

---

## Starting the repository

The history is already here, with two commits. To put it on GitHub as a **private**
repository:

```sh
gh repo create pinns-m2-macia --private --source=. --remote=origin --push
```

or, without the GitHub CLI: create an empty private repository on github.com, then

```sh
git remote add origin git@github.com:<you>/pinns-m2-macia.git
git push -u origin main
```

Check that Actions are enabled (Settings → Actions) and that the workflow has write
permission for releases (Settings → Actions → General → Workflow permissions →
*Read and write*). The release job needs it to publish.

One caveat worth knowing before you tag: a release attached to a **private**
repository is visible only to people with access to it. To hand students a public
link you need either a second public repository that the workflow pushes `dist/`
into, or GitHub Pages, or simply the release assets uploaded to your institutional
space. Decide this once, before the first tag.

---

## Licence

Course text under **CC BY-NC-SA 4.0**, code under the **MIT licence**. See
[`LICENSE`](LICENSE). Results quoted from the literature remain the property of
their authors and are cited in each session's reference list.

---

## A note on corrections

The Session 1 notes went through five rounds of mathematical review before being
fit to distribute, and the review caught real errors — a wrong coefficient in a
distributional derivative, a Barron class defined so narrowly that its own examples
fell outside it, an unproved claim about equal-weight averages. Corrections from
anyone reading this, students included, are welcome as issues.
