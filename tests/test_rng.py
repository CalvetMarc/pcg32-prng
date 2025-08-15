from bindings.pcg import (
    set_seed,
    get_uint32,
    get_normalized,
    get_int_between,
    get_float_between,
    get_bool,
)
import ctypes  # Només per definir reset_rng i control d'estat manual

# 🔧 Funcions extres des de la llibreria compartida
lib = ctypes.CDLL('./build/libpcg_rng.so')
lib.reset_rng.argtypes = [ctypes.c_uint64]
lib.get_state.restype = ctypes.c_uint64
lib.set_state.argtypes = [ctypes.c_uint64]

# ▶️ Inicialitza llavor
set_seed(37)

# 🔢 Valor bàsic
print(f"🔢 pcg32: {get_uint32()}")

# 🎲 Enter entre valors
print(f"🎲 Enter [-10,10]: {get_int_between(-10, 10, True, True)}")
print(f"🎲 Enter (1,6]: {get_int_between(1, 6, False, True)}")

normalized = get_normalized()
print(f"📈 Normalized abans del float: {normalized}")


# 🧮 Float amb 3 decimals
val = get_float_between(0.5, 1.5)
print(f"🧮 Float [0.5, 1.5] sense limitar decimals: {val} (raw) | {val:.3f} (formatat)")

# ✅ Test de booleans
true_count = 0
false_count = 0
for _ in range(1000):
    if get_bool():
        true_count += 1
    else:
        false_count += 1
print(f"✅ Booleans generats (1000 tirades): True = {true_count}, False = {false_count}")

# ♻️ Reset de llavor
lib.reset_rng(99)
print(f"♻️ Reset amb seed 99 → pcg32: {lib.pcg32()}")

# 💾 Test de guardar i restaurar estat
set_seed(123)
first = get_uint32()
print(f"🎲 First value: {first}")
saved = lib.get_state()
second = get_uint32()
print(f"🎲 Second value: {second}")
print(f"💾 Saved state: {saved}")
lib.set_state(saved)
print(f"🎯 Same second value again: {get_uint32()}")  # Ha de coincidir amb el segon valor
