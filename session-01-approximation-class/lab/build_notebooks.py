import json, copy

def md(s):   return {"cell_type":"markdown","metadata":{},"source":s.strip("\n").split("\n")}
def code(s): return {"cell_type":"code","metadata":{},"execution_count":None,"outputs":[],
                     "source":s.strip("\n").split("\n")}

HDR = """
# Computational lab 1 — Universal approximation, in numbers

**M2 MACIA · Physics-Informed Neural Networks for PDEs**  
Paul Boureau — AGM, CY Cergy Paris University

This notebook is the companion to the problem class *Session 1 · Universal approximation*.
Each part reproduces, numerically, a statement you proved on paper. Nothing here replaces a proof:
the point is to see the objects, and to meet — once, concretely — the gap between *a good network
exists* and *an algorithm finds it*.

Cells marked **`# TODO`** are yours. Everything else is given.
"""

SETUP = """
import torch, numpy as np, matplotlib.pyplot as plt
torch.set_default_dtype(torch.float64)      # double precision: we will measure small errors
torch.manual_seed(0); np.random.seed(0)

TEAL, WINE, OCHRE = "#0E6A62", "#8A3A55", "#7E5C0E"
print("torch", torch.__version__)
"""

P1_MD = """
---
## Part 1 — Slabs, not bumps

*Companion to Exercise 1 of the problem class, and to Proposition 1.5 of the lecture notes.*

A one-hidden-layer network is
$$\\Phi_\\theta(x) \;=\; \\sum_{i=1}^n c_i\\,\\sigma(w_i\\cdot x + b_i),
\\qquad \\theta = (c, W, b).$$
We write it by hand, with tensors, so that nothing is hidden. `W` has shape `(n, d)`.
"""

P1_CODE = """
def phi(x, c, W, b, act=torch.tanh):
    \"\"\"x: (M, d) -> (M,).  One hidden layer, n neurons, written out explicitly.\"\"\"
    return act(x @ W.T + b) @ c

d, n = 2, 3
x = torch.randn(5, d); c = torch.randn(n); W = torch.randn(n, d); b = torch.randn(n)
print(phi(x, c, W, b).shape)
"""

P1A_MD = """
### 1.1 — The bump in dimension 1 (Exercise 1, item 3)

You showed that for sigmoidal $\\sigma$ and $a<b$,
$\\sigma(\\lambda(x-a)) - \\sigma(\\lambda(x-b)) \\to \\mathbf{1}_{(a,b)}$ pointwise off $\\{a,b\\}$.
Watch it happen.
"""

P1A_CODE = """
xs = torch.linspace(-1, 2, 1000)
sig = lambda t: torch.sigmoid(t)                 # a sigmoidal activation: limits 0 and 1
a, bb = 0.3, 0.8

plt.figure(figsize=(6, 2.6))
for lam, col in zip([2, 10, 100], [OCHRE, WINE, TEAL]):
    plt.plot(xs, sig(lam*(xs-a)) - sig(lam*(xs-bb)), color=col, lw=1.4, label=f"$\\\\lambda={lam}$")
plt.legend(frameon=False); plt.xlabel("$x$"); plt.title("two sigmoids make a bump")
plt.tight_layout(); plt.show()
"""

P1B_MD = """
### 1.2 — In dimension 2 it is a slab, not a bump (Exercise 1, item 5) — **TODO**

Plot the level sets of $\\sigma(w_1\\cdot x)$, of $\\sigma(w_2\\cdot x)$ with $w_1=(1,0)$, $w_2=(0,1)$,
and of their half-sum, on $[-2,2]^2$.

Look at the level sets, and answer in one sentence: *why can no finite linear combination of ridge
functions be the indicator of a square?*
"""

P1B_CODE_TODO = """
g = torch.linspace(-2, 2, 300)
X, Y = torch.meshgrid(g, g, indexing="ij")
P = torch.stack([X.reshape(-1), Y.reshape(-1)], 1)      # (M, 2) grid points

# TODO: evaluate the three functions on P with phi(...), reshape to X.shape,
#       and draw them side by side with plt.contour / plt.contourf.
"""

