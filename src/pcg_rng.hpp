#pragma once
#include <cstdint>

extern "C" {
    void set_seed(uint64_t seed);
    void reset_rng(uint64_t seed);

    uint64_t get_state();       // Obtenir estat actual
    void set_state(uint64_t s); // Restaurar estat manualment


    uint32_t pcg32();
    double pcg_normalized(); // entre [0, 1)

    // 🔢 Enter entre min i max amb inclusivitat configurada
    int pcg_between(int min, int max, bool incMin, bool incMax);

    // 🎯 Float entre min i max amb X decimals de precisió
    double pcg_between_float(double min, double max);

    bool pcg_bool();

}
