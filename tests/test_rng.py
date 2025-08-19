import os, sys
# Ensure 'bindings' package is importable (project root on sys.path)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bindings.pcg import (
    set_seed,
    get_uint32,
    get_normalized,
    get_int_between,
    get_uint_between,   # unsigned helper for 0..2^32-1
    get_float_between,
    get_bool,
)

import ctypes  # only for reset/state calls as requested

# --- Load shared library with a robust absolute path ---
_here = os.path.abspath(os.path.dirname(__file__))
_so_path = os.path.abspath(os.path.join(_here, "..", "build", "libpcg_rng.so"))
lib = ctypes.CDLL(_so_path)

# --- Declare ctypes signatures for the direct calls you use ---
lib.reset_rng.argtypes  = [ctypes.c_uint64]
lib.reset_rng.restype   = None

lib.get_state.argtypes  = []
lib.get_state.restype   = ctypes.c_uint64

lib.set_state.argtypes  = [ctypes.c_uint64]
lib.set_state.restype   = None

lib.pcg32.argtypes      = []
lib.pcg32.restype       = ctypes.c_uint32  # ensure 32-bit return

# ▶️ Initialize seed
set_seed(37)

# 🔢 Basic uint32 value
print(f"🔢 pcg32: {get_uint32()}")

# 🎲 Signed int in range
print(f"🎲 int [-10,10]: {get_int_between(-10, 10, True, True)}")
print(f"🎲 int (1,6]: {get_int_between(1, 6, False, True)}")

# 📈 Normalized before float
normalized = get_normalized()
print(f"📈 normalized (before float): {normalized}")

# 🧮 Float in [0.5, 1.5)
val = get_float_between(0.5, 1.5)
print(f"🧮 float [0.5, 1.5): {val} (raw) | {val:.3f} (formatted)")

# ✅ Boolean quick test
true_count = 0
false_count = 0
for _ in range(1000):
    if get_bool():
        true_count += 1
    else:
        false_count += 1
print(f"✅ booleans (1000 draws): True = {true_count}, False = {false_count}")

# 🧩 UNSIGNED (uint32) tests
# Small window
u_min, u_max = 100, 200
u_val = get_uint_between(u_min, u_max, True, True)
print(f"🧩 uint32 [{u_min},{u_max}]: {u_val}")

# Full 32-bit span (0..2^32-1)
u_full = get_uint_between(0, 4_294_967_295, True, True)
print(f"🧩 uint32 [0, 2^32-1]: {u_full}")

# ♻️ Reset seed via ctypes (as per your original style)
lib.reset_rng(ctypes.c_uint64(99))
print(f"♻️ reset with seed 99 → pcg32: {lib.pcg32()}")

# 💾 Save & restore state via ctypes
set_seed(123)
first = get_uint32()
print(f"🎲 first value: {first}")

saved = lib.get_state()
second = get_uint32()
print(f"🎲 second value: {second}")
print(f"💾 saved state: {saved}")

lib.set_state(saved)
print(f"🎯 same second value again: {get_uint32()}")  # should match 'second'