P1B_CODE_SOL = """
g = torch.linspace(-2, 2, 300)
X, Y = torch.meshgrid(g, g, indexing="ij")
P = torch.stack([X.reshape(-1), Y.reshape(-1)], 1)

w1 = torch.tensor([[1.0, 0.0]]); w2 = torch.tensor([[0.0, 1.0]])
one, zero = torch.ones(1), torch.zeros(1)
f1 = phi(P, one, w1, zero).reshape(X.shape)
f2 = phi(P, one, w2, zero).reshape(X.shape)
fs = 0.5*(f1 + f2)

fig, ax = plt.subplots(1, 3, figsize=(9, 2.8))
for a_, (Z, t) in zip(ax, [(f1, r"$\\sigma(w_1\\cdot x)$"), (f2, r"$\\sigma(w_2\\cdot x)$"),
                           (fs, r"$\\frac{1}{2}(f_1+f_2)$")]):
    a_.contourf(X, Y, Z, levels=18, cmap="BrBG", alpha=.55)
    a_.contour(X, Y, Z, levels=12, colors=[TEAL], linewidths=.7)
    a_.set_title(t); a_.set_aspect("equal")
plt.tight_layout(); plt.show()
"""

P1B_ANS = """
**Answer.** Each ridge function is constant along every hyperplane $w\\cdot x=\\text{const}$: it is a
*slab*, infinite in the $d-1$ directions orthogonal to $w$. A finite sum of slabs cannot vanish
outside a bounded set, because far away in a direction orthogonal to every $w_i$ all the terms are
frozen at a constant value. Localisation in $d\\ge 2$ requires either intersecting slabs, which is
not a linear operation, or the genuinely different arguments of Parts C–F of the problem class.
"""

P1C_MD = """
### 1.3 — Proposition 1.5, measured (Exercise 1 again, and §1 of the notes) — **TODO**

You proved that if $f\\in\\Sigma_1(\\sigma)$ then $\\nabla f(x)$ is collinear to a *fixed* vector $w$
for every $x$, and that this fails for $\\frac12(f_1+f_2)$. Measure it: sample points at random,
compute $\\nabla f$ with `torch.autograd.grad`, normalise, and report the angular spread of the
directions.

*(You are using automatic differentiation two weeks early. Session 2 explains what it does; for now,
`autograd.grad` returns the exact gradient, not a finite difference.)*
"""

P1C_CODE_TODO = """
def angular_spread(fun, n_pts=4000):
    X = (torch.rand(n_pts, 2)*4 - 2).requires_grad_(True)
    # TODO: y = fun(X); get g = dy/dX with torch.autograd.grad(y.sum(), X)
    #       normalise each row, take the angle atan2(g1, g0), return max - min
    raise NotImplementedError

print("single ridge :", angular_spread(lambda X: torch.tanh(X @ torch.tensor([1.0, 0.0]))))
print("half-sum     :", angular_spread(lambda X: 0.5*(torch.tanh(X @ torch.tensor([1.0, 0.0]))
                                                    + torch.tanh(X @ torch.tensor([0.0, 1.0])))))
"""

P1C_CODE_SOL = """
def angular_spread(fun, n_pts=4000):
    X = (torch.rand(n_pts, 2)*4 - 2).requires_grad_(True)
    y = fun(X)
    g, = torch.autograd.grad(y.sum(), X)
    g = g / g.norm(dim=1, keepdim=True)
    ang = torch.atan2(g[:, 1], g[:, 0])
    return (ang.max() - ang.min()).item()

w1 = torch.tensor([1.0, 0.0]); w2 = torch.tensor([0.0, 1.0])
one_ridge = angular_spread(lambda X: torch.tanh(X @ w1))
half_sum  = angular_spread(lambda X: 0.5*(torch.tanh(X @ w1) + torch.tanh(X @ w2)))
print(f"single ridge : {one_ridge:.3e} rad")
print(f"half-sum     : {half_sum:.4f} rad")
"""

