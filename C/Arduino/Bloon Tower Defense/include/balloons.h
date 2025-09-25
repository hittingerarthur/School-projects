#ifndef BALLOONS_H
#define BALLOONS_H

#include <stdint.h>
#include <stdbool.h>
#include "menu.h" // Ensure this file declares wave_started, player_HP, current_state, etc.

// balloon type HP cost:
// Red = 1 HP, Blue = 2 HP, Green = 3 HP
#define BALLOON_RED   1
#define BALLOON_BLUE  2
#define BALLOON_GREEN 3

#define MAX_BALLOONS 20
#define FIRST_WAVE_BALLOONS 10
#define MAX_PATH_STEPS 27

extern void update_menu();
extern void draw_map();
extern void draw_balloons_on_map();
extern uint8_t map_matrix[8][8];

struct PathCoord {
    uint8_t row;
    uint8_t col;
};

static PathCoord path_steps[MAX_PATH_STEPS];

struct Balloon {
    bool active;
    uint8_t hp;          // Balloon "type" (HP cost)
    uint8_t path_index;  // Current step along the path
};

static Balloon balloons[MAX_BALLOONS];
static uint8_t spawn_count = 0; // Number of balloons spawned in current wave

static void init_path() {
    for (uint8_t num = 1; num <= 27; num++) {
        bool found = false;
        for (uint8_t r = 0; r < 8 && !found; r++) {
            for (uint8_t c = 0; c < 8 && !found; c++) {
                if (map_matrix[r][c] == num) {
                    path_steps[num - 1].row = r;
                    path_steps[num - 1].col = c;
                    found = true;
                }
            }
        }
    }
}

void init_balloons() {
    for (uint8_t i = 0; i < MAX_BALLOONS; i++) {
        balloons[i].active = false;
    }
    init_path();
    wave_started = false;
    spawn_count = 0;
    // player_HP now set in menu selection code (STATE_NEW_GAME_MENU)
}

void start_wave(uint8_t wave_number) {
    wave_started = true;
    spawn_count = 0; 
}

// Spawns a new balloon at the start of the path
static void spawn_balloon(uint8_t hp) {
    for (uint8_t i = 0; i < MAX_BALLOONS; i++) {
        if (!balloons[i].active) {
            balloons[i].active = true;
            balloons[i].hp = hp;
            balloons[i].path_index = 1; 
            return;
        }
    }
}

// Moves a balloon along the path
static void move_balloon(uint8_t i) {
    if (!balloons[i].active) return;

    balloons[i].path_index++;
    if (balloons[i].path_index > MAX_PATH_STEPS) {
        // Balloon reached the end of the path
        // Deduct balloon HP from player_HP
        if (player_HP > balloons[i].hp) {
            player_HP -= balloons[i].hp;
        } else {
            player_HP = 0;
        }

        balloons[i].active = false;
        update_menu(); // Refresh LCD to show new HP immediately
    }
}

void update_balloons() {
    // Move all active balloons
    for (uint8_t i = 0; i < MAX_BALLOONS; i++) {
        if (balloons[i].active) {
            move_balloon(i);
        }
    }

    // Spawn a new balloon if we haven't spawned them all yet
    if (wave_started && spawn_count < FIRST_WAVE_BALLOONS) {
        // For simplicity, always spawn red balloons. Adjust as needed.
        spawn_balloon(BALLOON_RED);
        spawn_count++;
    }

    // If player_HP is 0, you could handle game-over logic here if desired.
    // For now, just leave it as is.
}

void draw_balloons_on_map() {
    extern Adafruit_ST7735 tft;
    const int cell_width = 16;  
    const int cell_height = 16;

    for (uint8_t i = 0; i < MAX_BALLOONS; i++) {
        if (!balloons[i].active) continue;

        uint8_t path_idx = balloons[i].path_index;
        if (path_idx < 1 || path_idx > MAX_PATH_STEPS) continue;

        uint8_t r = path_steps[path_idx - 1].row;
        uint8_t c = path_steps[path_idx - 1].col;

        int x = c * cell_width;
        int y = r * cell_height;

        uint16_t color;
        if (balloons[i].hp == BALLOON_RED)   color = 0xF800; // Red
        else if (balloons[i].hp == BALLOON_BLUE)  color = 0x001F; // Blue
        else color = 0x07E0; // Green for BALLOON_GREEN

        int cx = x + cell_width/2;
        int cy = y + cell_height/2;
        tft.fillCircle(cx, cy, 5, color);
    }
}

#endif // BALLOONS_H
