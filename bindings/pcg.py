import ctypes
import os

# 📍 Ruta absoluta al .so
path = os.path.abspath(os.path.dirname(__file__))
lib_path = os.path.abspath(os.path.join(path, "..", "build", "libpcg_rng.so"))

# 📦 Carrega la llibreria
pcg = ctypes.CDLL(lib_path)

# 🔧 Definició de tipus per cada funció
pcg.set_seed.argtypes = [ctypes.c_uint64]
pcg.pcg32.restype = ctypes.c_uint32
pcg.pcg_normalized.restype = ctypes.c_double
pcg.pcg_between.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_bool]
pcg.pcg_between.restype = ctypes.c_int
pcg.pcg_between_float.argtypes = [ctypes.c_double, ctypes.c_double]
pcg.pcg_between_float.restype = ctypes.c_double
pcg.pcg_bool.restype = ctypes.c_bool

# 🎯 Funcions Python
def set_seed(seed: int):
    pcg.set_seed(seed)

def get_uint32() -> int:
    return pcg.pcg32()

def get_normalized() -> float:
    return pcg.pcg_normalized()

def get_int_between(min_val: int, max_val: int, inc_min=True, inc_max=True) -> int:
    return pcg.pcg_between(min_val, max_val, inc_min, inc_max)

def get_float_between(min_val: float, max_val: float) -> float:
    return pcg.pcg_between_float(min_val, max_val)

def get_bool() -> bool:
    return pcg.pcg_bool()