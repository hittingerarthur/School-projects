// pacman.h
#ifndef PACMAN_H
#define PACMAN_H

#include <stdint.h>

#define MELODY_SIZE_PACMAN 31 // Total number of notes in the melody

// Frequencies in Hz (Notes)
const uint16_t melody_frequencies_pacman[MELODY_SIZE_PACMAN] = {
    494, 988, 740, 622, 
    988, 740, 622, 523,
    1047, 1568, 1319, 1047, 1568, 1319,
    494, 988, 740, 622, 988, 
    740, 622, 622, 659, 698, 
    698, 740, 784, 784, 830, 880, 988
};

// Durations in milliseconds
const uint16_t melody_durations_pacman[MELODY_SIZE_PACMAN] = {
    63, 63, 63, 63,
    31, 63, 125, 63,
    63, 63, 63, 31, 63, 125,
    63, 63, 63, 63, 31,
    63, 125, 31, 31, 31,
    31, 31, 31, 31, 31, 63, 125
};

#endif // PACMAN_H