P1C_ANS = """
Expected output: `0.000e+00` and about `1.43` rad (the last digits depend on the sample). The first is exactly zero — not small, *zero* — because
$\\nabla f = c\\,\\sigma'(w\\cdot x+b)\\,w$ is a positive multiple of a fixed vector, and normalising
removes the only thing that varies. The second is a genuine angular sector: the gradient direction
rotates, which is precisely the contradiction in the proof of Proposition 1.5.
"""

P2_MD = """
---
## Part 2 — A polynomial activation is not rescued by width, and *is* helped by depth

*Companion to Exercise 2, items 5 and 6.*

You proved: with $\\sigma(t)=t^2$ and depth $L$, the realised function is a polynomial of degree at
most $2^{L-1}$ — whatever the width. And that letting $L$ grow recovers all polynomials.

Here is the cheapest possible test, and it needs no training at all: take a **random** deep
quadratic network, sample it, and fit a polynomial. If the prediction is right, degree $2^{L-1}$
should fit to machine precision and degree $2^{L-1}-1$ should not.
"""

P2_CODE_TODO = """
def deep_quadratic(x, L, width=6, seed=0):
    \"\"\"Random network, activation t^2, depth L (so L-1 hidden layers). x: (M,) -> (M,).\"\"\"
    torch.manual_seed(seed)
    h = x.reshape(-1, 1)
    for _ in range(L - 1):
        W = torch.randn(h.shape[1], width); b = torch.randn(width)
        h = (h @ W + b)**2
    W = torch.randn(h.shape[1], 1); b = torch.randn(1)
    return (h @ W + b).squeeze()

xs = torch.linspace(-1, 1, 400)
# TODO: for L = 2, 3, 4, evaluate the network, then np.polyfit at degrees 2**(L-1)-1 and 2**(L-1),
#       and print the relative sup residual of each fit. What do you predict before running it?
"""

P2_CODE_SOL = """
def deep_quadratic(x, L, width=6, seed=0):
    torch.manual_seed(seed)
    h = x.reshape(-1, 1)
    for _ in range(L - 1):
        W = torch.randn(h.shape[1], width); b = torch.randn(width)
        h = (h @ W + b)**2
    W = torch.randn(h.shape[1], 1); b = torch.randn(1)
    return (h @ W + b).squeeze()

xs = torch.linspace(-1, 1, 400); xn = xs.numpy()
for L in [2, 3, 4]:
    y = deep_quadratic(xs, L, seed=L).numpy(); deg = 2**(L-1)
    for dtry in [deg-1, deg]:
        res = np.abs(np.polyval(np.polyfit(xn, y, dtry), xn) - y).max() / np.abs(y).max()
        flag = "  <-- machine precision" if res < 1e-12 else ""
        print(f"L={L}  predicted degree {deg:2d} | polynomial fit of degree {dtry:2d}"
              f" -> rel. residual {res:.2e}{flag}")
"""

P2_ANS = """
Expected output: residuals of order $10^{-15}$ at degree exactly $2^{L-1}$, and $10^{-1}$ to
$10^{-3}$ one degree below. The bound of Exercise 2 is therefore not merely an upper bound — it is
attained, generically.

Two things worth noticing. The experiment involves **no optimisation**: it tests a statement about
the *class*, and a statement about a class should be testable without an algorithm. And the drop as
the degree goes from $2^{L-1}-1$ to $2^{L-1}$ shrinks as $L$ grows ($10^{-1}$, $10^{-2}$,
$10^{-3}$): a degree-$7$ polynomial already approximates a generic degree-$8$ one rather well on
$[-1,1]$. *Exact* representation and *good* approximation are different questions — the distinction
that separates Cybenko from Barron.
"""

