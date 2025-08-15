#include "pcg_rng.hpp"
#include <cmath>  // per powf i roundf
#include <algorithm> // per std::clamp

// Estat intern del generador
static uint64_t state = 0x853c49e6748fea9bULL;
static constexpr uint64_t MULT = 6364136223846793005ULL;
static constexpr uint64_t INC  = 1442695040888963407ULL;

// Funcions públiques exportables
extern "C" {

// 🌱 Inicialitza la llavor
void set_seed(uint64_t seed) {
    state = 0;
    pcg32();  // descarrega estat inicial
    state += seed;
    pcg32();  // estabilitza estat
}

void reset_rng(uint64_t seed) {
    state = 0;
    pcg32();       // descarrega estat inicial
    state += seed;
    pcg32();       // estabilitza estat
}

uint64_t get_state() {
    return state;
}

void set_state(uint64_t s) {
    state = s;
}


// 🔢 Retorna enter de 32 bits
uint32_t pcg32() {
    uint64_t oldstate = state;
    state = oldstate * MULT + INC;

    uint32_t xorshifted = static_cast<uint32_t>(((oldstate >> 18u) ^ oldstate) >> 27u);
    uint32_t rot = static_cast<uint32_t>(oldstate >> 59u);
    return (xorshifted >> rot) | (xorshifted << ((-rot) & 31));
}

// 🎯 Retorna float normalitzat [0, 1)
double pcg_normalized() {
    return static_cast<double>(pcg32()) / 4294967296.0;
}

// 🎲 Enter entre mínim i màxim, amb control d’inclusió
int pcg_between(int min, int max, bool incMin, bool incMax) {
    if (min > max) std::swap(min, max);      // 🟢 Intercanvi
    if (!incMin) min += 1;
    if (!incMax) max -= 1;
    if (max < min) return min;               // 🟢 Cas límit (rang buit)
    return min + (pcg32() % (max - min + 1));
}

// 🧮 Float entre min i max amb decimals controlats
double pcg_between_float(double min, double max) {
    if (min > max) std::swap(min, max);  // Garantir ordre
    double range = max - min;
    return min + range * pcg_normalized();  // [0, 1) * rang + mínim
}


bool pcg_bool(){
    return (pcg32() & 1);
}

} // fi extern "C"
