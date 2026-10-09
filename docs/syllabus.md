# Syllabus — ten sessions of 90 minutes

Prerequisites: a solid M1 in mathematics (functional analysis, distributions and
Sobolev spaces, linear PDEs, differentiable optimisation, elementary probability).
No prior exposure to machine learning.

Assessment: a mini-project distributed in Session 5, defended in Session 10.

---

## Block I — Foundations (1–3)

**1. The neural network as an approximation class.** The class and its structure;
it is neither a vector space nor a convex set, and this single fact is the source
of the course's difficulties. Universal approximation (Cybenko; LLPS). Quantitative
bounds: Maurey, Barron, comparison with linear Kolmogorov widths. Approximation in
Sobolev norms — the right question for PINNs, since one approximates `D[u]`, not
`u`. Depth against width.

**2. Automatic differentiation and nonconvex optimisation.** Forward and reverse
mode, with correctness and cost proved; the cheap-gradient principle. Why AD is not
a difference quotient, and the arithmetic of why that matters. The `O(d)` cost of a
Laplacian. What is provable about gradient descent, and what is not.

**3. The PINN method: formulation and mathematical status.** Residual formulation
and collocation. Boundary conditions: penalty against exact lifting. Read correctly:
nonlinear least squares on a parametrised manifold. Honest placement among the
classical methods of weighted residuals.

## Block II — Theory (4–6)

**4. Error decomposition; the approximation error.** Approximation, optimisation and
quadrature. Regularity of the solution and the rates it buys. High dimension:
Kolmogorov equations, Barron spaces for PDEs.

**5. From residual to error: PDE stability.** The heart of the course. Conditional
a posteriori estimates. Elliptic, parabolic, Navier–Stokes; the failure of the `L²`
framework for conservation laws. Generalisation and quadrature error. *Projects
distributed.*

**6. Training pathologies.** Spectral bias. The neural tangent kernel of a PINN.
Intrinsic ill-conditioning of the differential operator. Loss of causality in time.
Remedies, and which of them rest on a statement rather than on tuning.

## Block III — Extensions (7–10)

**7. Weak and variational formulations.** Deep Ritz, VPINN and hp-VPINN, weak
adversarial networks. What a weak formulation buys and what it costs.

**8. Inverse problems and data assimilation.** Where the method is genuinely
competitive. Comparison with the adjoint-state approach. Ill-posedness, conditional
stability, uncertainty.

**9. Operator learning.** DeepONet, neural operators, FNO. Physics-informed
operators. The curse of parametric complexity, and Kolmogorov widths again.

**10. Defences and critical assessment.** Project defences. PINNs against finite
elements, with published numbers. Where the method is legitimate. Open questions.

---

## A note on pacing

Session 1 as written contains more than ninety minutes of material: proving
Barron's theorem in full and the smooth case of LLPS at the board would take a
second slot. The notes say so explicitly. If an eleventh session can be found,
splitting Session 1 in two is the better option; otherwise Cybenko and Maurey are
proved in full and Barron is given as an idea.