P3_MD = """
---
## Part 3 — Existence is not an algorithm

*Companion to Exercise 5, items 2 and 3, and to Exercise 2.4 of the lecture notes.*

This is the part that matters for the rest of the course.
"""

P3A_MD = """
### 3.1 — The loss is not convex: the two-line counterexample, drawn — **TODO**

In Exercise 2.4 of the lecture notes you checked that $\\theta_+=(c,w,b)=(1,1,0)$ and
$\\theta_-=(-1,-1,0)$ both realise $\\tanh$, so $J(\\theta_+)=J(\\theta_-)=0$ for the target
$f=\\tanh$, while the midpoint realises the zero function.

Plot $t \\mapsto J\\big((1-t)\\theta_+ + t\\theta_-\\big)$ on $[0,1]$.
"""

P3A_CODE_TODO = """
xg = torch.linspace(-1, 1, 2001); f = torch.tanh(xg)

def J(theta):
    c, w, b = theta
    return ((c*torch.tanh(w*xg + b) - f)**2).mean().item()

tp = torch.tensor([1., 1., 0.]); tm = torch.tensor([-1., -1., 0.])
# TODO: evaluate J along the segment and plot it. What is the value at t = 1/2, and why?
"""

P3A_CODE_SOL = """
xg = torch.linspace(-1, 1, 2001); f = torch.tanh(xg)

def J(theta):
    c, w, b = theta
    return ((c*torch.tanh(w*xg + b) - f)**2).mean().item()

tp = torch.tensor([1., 1., 0.]); tm = torch.tensor([-1., -1., 0.])
ts = np.linspace(0, 1, 201)
Js = [J((1-t)*tp + t*tm) for t in ts]

plt.figure(figsize=(5.4, 2.5))
plt.plot(ts, Js, color=WINE, lw=1.6)
plt.plot([0, 1], [0, 0], "o", color=TEAL, ms=5)
plt.xlabel(r"$t$ along the segment"); plt.ylabel("$J$")
plt.tight_layout(); plt.show()
print(f"J at the midpoint = {J(0.5*(tp+tm)):.6f}   and   mean(tanh^2) = {(f**2).mean():.6f}")
"""

P3A_ANS = """
Expected: a curve equal to $0$ at both endpoints and rising to $0.2386$ in the middle — which is
exactly $\\frac12\\int_{-1}^{1}\\tanh^2$, because the midpoint parameter is $(0,0,0)$ and realises the
zero function. A convex function cannot exceed the larger of its endpoint values; this one does, by
a wide margin.

The mechanism is worth naming: the *function* class is traversed twice by the *parameter* space
(here $\\theta_+$ and $\\theta_-$ are different parameters realising the same function), and the
straight line between two such parameters leaves the region of good functions entirely. No amount of
cleverness in the optimiser removes this; it is a property of the parametrisation.
"""

P3B_MD = """
### 3.2 — $\\mathcal{E}_{\\mathrm{app}}$ against $\\mathcal{E}_{\\mathrm{opt}}$ — **TODO**

Cybenko's theorem says a good $\\theta$ exists. Here we separate *existence* from *finding*, with a
trick: if the inner parameters $(w_i,b_i)$ are **frozen at random values**, then $J$ depends on the
outer coefficients $c$ only, and $\\min_c J$ is a **linear least-squares problem** — convex, solved
exactly by `torch.linalg.lstsq`. That gives an achievable error with no optimisation difficulty at
all.

Then train *all* the parameters by gradient descent, with the same $n$, and compare.

Target: $f(x) = \\sin(2\\pi x) + \\tfrac14\\sin(16\\pi x)$ on $[0,1]$ — one slow mode and one fast one.
"""

