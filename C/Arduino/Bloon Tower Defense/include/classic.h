#ifndef CLASSIC_H
#define CLASSIC_H

#include <stdint.h>

#define MELODY_SIZE_CLASSIC 24 // Number of notes in the melody

// Frequencies in Hz (all within the playable range)
const uint16_t melody_frequencies_classic[MELODY_SIZE_CLASSIC] = {
    659, 831, 988, 1319, // Measure 1
    740, 880, 1109, 1480, // Measure 2
    880, 1109, 1319, 1760, // Measure 3
    831, 988, 1319, 1661, // Measure 4
    740, 880, 1109, 1480, // Measure 5
    659, 831, 988, 1319  // Measure 6
};

// Durations in milliseconds
const uint16_t melody_durations_classic[MELODY_SIZE_CLASSIC] = {
    387, 387, 387, 387, // Measure 1
    387, 387, 387, 387, // Measure 2
    387, 387, 387, 387, // Measure 3
    387, 387, 387, 387, // Measure 4
    387, 387, 387, 387, // Measure 5
    387, 387, 387, 387  // Measure 6
};

#endif // CLASSIC_H
