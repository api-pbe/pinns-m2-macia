import torch, numpy as np
torch.manual_seed(0); np.random.seed(0)
torch.set_default_dtype(torch.float64)

print("="*70); print("LAB 1  — ridge functions: gradient direction")
# f1 = tanh(w1.x), f2 = tanh(w2.x), f = (f1+f2)/2 ; measure spread of grad direction
w1 = torch.tensor([1.0, 0.0]); w2 = torch.tensor([0.0, 1.0])
X = torch.rand(4000, 2)*4 - 2; X.requires_grad_(True)
def spread(fun):
    y = fun(X); g, = torch.autograd.grad(y.sum(), X)
    g = g / g.norm(dim=1, keepdim=True)
    ang = torch.atan2(g[:,1], g[:,0])
    return (ang.max()-ang.min()).item()
print(f"  single ridge tanh(w1.x)  : angular spread of grad = {spread(lambda X: torch.tanh(X@w1)):.3e} rad")
print(f"  half-sum of two ridges   : angular spread of grad = {spread(lambda X: 0.5*(torch.tanh(X@w1)+torch.tanh(X@w2))):.4f} rad")

print("="*70); print("LAB 2  — quadratic activation: realised degree vs depth")
def deep_quad(x, L, width=6):
    h = x.reshape(-1,1)
    for _ in range(L-1):
        W = torch.randn(h.shape[1], width); b = torch.randn(width)
        h = (h@W + b)**2
    W = torch.randn(h.shape[1], 1); b = torch.randn(1)
    return (h@W + b).squeeze()
xs = torch.linspace(-1, 1, 400)
for L in [2,3,4]:
    torch.manual_seed(L)
    y = deep_quad(xs, L).numpy(); deg = 2**(L-1)
    for dtry in [deg-1, deg]:
        c = np.polyfit(xs.numpy(), y, dtry)
        r = np.abs(np.polyval(c, xs.numpy())-y).max()/np.abs(y).max()
        print(f"  depth L={L} (predicted degree {deg:2d}) : fit by degree {dtry:2d} -> rel. residual {r:.2e}")

print("="*70); print("LAB 3a — non-convexity of the loss along a segment")
# target tanh ; theta+ = (c,w,b)=(1,1,0) ; theta- = (-1,-1,0) ; both realise tanh
xg = torch.linspace(-1,1,2001); f = torch.tanh(xg)
def J(theta):
    c,w,b = theta
    return ((c*torch.tanh(w*xg+b) - f)**2).mean().item()
tp = torch.tensor([1.,1.,0.]); tm = torch.tensor([-1.,-1.,0.])
for t in [0.0,0.25,0.5,0.75,1.0]:
    th = (1-t)*tp + t*tm
    print(f"  t={t:.2f}  theta=({th[0]:+.2f},{th[1]:+.2f},{th[2]:+.2f})   J = {J(th):.6f}")

print("="*70); print("LAB 3b — random features (convex) vs full training (nonconvex)")
def target(x): return torch.sin(2*np.pi*x) + 0.25*torch.sin(16*np.pi*x)
xtr = torch.linspace(0,1,2000); ytr = target(xtr)
def rf_solve(n, seed):
    g = torch.Generator().manual_seed(seed)
    s = torch.randn(n, generator=g)*20.0; u = torch.rand(n, generator=g)
    A = torch.tanh(s*(xtr.reshape(-1,1)-u))
    A = torch.cat([A, torch.ones(len(xtr),1)], 1)
    c = torch.linalg.lstsq(A, ytr.reshape(-1,1)).solution
    return ((A@c).squeeze()-ytr).pow(2).mean().sqrt().item()
def train_full(n, seed, steps=4000):
    g = torch.Generator().manual_seed(seed)
    s = (torch.randn(n, generator=g)*20.0).requires_grad_(True)
    u = (torch.rand(n, generator=g)).requires_grad_(True)
    c = (torch.randn(n, generator=g)/np.sqrt(n)).requires_grad_(True)
    b0 = torch.zeros(1, requires_grad=True)
    opt = torch.optim.Adam([s,u,c,b0], lr=5e-3)
    for _ in range(steps):
        opt.zero_grad()
        loss = ((torch.tanh(s*(xtr.reshape(-1,1)-u))@c + b0) - ytr).pow(2).mean()
        loss.backward(); opt.step()
    return loss.sqrt().item()
print(f"  {'n':>5} | {'random feat. (lstsq)':>22} | {'full training (Adam)':>22}")
for n in [8, 16, 32, 64, 128, 256]:
    a = np.median([rf_solve(n, s) for s in range(5)])
    b = np.median([train_full(n, s) for s in range(3)])
    print(f"  {n:>5} | {a:>22.3e} | {b:>22.3e}")

print("="*70); print("LAB 4  — a finite-dimensional shadow of 'discriminatory'")
M = 40; xs4 = torch.linspace(-1,1,M)
for name, act in [("tanh", torch.tanh), ("t^2", lambda t: t**2)]:
    print(f"  activation {name}:")
    for n in [2, 5, 10, 20, 40, 100, 400]:
        g = torch.Generator().manual_seed(1)
        w = torch.randn(n, generator=g)*3; b = torch.randn(n, generator=g)*3
        A = act(xs4.reshape(-1,1)*w + b)
        r = torch.linalg.matrix_rank(A, rtol=1e-10).item()
        print(f"     n={n:>4} features -> rank of A ({M}x{n}) = {r}")
