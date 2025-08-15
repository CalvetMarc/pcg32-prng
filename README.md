# 🎲 PCG32 Random Number Generator – High-Quality, Bindable RNG in C++ + Python

This project is a high-quality implementation of the **PCG32** pseudo-random number generator (PRNG), written in C++ and exposed to Python via `ctypes`.

Designed with readability and auditability in mind, it is ideal for learning, research, or integration into systems where randomness quality is critical.

---

## 🚀 Features

- ✅ Based on the **PCG32** algorithm: simple, fast, and statistically sound
- 🧠 Implemented in **C++**
- 🧩 Python bindings using **`ctypes`**
- 📈 Visual distribution plots (`matplotlib`)
- 📊 Full access to:
  - `uint32` values
  - normalized floats in [0.0, 1.0)
  - integers and floats between arbitrary bounds
  - booleans
  - internal RNG state (get/set)
- 🧪 Successfully passed **BigCrush** test suite (see `bigcrush_results.txt`)

---

## 🛠 Folder Structure

```
libpcg_rng/
├── bindings/              # Python bindings to the C++ shared library
│   └── pcg.py
├── build/                 # (empty) used as build output dir for .so
├── src/                   # Core C++ RNG implementation
│   ├── pcg_rng.cpp
│   └── pcg_rng.hpp
├── tests/                 # Usage demos and distribution analysis
│   ├── test_hist.py       # Shows histograms (float, int, bool)
│   └── test_rng.py        # Prints results, tests state management
├── Makefile               # Compiles to build/libpcg_rng.so
└── bigcrush_results.txt   # Output from BigCrush test battery
```

---

## 📦 Build Instructions

Make sure you’re on **Linux** or **WSL**. This repo builds a shared library used by Python.

### Requirements:
- `make`
- `g++`
- `python3`
- `matplotlib` (for histogram plotting)

### 1. Build the shared library

```bash
cd libpcg_rng
make
```

This will generate `build/libpcg_rng.so`.

### 2. Run a Python usage demo

```bash
python3 tests/test_rng.py
```

### 3. Plot distributions

```bash
python3 tests/test_hist.py
```

---

## ✅ Proven Randomness: BigCrush Results

The implementation has successfully passed the full **BigCrush** battery from TestU01.

📄 See results in [`bigcrush_results.txt`](./bigcrush_results.txt)

---

## 🧠 Notes

- This is a stateless wrapper by default, but state management (`get_state`, `set_state`) is exposed for advanced usage.
- Currently built and tested on **Linux (Ubuntu)**.
- Windows compatibility is not guaranteed (but can likely be adapted via MSVC or MinGW).

---

## 🔐 License

MIT — use freely, credit appreciated.