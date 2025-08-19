#include "pcg_rng.hpp"
#include <cstdint>
#include <algorithm>
#include <limits>

// --- Internal state (64-bit LCG) ---
static uint64_t state = 0x853c49e6748fea9bULL;
static constexpr uint64_t MULT = 6364136223846793005ULL;
static constexpr uint64_t INC  = 1442695040888963407ULL;

extern "C" {

    // 🌱 Seed (PCG-recommended pattern; fixed INC stream)
    void set_seed(uint64_t seed) {
        state = 0ull;
        (void)pcg32();      // advance with fixed INC
        state += seed;
        (void)pcg32();      // stabilize
    }

    void reset_rng(uint64_t seed) { set_seed(seed); }

    uint64_t get_state() { return state; }
    void     set_state(uint64_t s) { state = s; }

    // Core PCG XSH RR 64->32
    uint32_t pcg32() {
        uint64_t oldstate = state;
        state = oldstate * MULT + INC;

        uint32_t xorshifted = static_cast<uint32_t>(((oldstate >> 18u) ^ oldstate) >> 27u);
        uint32_t rot        = static_cast<uint32_t>(oldstate >> 59u);
        return (xorshifted >> rot) | (xorshifted << ((-rot) & 31));
    }

    // Normalized double in [0, 1)
    double pcg_normalized() {
        // 2^32 = 4294967296.0; pcg32() max is 0xFFFFFFFF → never returns 1.0
        return static_cast<double>(pcg32()) / 4294967296.0;
    }

    // -------- Signed int32 helper (unbiased) --------
    int pcg_between(int min, int max, bool incMin, bool incMax) {
        if (min > max) std::swap(min, max);

        // Guard against overflow when excluding bounds
        if (!incMin) { if (min == std::numeric_limits<int>::max()) return min; ++min; }
        if (!incMax) { if (max == std::numeric_limits<int>::min()) return max; --max; }

        if (max < min) return min; // empty range → return min

        // Compute range as uint32 to avoid intermediate overflows
        uint32_t range = static_cast<uint32_t>(
            static_cast<uint64_t>(max) - static_cast<uint64_t>(min) + 1ull
        );

        // Rejection sampling: threshold = (-range % range) == (2^32 % range)
        uint32_t threshold = static_cast<uint32_t>(-range) % range;

        uint32_t r;
        do { r = pcg32(); } while (r < threshold);

        return min + static_cast<int>(r % range);
    }

    // -------- Unsigned uint32 helper (unbiased) --------
    uint32_t pcg_between_u32(uint32_t min, uint32_t max, bool incMin, bool incMax) {
        if (min > max) std::swap(min, max);
        if (!incMin) ++min;
        if (!incMax) --max;
        if (max < min) return min;

        uint32_t range = max - min + 1u;

        // Full 32-bit span → use pcg32 directly (no bias)
        if (range == 0u) {
            return pcg32();
        }

        uint32_t threshold = static_cast<uint32_t>(-range) % range;

        uint32_t r;
        do { r = pcg32(); } while (r < threshold);
        return min + (r % range);
    }

    // Uniform double in [min, max)
    double pcg_between_float(double min, double max) {
        if (min > max) std::swap(min, max);
        return min + (max - min) * pcg_normalized();
    }

    // Boolean from MSB (more robust than using LSB)
    bool pcg_bool() {
        return (pcg32() >> 31) != 0;
    }

} // extern "C"
