import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
TEAL="#0E6A62"; WINE="#8A3A55"; OCHRE="#7E5C0E"; GREY="#5C6663"
plt.rcParams.update({"font.size":8,"axes.edgecolor":GREY,"axes.labelcolor":GREY,
    "xtick.color":GREY,"ytick.color":GREY,"axes.titlesize":8,"font.family":"serif"})

# ---- Fig 1 : ridge functions in 2D -------------------------------------
g=np.linspace(-2,2,400); X,Y=np.meshgrid(g,g)
f1=np.tanh(X); f2=np.tanh(Y); fs=0.5*(f1+f2)
fig,ax=plt.subplots(1,3,figsize=(7.4,2.5))
for a,(Z,t) in zip(ax,[(f1,r"$\sigma(w_1\cdot x)$"),(f2,r"$\sigma(w_2\cdot x)$"),
                        (fs,r"$\frac{1}{2}(f_1+f_2)$")]):
    a.contourf(X,Y,Z,levels=18,cmap="BrBG",alpha=.55)
    a.contour(X,Y,Z,levels=12,colors=[TEAL],linewidths=.7)
    a.set_title(t); a.set_aspect("equal"); a.set_xticks([-2,0,2]); a.set_yticks([-2,0,2])
ax[0].set_ylabel(r"$x_2$")
for a in ax: a.set_xlabel(r"$x_1$")
plt.tight_layout(); plt.savefig("../figures/fig_ridge2d.png",dpi=200)
print("fig_ridge2d.png")

# ---- Fig 2 : convex solve vs full training -----------------------------
n=[8,16,32,64,128,256]
rf=[1.718e-01,1.279e-01,1.317e-02,5.716e-06,6.323e-09,1.447e-10]
tr=[1.476e-01,5.044e-02,1.172e-02,2.460e-02,8.845e-03,9.920e-03]
fig,a=plt.subplots(figsize=(5.0,3.0))
a.loglog(n,rf,"o-",color=TEAL,lw=1.4,ms=4,label="random features, solved by least squares\n(convex, exact)")
a.loglog(n,tr,"s-",color=WINE,lw=1.4,ms=4,label="all parameters trained by Adam\n(nonconvex, 4000 steps)")
a.set_xlabel("number of neurons $n$"); a.set_ylabel(r"RMS error on $[0,1]$")
a.grid(True,which="both",ls=":",lw=.5,color="#CBD3CD")
a.legend(frameon=False,fontsize=6.5,loc="lower left")
a.annotate("8 orders of\nmagnitude",xy=(256,1.4e-10),xytext=(70,2e-9),fontsize=6.5,color=OCHRE,
           arrowprops=dict(arrowstyle="-",color=OCHRE,lw=.8))
plt.tight_layout(); plt.savefig("../figures/fig_app_vs_opt.png",dpi=200)
print("fig_app_vs_opt.png")

# ---- Fig 3 : rank saturation -------------------------------------------
nn=[2,5,10,20,40,100,400]
rt=[2,5,10,20,25,37,40]; rq=[2,3,3,3,3,3,3]
fig,a=plt.subplots(figsize=(5.0,2.7))
a.semilogx(nn,rt,"o-",color=TEAL,lw=1.4,ms=4,label=r"$\sigma=\tanh$")
a.semilogx(nn,rq,"s-",color=WINE,lw=1.4,ms=4,label=r"$\sigma(t)=t^2$")
a.axhline(40,ls="--",lw=.8,color=GREY); a.text(2.2,41,"full rank $M=40$",fontsize=6.5,color=GREY)
a.axhline(3,ls=":",lw=.8,color=WINE);  a.text(2.2,4.5,r"$\dim\mathcal{P}_2(\mathbb{R})=3$",fontsize=6.5,color=WINE)
a.set_xlabel("number of random features $n$"); a.set_ylabel("numerical rank of $A$")
a.set_ylim(0,47); a.legend(frameon=False,fontsize=7,loc="center right")
a.grid(True,which="both",ls=":",lw=.5,color="#CBD3CD")
plt.tight_layout(); plt.savefig("../figures/fig_rank.png",dpi=200)
print("fig_rank.png")

# ---- Fig 4 : nonconvexity along the segment ----------------------------
import math
xg=np.linspace(-1,1,2001); f=np.tanh(xg)
ts=np.linspace(0,1,201); tp=np.array([1.,1.,0.]); tm=np.array([-1.,-1.,0.])
J=[np.mean((th[0]*np.tanh(th[1]*xg+th[2])-f)**2) for th in [(1-t)*tp+t*tm for t in ts]]
fig,a=plt.subplots(figsize=(5.0,2.5))
a.plot(ts,J,color=WINE,lw=1.6)
a.plot([0,1],[0,0],"o",color=TEAL,ms=5)
a.annotate(r"$\theta_+$",xy=(0,0),xytext=(0.03,0.02),fontsize=8,color=TEAL)
a.annotate(r"$\theta_-$",xy=(1,0),xytext=(0.93,0.02),fontsize=8,color=TEAL)
a.set_xlabel(r"$t$   along the segment $(1-t)\,\theta_+ + t\,\theta_-$")
a.set_ylabel(r"$J$")
a.grid(True,ls=":",lw=.5,color="#CBD3CD")
plt.tight_layout(); plt.savefig("../figures/fig_nonconvex.png",dpi=200)
print("fig_nonconvex.png  (max J =", round(max(J),6), ")")
