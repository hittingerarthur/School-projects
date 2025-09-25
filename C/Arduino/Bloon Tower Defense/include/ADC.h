#ifndef ADC_H
#define ADC_H

#include <avr/io.h>

void ADC_init() {
    // Reference voltage: AVcc
    ADMUX |= (1 << REFS0);
    // Prescaler: 128
    ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);
    // Enable ADC
    ADCSRA |= (1 << ADEN);
}

uint16_t ADC_read(uint8_t channel) {
    // Select ADC channel
    ADMUX = (ADMUX & 0xF0) | (channel & 0x0F);
    // Start conversion
    ADCSRA |= (1 << ADSC);
    // Wait for conversion to complete
    while (ADCSRA & (1 << ADSC));
    // Return ADC value
    return ADC;
}

#endif // ADC_H
