#pragma once
#include <cstdint>

extern "C" {

    // --- Seeding / state ---
    void     set_seed(uint64_t seed);
    void     reset_rng(uint64_t seed);   // alias to set_seed
    uint64_t get_state();                // read current internal state
    void     set_state(uint64_t s);      // set internal state (use carefully)

    // --- Core generator ---
    uint32_t pcg32();                    // PCG XSH RR 64->32 step
    double   pcg_normalized();           // uniform in [0, 1)

    // --- Mapped helpers (unbiased) ---
    int      pcg_between(int min, int max, bool incMin, bool incMax);              // signed 32-bit range
    uint32_t pcg_between_u32(uint32_t min, uint32_t max, bool incMin, bool incMax); // unsigned 32-bit range

    double   pcg_between_float(double min, double max); // uniform in [min, max)
    bool     pcg_bool();                                // boolean from MSB

} // extern "C"
