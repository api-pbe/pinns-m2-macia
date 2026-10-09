# Physics-Informed Neural Networks for PDEs — course materials

**M2 MACIA** · AGM, CY Cergy Paris University · Paul Boureau

Ten ninety-minute sessions on what can and cannot be proved about solving partial
differential equations with neural networks. Assumes a solid M1 in mathematics and
**no prior exposure to machine learning**.

Everything below is in [`materials/`](materials/), republished whenever a new
session is released.

## Documents

| | |
|---|---|
| Lecture notes | `materials/session-NN-notes.pdf` |
| Problem classes | `materials/session-NN-problem-class.pdf` |
| Computational labs | `materials/session-NN-lab.pdf` |

Solutions are distributed in class, not here.

## Labs

Open a lab notebook directly in Google Colab — nothing to install:

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/<PUBLIC_REPO>/blob/main/materials/lab1-student.ipynb)

To run them locally instead:

```sh
git clone https://github.com/<PUBLIC_REPO>.git
cd pinns-m2-macia-students
pip install torch numpy matplotlib jupyter
jupyter lab materials/
```

CPU only; no GPU is needed anywhere in this course. The labs set
`torch.set_default_dtype(torch.float64)` at the top, and this matters: several
tasks measure errors below `1e-8`, which single precision cannot represent.

## Found a mistake?

Please open an [issue](../../issues). The Session 1 notes went through five rounds
of review before being distributed and the review caught real errors; further
corrections are welcome, and credited.

## Licence

Course text under CC BY-NC-SA 4.0, code under the MIT licence.
