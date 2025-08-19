# 🎲 PCG32 Random Number Generator – High-Quality, Bindable RNG in C++ + Python

This project is a high-quality implementation of the **PCG32** pseudo-random number generator (PRNG), written in C++ and exposed to Python via `ctypes`.

Designed with readability and auditability in mind, it is ideal for learning, research, or integration into systems where randomness quality is critical.

---

## 🚀 Features

- ✅ Based on the **PCG32** algorithm: simple, fast, and statistically sound
- 🧠 Implemented in **C++**
- 🧩 Python bindings using **`ctypes`**
- 🌐 WebAssembly build for direct usage in JavaScript / Web projects
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
├── web/dist/                  # WebAssembly build output
│   ├── pcg_rng.js
│   └── pcg_rng.wasm
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
- *(Optional, for WebAssembly)*: [Emscripten SDK](https://emscripten.org/docs/getting_started/downloads.html)

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

### 🔹 WebAssembly build

The `web/dist/` folder already contains a **precompiled WebAssembly build**:

- `pcg_rng.js` (JavaScript loader)  
- `pcg_rng.wasm` (compiled WebAssembly module)  

You can import and use it directly in a web project:

```html
<script type="module">
  import initWasm from './web/dist/pcg_rng.js';

  const run = async () => {
    const wasm = await initWasm();

    // Wrap exported functions
    const pcg32 = wasm.cwrap('pcg32', 'number', []);
    const setSeed = wasm.cwrap('set_seed', null, ['number']);

    // Initialize seed
    setSeed(Date.now());

    // Generate a random number
    console.log("Random uint32:", pcg32());
  };

  run();
</script>

```

---

#### 🔨 Build manually (optional)

If you want to rebuild the WASM module yourself:

```bash
# Clone and activate Emscripten if not already installed
git clone https://github.com/emscripten-core/emsdk.git
cd emsdk
./emsdk install latest
./emsdk activate latest
source ./emsdk_env.sh

# IMPORTANT: before building, always load the Emscripten environment
source ./emsdk_env.sh

# Build WebAssembly module
mkdir -p web/dist
emcc src/pcg_rng.cpp -O3 -s WASM=1 -s STRICT=1 \
  -s ALLOW_MEMORY_GROWTH=1 \
  -s MODULARIZE=1 \
  -s EXPORT_ES6=1 \
  -s ENVIRONMENT=web \
  -s EXPORTED_RUNTIME_METHODS='["cwrap"]' \
  -s EXPORTED_FUNCTIONS='[
    "_set_seed",
    "_reset_rng",
    "_get_state",
    "_set_state",
    "_pcg32",
    "_pcg_normalized",
    "_pcg_between",
    "_pcg_between_u32",
    "_pcg_between_float",
    "_pcg_bool"
  ]' \
  -o web/dist/pcg_rng.js

```

---


## ✅ Proven Randomness: BigCrush Results

The implementation has successfully passed the full **BigCrush** battery from TestU01.

📄 See results in [`bigcrush_results.txt`](./bigcrush_results.txt)

---

## 🧠 Notes

- The generator maintains internal state, with full access via get_state and set_state.
- Currently built and tested on **Linux (Ubuntu)**.
- Windows compatibility is not guaranteed (but can likely be adapted via MSVC or MinGW).

---

## 🔐 License

MIT — use freely, credit appreciated.