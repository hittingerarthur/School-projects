#ifndef MAP_H
#define MAP_H

#include <Adafruit_GFX.h>
#include <Adafruit_ST7735.h>
#include <SPI.h>
#include "menu.h"

extern void draw_balloons_on_map();

#define ST77XX_BLACK   0x0000
#define ST77XX_BLUE    0x001F
#define ST77XX_GREEN   0x07E0
#define ST77XX_PINK    0xFD40 
#define ST77XX_RED     0xF81F
#define HIGHLIGHT_COLOR ST77XX_RED
#define BACKGROUND_COLOR ST77XX_BLACK

extern uint8_t map_matrix[8][8];
uint8_t map_matrix[8][8] = {
    {0,   0,  0,  0,  0,  0, 26, 27},
    {1,   2,  3,  0,  0,  0, 25,  0},
    {0,   0,  4,  0, 22, 23, 24,  0},
    {0,   6,  5,  0, 21,  0,  0,  0},
    {0,   7,  0,  0, 20, 19, 18,  0},
    {0,   8,  0,  0,  0,  0, 17,  0},
    {0,   9,  0, 13, 14, 15, 16,  0},
    {0,  10, 11,12,  0,  0,  0,  0}
};

extern Adafruit_ST7735 tft;
Adafruit_ST7735 tft = Adafruit_ST7735(11, 13, 3, 2, 12);

void map_display_init() {
    tft.initR(INITR_144GREENTAB);
    tft.setRotation(2);
    tft.invertDisplay(false);
    tft.fillScreen(BACKGROUND_COLOR);
}

void draw_map() {
    const int cell_width = 16;  
    const int cell_height = 16;

    for (int row = 0; row < 8; row++) {
        for (int col = 0; col < 8; col++) {
            int x = col * cell_width;
            int y = row * cell_height;
            uint8_t cell_value = map_matrix[row][col];
            uint16_t fill_color;
            if ((cell_value >=1 && cell_value <=27)) {
                fill_color = ST77XX_BLACK;
            } else if (cell_value == 0) {
                fill_color = ST77XX_GREEN; 
            } else if (cell_value == 100) {
                fill_color = ST77XX_RED;
            } else if (cell_value == 101) {
                fill_color = ST77XX_BLUE;
            } else if (cell_value == 102) {
                fill_color = ST77XX_PINK;
            } else {
                fill_color = ST77XX_BLACK;
            }
            tft.fillRect(x, y, cell_width, cell_height, fill_color);
        }
    }

    if (wave_started) {
        draw_balloons_on_map();
    }
}

void draw_map_with_highlight(uint8_t prev_row, uint8_t prev_col, uint8_t highlight_row, uint8_t highlight_col) {
    const int cell_width = 16;  
    const int cell_height = 16;

    auto get_color = [&](uint8_t val)->uint16_t {
        if (val>=1 && val<=27) return ST77XX_BLACK;
        else if (val==0) return ST77XX_GREEN;
        else if (val==100) return ST77XX_RED;
        else if (val==101) return ST77XX_BLUE;
        else if (val==102) return ST77XX_PINK;
        return ST77XX_BLACK;
    };

    uint8_t cell_prev = map_matrix[prev_row][prev_col];
    tft.fillRect(prev_col*cell_width, prev_row*cell_height, cell_width, cell_height, get_color(cell_prev));

    uint8_t cell_new = map_matrix[highlight_row][highlight_col];
    tft.fillRect(highlight_col*cell_width, highlight_row*cell_height, cell_width, cell_height, get_color(cell_new));
    tft.drawRect(highlight_col*cell_width, highlight_row*cell_height, cell_width, cell_height, HIGHLIGHT_COLOR);
    tft.drawRect(highlight_col*cell_width+1, highlight_row*cell_height+1, cell_width-2, cell_height-2, HIGHLIGHT_COLOR);

    if (wave_started) {
        draw_balloons_on_map();
    }
}

#endif