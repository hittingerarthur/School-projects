#ifndef LCD_H
#define LCD_H

#include <avr/io.h>
#include <util/delay.h>

// Define the LCD control pins
#define LCD_RS PB0 // RS → PB0 (Digital Pin 8)
#define LCD_E  PB1 // E  → PB1 (Digital Pin 9)

// Define the LCD data pins
#define LCD_D4 PD4 // D4 → PD4 (Digital Pin 4)
#define LCD_D5 PD5 // D5 → PD5 (Digital Pin 5)
#define LCD_D6 PD6 // D6 → PD6 (Digital Pin 6)
#define LCD_D7 PD7 // D7 → PD7 (Digital Pin 7)

// Macros to simplify pin configuration
#define SET_OUTPUT(port, pin) (DDR##port |= (1 << pin))
#define SET_INPUT(port, pin)  (DDR##port &= ~(1 << pin))
#define SET_HIGH(port, pin)   (PORT##port |= (1 << pin))
#define SET_LOW(port, pin)    (PORT##port &= ~(1 << pin))

// Function prototypes
void LCD_init();
void LCD_command(uint8_t cmd);
void LCD_data(uint8_t data);
void LCD_set_cursor(uint8_t row, uint8_t col);
void LCD_print(const char* str);

// Function implementations

// Initialize the LCD in 4-bit mode
void LCD_init() {
    // Set control pins as output
    SET_OUTPUT(B, LCD_RS);
    SET_OUTPUT(B, LCD_E);
    
    // Set data pins as output
    SET_OUTPUT(D, LCD_D4);
    SET_OUTPUT(D, LCD_D5);
    SET_OUTPUT(D, LCD_D6);
    SET_OUTPUT(D, LCD_D7);
    
    // Initial delay to allow LCD to power up
    _delay_ms(50);
    
    // Initialize in 4-bit mode
    // According to the HD44780 datasheet, the sequence is critical
    // Send 0x33 to initialize
    LCD_command(0x33);
    _delay_ms(5);
    
    // Send 0x32 to set to 4-bit mode
    LCD_command(0x32);
    _delay_ms(5);
    
    // Function set: 4-bit mode, 2 lines, 5x8 dots
    LCD_command(0x28);
    _delay_ms(5);
    
    // Display on, cursor off, blink off
    LCD_command(0x0C);
    _delay_ms(5);
    
    // Clear display
    LCD_command(0x01);
    _delay_ms(5);
    
    // Entry mode set: Increment cursor, no shift
    LCD_command(0x06);
    _delay_ms(5);
}

// Send a command byte to the LCD
void LCD_command(uint8_t cmd) {
    // RS = 0 for command
    SET_LOW(B, LCD_RS);
    
    // Send higher nibble
    PORTD = (PORTD & 0x0F) | (cmd & 0xF0); // Mask lower 4 bits of PORTD, OR with higher nibble
    // Toggle E to latch the data
    SET_HIGH(B, LCD_E);
    _delay_us(1);
    SET_LOW(B, LCD_E);
    _delay_us(200);
    
    // Send lower nibble
    PORTD = (PORTD & 0x0F) | ((cmd << 4) & 0xF0);
    // Toggle E to latch the data
    SET_HIGH(B, LCD_E);
    _delay_us(1);
    SET_LOW(B, LCD_E);
    _delay_us(200);
}

// Send a data byte to the LCD
void LCD_data(uint8_t data) {
    // RS = 1 for data
    SET_HIGH(B, LCD_RS);
    
    // Send higher nibble
    PORTD = (PORTD & 0x0F) | (data & 0xF0); // Mask lower 4 bits of PORTD, OR with higher nibble
    // Toggle E to latch the data
    SET_HIGH(B, LCD_E);
    _delay_us(1);
    SET_LOW(B, LCD_E);
    _delay_us(200);
    
    // Send lower nibble
    PORTD = (PORTD & 0x0F) | ((data << 4) & 0xF0);
    // Toggle E to latch the data
    SET_HIGH(B, LCD_E);
    _delay_us(1);
    SET_LOW(B, LCD_E);
    _delay_us(200);
}

// Set the cursor to a specific row and column
void LCD_set_cursor(uint8_t row, uint8_t col) {
    // Rows: 0 or 1
    // Columns: 0-15
    uint8_t address;
    switch(row) {
        case 0:
            address = 0x80 + col;
            break;
        case 1:
            address = 0xC0 + col;
            break;
        default:
            address = 0x80; // Default to first line
            break;
    }
    LCD_command(address);
}

// Print a string to the LCD
void LCD_print(const char* str) {
    while(*str) {
        LCD_data(*str++);
    }
}

#endif // LCD_H