P3B_CODE_TODO = """
def target(x): return torch.sin(2*np.pi*x) + 0.25*torch.sin(16*np.pi*x)
xtr = torch.linspace(0, 1, 2000); ytr = target(xtr)

def features(s, u):                      # tanh(s_i (x - u_i)) : slope s_i, transition at u_i
    return torch.tanh(s*(xtr.reshape(-1, 1) - u))

def random_features(n, seed):
    \"\"\"Freeze (s, u) at random, solve for c by least squares. Return the RMS error.\"\"\"
    g = torch.Generator().manual_seed(seed)
    s = torch.randn(n, generator=g)*20.0; u = torch.rand(n, generator=g)
    # TODO: build A = [features(s,u), 1], solve with torch.linalg.lstsq, return the RMS error
    raise NotImplementedError

def train_everything(n, seed, steps=4000, lr=5e-3):
    \"\"\"Same architecture, but optimise s, u, c, b0 jointly with Adam.\"\"\"
    g = torch.Generator().manual_seed(seed)
    s  = (torch.randn(n, generator=g)*20.0).requires_grad_(True)
    u  = (torch.rand(n, generator=g)).requires_grad_(True)
    c  = (torch.randn(n, generator=g)/np.sqrt(n)).requires_grad_(True)
    b0 = torch.zeros(1, requires_grad=True)
    opt = torch.optim.Adam([s, u, c, b0], lr=lr)
    # TODO: the training loop. At each step: zero the gradients, compute the mean squared error
    #       between tanh(s*(x-u)) @ c + b0 and ytr, call .backward(), call opt.step().
    raise NotImplementedError

# TODO: loop over n = 8, 16, 32, 64, 128, 256 and tabulate the two errors. Predict first.
"""

P3B_CODE_SOL = """
def target(x): return torch.sin(2*np.pi*x) + 0.25*torch.sin(16*np.pi*x)
xtr = torch.linspace(0, 1, 2000); ytr = target(xtr)

def random_features(n, seed):
    g = torch.Generator().manual_seed(seed)
    s = torch.randn(n, generator=g)*20.0; u = torch.rand(n, generator=g)
    A = torch.cat([torch.tanh(s*(xtr.reshape(-1,1) - u)), torch.ones(len(xtr), 1)], 1)
    c = torch.linalg.lstsq(A, ytr.reshape(-1, 1)).solution
    return ((A @ c).squeeze() - ytr).pow(2).mean().sqrt().item()

def train_everything(n, seed, steps=4000, lr=5e-3):
    g = torch.Generator().manual_seed(seed)
    s  = (torch.randn(n, generator=g)*20.0).requires_grad_(True)
    u  = (torch.rand(n, generator=g)).requires_grad_(True)
    c  = (torch.randn(n, generator=g)/np.sqrt(n)).requires_grad_(True)
    b0 = torch.zeros(1, requires_grad=True)
    opt = torch.optim.Adam([s, u, c, b0], lr=lr)
    for _ in range(steps):
        opt.zero_grad()
        loss = ((torch.tanh(s*(xtr.reshape(-1,1) - u)) @ c + b0) - ytr).pow(2).mean()
        loss.backward(); opt.step()
    return loss.sqrt().item()

ns, rf, tr = [8, 16, 32, 64, 128, 256], [], []
print(f"{'n':>5} | {'frozen features (exact)':>24} | {'all trained (Adam)':>20}")
for n in ns:
    a = float(np.median([random_features(n, s) for s in range(5)]))
    b = float(np.median([train_everything(n, s) for s in range(3)]))
    rf.append(a); tr.append(b)
    print(f"{n:>5} | {a:>24.3e} | {b:>20.3e}")

plt.figure(figsize=(5.4, 3.0))
plt.loglog(ns, rf, "o-", color=TEAL,  lw=1.4, ms=4, label="frozen features, least squares (convex)")
plt.loglog(ns, tr, "s-", color=WINE,  lw=1.4, ms=4, label="all parameters, Adam (nonconvex)")
plt.xlabel("number of neurons $n$"); plt.ylabel("RMS error"); plt.legend(frameon=False, fontsize=7)
plt.grid(True, which="both", ls=":", lw=.5); plt.tight_layout(); plt.show()
"""

