import matplotlib.pyplot as plt
from collections import Counter
from bindings.pcg import (
    set_seed,
    get_float_between,
    get_int_between,
    get_normalized,
    get_bool,
)

NUM_SAMPLES = 100_000
set_seed(42)

# ─── 1. FLOAT ───
MIN_FLOAT = 0.5
MAX_FLOAT = 1.5
float_samples = [get_float_between(MIN_FLOAT, MAX_FLOAT) for _ in range(NUM_SAMPLES)]

plt.figure(figsize=(10, 4))
plt.hist(float_samples, bins=50, edgecolor='black')
plt.title(f"Distribution of {NUM_SAMPLES} FLOAT values between {MIN_FLOAT} and {MAX_FLOAT}")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.grid(True)

# ─── 2. INT ───
MIN_INT = -10
MAX_INT = 10
int_samples = [get_int_between(MIN_INT, MAX_INT, True, True) for _ in range(NUM_SAMPLES)]
int_counts = Counter(int_samples)
int_keys = sorted(int_counts.keys())
int_freqs = [int_counts[k] for k in int_keys]

plt.figure(figsize=(10, 4))
plt.bar(int_keys, int_freqs, edgecolor='black')
plt.title(f"Distribution of {NUM_SAMPLES} INT values between {MIN_INT} and {MAX_INT}")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.grid(True)

# ─── 3. NORMALIZED ───
normalized_samples = [get_normalized() for _ in range(NUM_SAMPLES)]

plt.figure(figsize=(10, 4))
plt.hist(normalized_samples, bins=50, edgecolor='black')
plt.title(f"Distribution of {NUM_SAMPLES} pcg_normalized() values")
plt.xlabel("Value (in range [0.0, 1.0))")
plt.ylabel("Frequency")
plt.grid(True)

# ─── 4. BOOL ───
bool_samples = [get_bool() for _ in range(NUM_SAMPLES)]
bool_counts = Counter(bool_samples)
bool_labels = ["False", "True"]
bool_values = [bool_counts[False], bool_counts[True]]

plt.figure(figsize=(6, 4))
plt.bar(bool_labels, bool_values, edgecolor='black', color=["gray", "green"])
plt.title(f"Distribution of {NUM_SAMPLES} pcg_bool() samples")
plt.ylabel("Frequency")
plt.grid(True, axis='y')

# ✅ Show all plots
plt.show()
