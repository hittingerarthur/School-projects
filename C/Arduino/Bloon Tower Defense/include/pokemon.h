#ifndef POKEMON_H
#define POKEMON_H

#include <stdint.h>

#define MELODY_SIZE_POKEMON 48 // Total number of notes in the melody

// Frequencies in Hz (Notes)
const uint16_t melody_frequencies_pokemon[MELODY_SIZE_POKEMON] = {
    587, 880, 740, 587, // NOTE_D5, NOTE_A5, NOTE_FS5, NOTE_D5
    659, 740, 784, 740, // NOTE_E5, NOTE_FS5, NOTE_G5, NOTE_FS5
    659, 740, 587, 587, // NOTE_E5, NOTE_FS5, NOTE_D5, NOTE_D5
    587, 880, 740, 587, // NOTE_D5, NOTE_A5, NOTE_FS5, NOTE_D5
    659, 740, 784, 740, // NOTE_E5, NOTE_FS5, NOTE_G5, NOTE_FS5
    740, 659, 740, 587, // NOTE_FS5, NOTE_E5, NOTE_FS5, NOTE_D5
    587, 880, 740, 587, // NOTE_D5, NOTE_A5, NOTE_FS5, NOTE_D5
    659, 740, 784, 740, // NOTE_E5, NOTE_FS5, NOTE_G5, NOTE_FS5
};

// Durations in milliseconds
const int16_t melody_durations_pokemon[MELODY_SIZE_POKEMON] = {
    -4, 8, 8, 8, // Dotted quarter note, eighth note, etc.
    -4, 8, 4, -4, // E5 and FS5 durations
    8, 4, -2, -4, // Continue with rest durations
    8, 8, 8, -4,
    8, 4, -1, -4,
    8, 4, -2, -4,
    8, 8, 8, -4,
    8, 4, -1, -4
};

#endif // POKEMON_H
