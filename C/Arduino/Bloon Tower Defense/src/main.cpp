#include <Arduino.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdlib.h>
#include <string.h>

#include "LCD.h"
#include "ADC.h"
#include "melody.h"
#include "ageofwar.h"
#include "classic.h"
#include "pacman.h"
#include "menu.h"
#include "map.h"
#include "balloons.h"

// ------------------------------------------------------------
// Custom Time Base Implementation Using Timer2
// ------------------------------------------------------------
volatile uint32_t custom_millis_counter = 0;

// Timer2 Compare Match ISR: increments our custom millisecond counter
ISR(TIMER2_COMPA_vect) {
    custom_millis_counter++;
}


// POINT DE VIE 
uint8_t player_HP;

// Returns the current custom millisecond count
uint32_t custom_millis() {
    uint32_t ms;
    cli();
    ms = custom_millis_counter;
    sei();
    return ms;
}

// Initialize Timer2 to generate an interrupt every 1 millisecond
void custom_timebase_init() {
    cli();
    // Set Timer2 to CTC mode (Clear Timer on Compare)
    TCCR2A = (1 << WGM21);  // WGM21=1 for CTC, WGM20=0
    TCCR2B = 0;

    // CPU=16MHz, we want 1ms:
    // Prescaler=64 -> Tick=4us. For 1ms=1000us/4us=250 counts
    OCR2A = 249; 
    // Start Timer2 with prescaler 64: CS22=1, CS21=1, CS20=0 (0x06)
    TCCR2B |= (1 << CS22) | (1 << CS21);
    // Enable compare match interrupt
    TIMSK2 = (1 << OCIE2A);

    sei();
}
// ------------------------------------------------------------

// ISR for melody timing (existing code)
ISR(TIMER0_COMPA_vect) {
    if (music_on && current_melody_frequencies && current_melody_durations) {
        if (melody_index < current_melody_size) {
            if (note_elapsed == 0) {
                uint16_t frequency = current_melody_frequencies[melody_index];
                if (frequency == 0) {
                    TCCR1B &= ~((1 << CS11) | (1 << CS10));
                } else {
                    uint16_t top = (uint16_t)(F_CPU / (frequency * 8UL)) - 1;
                    ICR1 = top;
                    OCR1B = top / 2;
                    TCCR1B &= ~((1 << CS12) | (1 << CS10));
                    TCCR1B |= (1 << CS11);
                }
            }
            note_elapsed++;
            if (note_elapsed >= current_melody_durations[melody_index]) {
                note_elapsed = 0;
                melody_index++;
                if (current_state == STATE_GAME_MAP && melody_index >= current_melody_size) {
                    melody_index = 0;
                }
                TCCR1B &= ~((1 << CS11) | (1 << CS10));
            }
        } else {
            melody_index = 0;
            note_elapsed = 0;
            if (current_state == STATE_GAME_MAP) {
                melody_index = 0;
                note_elapsed = 0;
            }
        }
    } else {
        TCCR1B &= ~((1 << CS11) | (1 << CS10));
    }
}

void buzzer_init() {
    SET_OUTPUT(B, PB2);
    TCCR1A = (1 << COM1B1) | (1 << WGM11);
    TCCR1B = (1 << WGM13) | (1 << WGM12);
}

void timer0_init() {
    // Configure Timer0 as in your original code to handle melody timing
    TCCR0A = (1 << WGM01);
    TCCR0B = (1 << CS01) | (1 << CS00);
    OCR0A = 249;
    TIMSK0 = (1 << OCIE0A);
}

uint32_t lastBalloonUpdateTime = 0;

int main(void) {
    LCD_init();
    ADC_init();
    buzzer_init();
    timer0_init();
    custom_timebase_init(); // Initialize our custom time base

    DDRC &= ~(1 << PC2);
    PORTC |= (1 << PC2);

    DDRC &= ~((1 << PC3) | (1 << PC4));
    PORTC |= (1 << PC3) | (1 << PC4);

    map_display_init();
    draw_map();

    current_melody_frequencies = melody_frequencies_melody;
    current_melody_durations = melody_durations_melody;
    current_melody_size = MELODY_SIZE_MELODY;
    melody_index = 0;
    note_elapsed = 0;

    init_balloons();
    update_menu();

    sei();

    while (1) {
        handle_input();

        uint32_t currentTime = custom_millis(); // Use custom time base here
        if (wave_started && (currentTime - lastBalloonUpdateTime >= 250)) {
            lastBalloonUpdateTime = currentTime;
            update_balloons();
            draw_map();
            draw_balloons_on_map();
        }

        _delay_ms(10);
    }
    return 0;
}