P3B_ANS = """
Expected output (medians over several seeds; your digits will differ slightly):

| $n$ | frozen features, exact solve | all parameters, Adam |
|---|---|---|
| 8 | 1.7e-01 | 1.5e-01 |
| 16 | 1.3e-01 | 5.0e-02 |
| 32 | 1.3e-02 | 1.2e-02 |
| 64 | 5.7e-06 | 2.5e-02 |
| 128 | 6.3e-09 | 8.8e-03 |
| 256 | 1.4e-10 | 9.9e-03 |

Read it carefully, in three steps.

1. **Up to $n\\approx 32$, training wins.** That is not a paradox: training may move the $(s_i,u_i)$,
   so it searches a strictly larger set than the frozen dictionary. When neurons are scarce,
   placing them well is worth more than solving exactly.

2. **From $n=64$ on, the convex solve runs away** — down to $10^{-10}$, while training *stops
   improving* and sits near $10^{-2}$. At $n=256$ the gap is eight orders of magnitude. Both numbers
   concern the *same* class $\\Sigma_n(\\tanh)$: a network achieving $10^{-10}$ demonstrably exists,
   since we exhibited one, and Adam does not find anything close.

3. **This is $\\mathcal{E}_{\\mathrm{app}}$ against $\\mathcal{E}_{\\mathrm{opt}}$**, and it is the
   subject of Session 6. Cybenko and Barron bound the first term. The experiment above says the
   second can dominate it completely.

**An honest caveat, which is part of the lesson.** This is *one* optimiser, *one* learning rate,
*one* budget of 4000 steps. A longer run, a schedule, or L-BFGS would improve the red curve — try
it, that is the most instructive variation to make. What no tuning removes is the shape of the
finding: the convex problem is solved to machine precision without effort, and the nonconvex one
over the same class requires care, luck and a stopping criterion. Nothing in Session 1 warned you
about this, because nothing in Session 1 is about it.
"""

P4_MD = """
---
## Part 4 (take home) — A finite-dimensional shadow of "discriminatory"

*Companion to Exercise 4 and Definition 1 of the problem class.*

The discriminatory property says: the only finite signed measure $\\mu$ with
$\\int \\sigma(wx+b)\\,d\\mu = 0$ for **all** $(w,b)$ is $\\mu = 0$. Replace $K$ by $M$ sample points
and the measure by a weight vector $\\mu\\in\\mathbb{R}^M$. The condition becomes
$A^{\\!\\top}\\mu = 0$, where $A_{ij} = \\sigma(w_j x_i + b_j)$.

So *"$\\sigma$ is discriminatory"* becomes, in finite dimension: **$A$ has full row rank $M$ once
enough features are drawn**. And a non-discriminatory $\\sigma$ should show a rank that saturates
below $M$ — the surviving $\\mu$'s spanning the annihilator of the whole class.

Compute the numerical rank of $A$ as $n$ grows, for $\\sigma=\\tanh$ and for $\\sigma(t)=t^2$.
"""

P4_CODE_TODO = """
M = 40; xs4 = torch.linspace(-1, 1, M)
# TODO: for each activation and each n in [2,5,10,20,40,100,400], build A (M x n) from random
#       (w, b) and print torch.linalg.matrix_rank(A, rtol=1e-10).
#       Predict the saturation value for t^2 before running.
"""

P4_CODE_SOL = """
M = 40; xs4 = torch.linspace(-1, 1, M)
for name, act in [("tanh", torch.tanh), ("t^2", lambda t: t**2)]:
    ranks = []
    for n in [2, 5, 10, 20, 40, 100, 400]:
        g = torch.Generator().manual_seed(1)
        w = torch.randn(n, generator=g)*3; b = torch.randn(n, generator=g)*3
        A = act(xs4.reshape(-1, 1)*w + b)
        ranks.append(torch.linalg.matrix_rank(A, rtol=1e-10).item())
    print(f"{name:>5}:  n = 2,5,10,20,40,100,400  ->  rank = {ranks}")
"""

