"""Numerical checks for this session.

Everything asserted in the text — constants, worked examples, figures — is
computed here first. See docs/authoring.md, section 4.

    python3 experiments.py
"""
import torch, numpy as np
torch.set_default_dtype(torch.float64)
torch.manual_seed(0); np.random.seed(0)

print("=" * 70)
print("CHECK 1 — ")
