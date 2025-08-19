# test_hist.py — histogram sanity plots for PCG outputs (headless-friendly)
import os
import matplotlib
matplotlib.use("Agg")  # headless backend
import matplotlib.pyplot as plt
from collections import Counter

# Make sure 'bindings' is importable when running from project root
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bindings.pcg import (
    set_seed,
    get_float_between,
    get_int_between,
    get_uint_between,
    get_normalized,
    get_bool,
)

# Config
NUM_SAMPLES = int(os.environ.get("NUM_SAMPLES", "100000"))
SEED = int(os.environ.get("SEED", "42"))
OUT_DIR = os.environ.get("OUT_DIR", os.path.join(os.path.dirname(__file__), "plotsResults"))
os.makedirs(OUT_DIR, exist_ok=True)

set_seed(SEED)

# ─── 1) FLOAT [0.5, 1.5) ───
MIN_FLOAT, MAX_FLOAT = 0.5, 1.5
float_samples = [get_float_between(MIN_FLOAT, MAX_FLOAT) for _ in range(NUM_SAMPLES)]
plt.figure(figsize=(10, 4))
plt.hist(float_samples, bins=50, edgecolor="black", density=True)
plt.title(f"Distribution of {NUM_SAMPLES} FLOAT values [{MIN_FLOAT}, {MAX_FLOAT})")
plt.xlabel("Value"); plt.ylabel("Density"); plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "hist_float.png"), dpi=120)
plt.close()

# ─── 2) INT signed [-10, 10] ───
MIN_INT, MAX_INT = -10, 10
int_samples = [get_int_between(MIN_INT, MAX_INT, True, True) for _ in range(NUM_SAMPLES)]
int_counts = Counter(int_samples)
int_keys = sorted(int_counts.keys())
int_freqs = [int_counts[k] for k in int_keys]
plt.figure(figsize=(10, 4))
plt.bar(int_keys, int_freqs, edgecolor="black")
plt.title(f"Distribution of {NUM_SAMPLES} INT values [{MIN_INT}, {MAX_INT}]")
plt.xlabel("Value"); plt.ylabel("Frequency"); plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "hist_int.png"), dpi=120)
plt.close()

# ─── 2B) UINT32 [0, 2^32-1] ───
MIN_U32, MAX_U32 = 0, 4_294_967_295
u32_samples = [get_uint_between(MIN_U32, MAX_U32, True, True) for _ in range(NUM_SAMPLES)]
plt.figure(figsize=(10, 4))
plt.hist(u32_samples, bins=50, edgecolor="black", density=True)
plt.title(f"Distribution of {NUM_SAMPLES} UINT32 values [{MIN_U32}, {MAX_U32}]")
plt.xlabel("Value"); plt.ylabel("Density"); plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "hist_uint32.png"), dpi=120)
plt.close()

# ─── 3) NORMALIZED [0,1) ───
normalized_samples = [get_normalized() for _ in range(NUM_SAMPLES)]
plt.figure(figsize=(10, 4))
plt.hist(normalized_samples, bins=50, edgecolor="black", density=True)
plt.title(f"Distribution of {NUM_SAMPLES} pcg_normalized() values [0,1)")
plt.xlabel("Value"); plt.ylabel("Density"); plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "hist_normalized.png"), dpi=120)
plt.close()

# ─── 4) BOOL ───
bool_samples = [get_bool() for _ in range(NUM_SAMPLES)]
bool_counts = Counter(bool_samples)
bool_labels = ["False", "True"]
bool_values = [bool_counts.get(False, 0), bool_counts.get(True, 0)]
plt.figure(figsize=(6, 4))
plt.bar(bool_labels, bool_values, edgecolor="black")
plt.title(f"Distribution of {NUM_SAMPLES} pcg_bool() samples")
plt.ylabel("Frequency"); plt.grid(True, axis="y")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "hist_bool.png"), dpi=120)
plt.close()

print(f"✅ Saved plots to: {OUT_DIR}")