P4_ANS = """
Expected: `tanh: [2, 5, 10, 20, 25, 37, 40]` and `t^2: [2, 3, 3, 3, 3, 3, 3]`.

The quadratic activation saturates at **3**, for ever, and $3 = \\dim\\mathcal{P}_2(\\mathbb{R})$. The
$37$-dimensional orthogonal complement is exactly the space of weight vectors annihilating every
element of $\\Sigma(t^2)$: a whole family of nonzero "measures" killing the entire class. That is
what *not* discriminatory looks like, and it is Exercise 2 seen through linear algebra.

Two further observations worth making, both honest.

*The tanh row is not clean.* Rank $25$ at $n=40$ and $37$ at $n=100$: full rank is reached slowly,
and only because the tolerance is finite. Mathematically $A$ has full rank for generic $(w,b)$ as
soon as $n\\ge M$; numerically the columns become nearly dependent and the matrix is atrociously
conditioned. You have just met, as a side effect, the conditioning problem that Session 2 will
quantify and Session 6 will blame for most PINN failures.

*This is a shadow, not a proof.* Full row rank on a finite point set does not imply that $\\sigma$ is
discriminatory on $K$ — the real statement quantifies over all measures on a continuum, and no
finite computation reaches it. The experiment illustrates the dichotomy; Part D of the problem class
proves it.
"""

CLOSING = """
---
## What to take away

1. Ridge functions are **slabs**. In $d\\ge2$ nothing is localised, and the one-dimensional intuition
   of a staircase of bumps does not transpose. This is why the proof needs Hahn–Banach and Fourier.
2. A **polynomial activation** is capped by width and freed by depth, exactly as predicted, and the
   cap is visible to machine precision without training anything.
3. The loss is **not convex**, and the counterexample is not pathological: it comes from the
   parametrisation being many-to-one on functions.
4. **Existence is not an algorithm.** On the same class, a convex solve reaches $10^{-10}$ where
   gradient training stalls at $10^{-2}$. Sessions 4 and 6 are about that gap.

*Next session: how `autograd.grad` actually computed those derivatives, why it is exact where a
finite difference is not, and what can and cannot be proved about the optimiser you just used.*
"""

def build(solutions: bool):
    cells = [md(HDR), code(SETUP),
             md(P1_MD), code(P1_CODE), md(P1A_MD), code(P1A_CODE),
             md(P1B_MD), code(P1B_CODE_SOL if solutions else P1B_CODE_TODO)]
    if solutions: cells.append(md(P1B_ANS))
    cells += [md(P1C_MD), code(P1C_CODE_SOL if solutions else P1C_CODE_TODO)]
    if solutions: cells.append(md(P1C_ANS))
    cells += [md(P2_MD), code(P2_CODE_SOL if solutions else P2_CODE_TODO)]
    if solutions: cells.append(md(P2_ANS))
    cells += [md(P3_MD), md(P3A_MD), code(P3A_CODE_SOL if solutions else P3A_CODE_TODO)]
    if solutions: cells.append(md(P3A_ANS))
    cells += [md(P3B_MD), code(P3B_CODE_SOL if solutions else P3B_CODE_TODO)]
    if solutions: cells.append(md(P3B_ANS))
    cells += [md(P4_MD), code(P4_CODE_SOL if solutions else P4_CODE_TODO)]
    if solutions: cells.append(md(P4_ANS))
    cells.append(md(CLOSING))
    return {"cells": cells, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"}},
        "nbformat": 4, "nbformat_minor": 5}

for sol, fn in [(False, "lab1-student.ipynb"), (True, "lab1-solutions.ipynb")]:
    json.dump(build(sol), open(fn, "w"), indent=1, ensure_ascii=False)
    print("wrote", fn)
