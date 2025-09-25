#ifndef MENU_H
#define MENU_H

#include <Arduino.h>
#include "LCD.h"
#include "ADC.h"
#include "melody.h"
#include "ageofwar.h"
#include "classic.h"
#include "pacman.h"

enum MenuState {
    STATE_MAIN_MENU,
    STATE_GOAT_SCREEN,
    STATE_NEW_GAME_MENU,
    STATE_HELP_MENU,
    STATE_LOAD_GAME_MENU,
    STATE_GAME_MAP,
    STATE_IN_GAME_HELP_MENU,
    STATE_TURRET_SELECTION
};

extern MenuState current_state;
extern bool music_on;
extern volatile const uint16_t* current_melody_frequencies;
extern volatile const uint16_t* current_melody_durations;
extern volatile uint16_t current_melody_size;
extern volatile uint16_t melody_index;
extern volatile uint16_t note_elapsed;
extern bool wave_started; 
extern uint8_t player_HP;

extern void start_wave(uint8_t wave_number);
extern void draw_map();
extern void draw_balloons_on_map();
extern void init_balloons();
extern void update_balloons();

extern uint8_t map_matrix[8][8];

#define GAME_MAP_ITEMS 5
#define ITEMS_PER_PAGE 2
#define JOY_CENTER 512
#define JOY_DEADZONE 200
#define DEBOUNCE_DELAY 200
#define LEFT_BUTTON_PIN PC3
#define RIGHT_BUTTON_PIN PC4

extern uint8_t highlighted_row;
extern uint8_t highlighted_col;
extern bool selection_on_tft;
extern uint8_t selected_row;
extern uint8_t selected_col;

extern uint8_t menu_index;
extern uint8_t last_joy_pos;
extern uint8_t current_page;

extern const char* main_menu_options[];
extern const char* new_game_menu_options[];
extern const char* load_game_menu_options[];
extern const char* in_game_help_options[];
extern const char* turret_options[];

MenuState current_state = STATE_MAIN_MENU;
bool music_on = true;
volatile const uint16_t* current_melody_frequencies = NULL;
volatile const uint16_t* current_melody_durations = NULL;
volatile uint16_t current_melody_size = 0;
volatile uint16_t melody_index = 0;
volatile uint16_t note_elapsed = 0;
bool wave_started = false;
// player_HP will now be set based on difficulty when a new game is started.

uint8_t menu_index = 0;
uint8_t last_joy_pos = 0;
uint8_t current_page = 0;
bool selection_on_tft = false;
uint8_t highlighted_row = 0;
uint8_t highlighted_col = 0;
uint8_t selected_row = 0;
uint8_t selected_col = 0;

const char* main_menu_options[] = {"New Game", "HELP", "Load Game", "GOAT"};
#define MAIN_MENU_SIZE 4
const char* new_game_menu_options[] = {"Baby", "Child", "Adult", "Senior", "Quit"};
#define NEW_GAME_MENU_SIZE 5
const char* load_game_menu_options[] = {"No game loaded yet", "Quit"};
#define LOAD_GAME_MENU_SIZE 2
const char* in_game_help_options[] = {"Music ON/OFF", "Quit"};
#define IN_GAME_HELP_MENU_SIZE 2
const char* turret_options[] = {"Purple", "Blue", "Orange", "Quit"};
#define TURRET_MENU_SIZE 4

void update_menu();
void handle_input();
void interact_with_cell(uint8_t row, uint8_t col);

void update_menu() {
    LCD_command(0x01);
    _delay_ms(2);
    switch (current_state) {
        case STATE_MAIN_MENU:
            for (uint8_t i = 0; i < 2; i++) {
                uint8_t idx = (menu_index + i) % MAIN_MENU_SIZE;
                LCD_set_cursor(i, 0);
                if (i == 0) LCD_data('>'); else LCD_data(' ');
                LCD_print(main_menu_options[idx]);
                LCD_print("        ");
            }
            break;
        case STATE_GOAT_SCREEN:
            LCD_set_cursor(0, 0);
            LCD_print("Best score:XXXXX");
            LCD_set_cursor(1, 0);
            LCD_print((menu_index == 0) ? ">Quit" : " Quit");
            break;
        case STATE_NEW_GAME_MENU:
            for (uint8_t i = 0; i < 2; i++) {
                uint8_t idx = (menu_index + i) % NEW_GAME_MENU_SIZE;
                LCD_set_cursor(i, 0);
                if (i == 0) LCD_data('>'); else LCD_data(' ');
                LCD_print(new_game_menu_options[idx]);
                LCD_print("        ");
            }
            break;
        case STATE_HELP_MENU:
            LCD_set_cursor(0, 0);
            if (music_on) {
                LCD_print((menu_index == 0) ? ">Music ON" : " Music ON");
            } else {
                LCD_print((menu_index == 0) ? ">Music OFF" : " Music OFF");
            }
            LCD_print("       ");
            LCD_set_cursor(1, 0);
            LCD_print((menu_index == 1) ? ">Quit" : " Quit");
            break;
        case STATE_LOAD_GAME_MENU:
            for (uint8_t i = 0; i < 2; i++) {
                uint8_t idx = (menu_index + i) % LOAD_GAME_MENU_SIZE;
                LCD_set_cursor(i, 0);
                if (i == 0) LCD_data('>'); else LCD_data(' ');
                LCD_print(load_game_menu_options[idx]);
                LCD_print("        ");
            }
            break;
        case STATE_GAME_MAP: {
            LCD_command(0x01);
            _delay_ms(2);
            if (menu_index < 2) current_page = 0;
            else if (menu_index < 4) current_page = 1;
            else current_page = 2;

            if (current_page == 0) {
                // Display Money (not yet implemented fully) and HP
                if (menu_index == 0 && !selection_on_tft) {
                    LCD_print(">$$: 0");
                } else {
                    LCD_print(" $$: 0");
                }
                LCD_set_cursor(1, 0);
                char hpStr[10];
                snprintf(hpStr, 10, "%d", player_HP);
                if (menu_index == 1 && !selection_on_tft) {
                    LCD_print(">HP:");
                    LCD_print(hpStr);
                } else {
                    LCD_print(" HP:");
                    LCD_print(hpStr);
                }
            } else if (current_page == 1) {
                if (menu_index == 2 && !selection_on_tft) {
                    LCD_print(">HELP");
                } else {
                    LCD_print(" HELP");
                }
                LCD_set_cursor(1, 0);
                if (menu_index == 3 && !selection_on_tft) {
                    LCD_print(">Score:0");
                } else {
                    LCD_print(" Score:0");
                }
            } else {
                if (menu_index == 4 && !selection_on_tft) {
                    LCD_print(">Start wave");
                } else {
                    LCD_print(" Start wave");
                }
                LCD_set_cursor(1, 0);
                LCD_print("           ");
            }
            break;
        }
        case STATE_IN_GAME_HELP_MENU:
            LCD_set_cursor(0, 0);
            if (music_on) {
                LCD_print((menu_index == 0) ? ">Music ON" : " Music ON");
            } else {
                LCD_print((menu_index == 0) ? ">Music OFF" : " Music OFF");
            }
            LCD_print("       ");
            LCD_set_cursor(1, 0);
            LCD_print((menu_index == 1) ? ">Quit" : " Quit");
            break;
        case STATE_TURRET_SELECTION:
            for (uint8_t i = 0; i < 2; i++) {
                uint8_t idx = (menu_index + i) % TURRET_MENU_SIZE;
                LCD_set_cursor(i, 0);
                if (i == 0) LCD_data('>'); else LCD_data(' ');
                LCD_print(turret_options[idx]);
                LCD_print("       ");
            }
            break;
        default:
            break;
    }
}

void interact_with_cell(uint8_t row, uint8_t col) {
    uint8_t val = map_matrix[row][col];
    if ((val >= 1 && val <= 27)) {
        return;
    } else if (val == 0) {
        selected_row = row;
        selected_col = col;
        current_state = STATE_TURRET_SELECTION;
        menu_index = 0;
        selection_on_tft = false;
        update_menu();
    } else if (val >= 100 && val <=102) {
        return;
    } else {
        return;
    }
}

void handle_input() {
    uint16_t joy_y = ADC_read(0); 
    uint16_t joy_x = ADC_read(1); 
    uint8_t select_pressed = !(PINC & (1 << PC2));
    uint8_t left_button_pressed = !(PINC & (1 << PC3));
    uint8_t right_button_pressed = !(PINC & (1 << PC4));

    static uint8_t left_button_last_state = 0;
    static uint8_t right_button_last_state = 0;
    static uint8_t select_last_state = 0;

    if (left_button_pressed && !left_button_last_state) {
        current_state = STATE_MAIN_MENU;
        menu_index = 0;
        selection_on_tft = false;
        wave_started = false;
        // player_HP reset to some default if needed, but will be set after difficulty is chosen.
        update_menu();
        if (music_on) {
            current_melody_frequencies = melody_frequencies_melody;
            current_melody_durations = melody_durations_melody;
            current_melody_size = MELODY_SIZE_MELODY;
            melody_index = 0;
            note_elapsed = 0;
        }
        left_button_last_state = 1;
    } else if (!left_button_pressed) {
        left_button_last_state = 0;
    }

    if (right_button_pressed && !right_button_last_state && current_state == STATE_GAME_MAP) {
        selection_on_tft = !selection_on_tft;
        extern void draw_map_with_highlight(uint8_t,uint8_t,uint8_t,uint8_t);
        if (selection_on_tft) {
            highlighted_row = 0; 
            highlighted_col = 0;
            draw_map_with_highlight(highlighted_row, highlighted_col, highlighted_row, highlighted_col);
        } else {
            draw_map();
            draw_balloons_on_map(); 
        }
        update_menu();
        right_button_last_state = 1;
    } else if (!right_button_pressed) {
        right_button_last_state = 0;
    }

    if (selection_on_tft && current_state == STATE_GAME_MAP) {
        // Navigation on the TFT
        static uint8_t prev_highlighted_row = 0;
        static uint8_t prev_highlighted_col = 0;
        extern void draw_map_with_highlight(uint8_t,uint8_t,uint8_t,uint8_t);

        if (joy_y < (JOY_CENTER - JOY_DEADZONE) && last_joy_pos != 1) {
            if (highlighted_row > 0) {
                prev_highlighted_row = highlighted_row;
                prev_highlighted_col = highlighted_col;
                highlighted_row--;
                draw_map_with_highlight(prev_highlighted_row, prev_highlighted_col, highlighted_row, highlighted_col);
                draw_balloons_on_map();
            }
            last_joy_pos = 1;
        } else if (joy_y > (JOY_CENTER + JOY_DEADZONE) && last_joy_pos != 2) {
            if (highlighted_row < 7) {
                prev_highlighted_row = highlighted_row;
                prev_highlighted_col = highlighted_col;
                highlighted_row++;
                draw_map_with_highlight(prev_highlighted_row, prev_highlighted_col, highlighted_row, highlighted_col);
                draw_balloons_on_map();
            }
            last_joy_pos = 2;
        } else if (joy_x < (JOY_CENTER - JOY_DEADZONE) && last_joy_pos != 3) {
            if (highlighted_col > 0) {
                prev_highlighted_row = highlighted_row;
                prev_highlighted_col = highlighted_col;
                highlighted_col--;
                draw_map_with_highlight(prev_highlighted_row, prev_highlighted_col, highlighted_row, highlighted_col);
                draw_balloons_on_map();
            }
            last_joy_pos = 3;
        } else if (joy_x > (JOY_CENTER + JOY_DEADZONE) && last_joy_pos != 4) {
            if (highlighted_col < 7) {
                prev_highlighted_row = highlighted_row;
                prev_highlighted_col = highlighted_col;
                highlighted_col++;
                draw_map_with_highlight(prev_highlighted_row, prev_highlighted_col, highlighted_row, highlighted_col);
                draw_balloons_on_map();
            }
            last_joy_pos = 4;
        } else if (abs((int)joy_x - JOY_CENTER) <= JOY_DEADZONE && abs((int)joy_y - JOY_CENTER) <= JOY_DEADZONE) {
            last_joy_pos = 0;
        }

        if (select_pressed && !select_last_state) {
            interact_with_cell(highlighted_row, highlighted_col);
            select_last_state = 1;
        } else if (!select_pressed) {
            select_last_state = 0;
        }

    } else {
        switch (current_state) {
            case STATE_MAIN_MENU:
                if (joy_y < (JOY_CENTER - JOY_DEADZONE) && last_joy_pos != 1) {
                    if (menu_index == 0) menu_index = MAIN_MENU_SIZE - 1;
                    else menu_index--;
                    update_menu();
                    last_joy_pos = 1;
                } else if (joy_y > (JOY_CENTER + JOY_DEADZONE) && last_joy_pos != 2) {
                    menu_index = (menu_index + 1) % MAIN_MENU_SIZE;
                    update_menu();
                    last_joy_pos = 2;
                } else if (abs((int)joy_y - JOY_CENTER) <= JOY_DEADZONE) {
                    last_joy_pos = 0;
                }
                if (select_pressed && !select_last_state) {
                    const char* selected_option = main_menu_options[menu_index];
                    if (strcmp(selected_option, "GOAT") == 0) {
                        current_state = STATE_GOAT_SCREEN;
                        menu_index = 0;
                        update_menu();
                        if (music_on) {
                            current_melody_frequencies = melody_frequencies_pacman;
                            current_melody_durations = melody_durations_pacman;
                            current_melody_size = MELODY_SIZE_PACMAN;
                            melody_index = 0;
                            note_elapsed = 0;
                        }
                    } else if (strcmp(selected_option, "New Game") == 0) {
                        current_state = STATE_NEW_GAME_MENU;
                        menu_index = 0;
                        update_menu();
                        if (music_on) {
                            current_melody_frequencies = melody_frequencies_melody;
                            current_melody_durations = melody_durations_melody;
                            current_melody_size = MELODY_SIZE_MELODY;
                            melody_index = 0;
                            note_elapsed = 0;
                        }
                    } else if (strcmp(selected_option, "HELP") == 0) {
                        current_state = STATE_HELP_MENU;
                        menu_index = 0;
                        update_menu();
                        if (music_on) {
                            current_melody_frequencies = melody_frequencies_classic;
                            current_melody_durations = melody_durations_classic;
                            current_melody_size = MELODY_SIZE_CLASSIC;
                            melody_index = 0;
                            note_elapsed = 0;
                        }
                    } else if (strcmp(selected_option, "Load Game") == 0) {
                        current_state = STATE_LOAD_GAME_MENU;
                        menu_index = 0;
                        update_menu();
                        if (music_on) {
                            current_melody_frequencies = melody_frequencies_ageofwar;
                            current_melody_durations = melody_durations_ageofwar;
                            current_melody_size = MELODY_SIZE_AGEOFWAR;
                            melody_index = 0;
                            note_elapsed = 0;
                        }
                    }
                    select_last_state = 1;
                } else if (!select_pressed) {
                    select_last_state = 0;
                }
                break;
            case STATE_GOAT_SCREEN:
                if (select_pressed && !select_last_state) {
                    if (menu_index == 0) {
                        current_state = STATE_MAIN_MENU;
                        menu_index = 0;
                        update_menu();
                        if (music_on) {
                            current_melody_frequencies = melody_frequencies_melody;
                            current_melody_durations = melody_durations_melody;
                            current_melody_size = MELODY_SIZE_MELODY;
                            melody_index = 0;
                            note_elapsed = 0;
                        }
                    }
                    select_last_state = 1;
                } else if (!select_pressed) {
                    select_last_state = 0;
                }
                break;
            case STATE_HELP_MENU:
                if (joy_y < (JOY_CENTER - JOY_DEADZONE) && last_joy_pos != 1) {
                    if (menu_index == 0) menu_index = 1;
                    else menu_index--;
                    update_menu();
                    last_joy_pos = 1;
                } else if (joy_y > (JOY_CENTER + JOY_DEADZONE) && last_joy_pos != 2) {
                    menu_index = (menu_index + 1) % 2;
                    update_menu();
                    last_joy_pos = 2;
                } else if (abs((int)joy_y - JOY_CENTER) <= JOY_DEADZONE) {
                    last_joy_pos = 0;
                }

                if (select_pressed && !select_last_state) {
                    if (menu_index == 0) {
                        music_on = !music_on;
                        update_menu();
                        if (!music_on) {
                            TCCR1B &= ~((1 << CS11) | (1 << CS10));
                        } else {
                            melody_index = 0;
                            note_elapsed = 0;
                        }
                    } else if (menu_index == 1) {
                        current_state = STATE_MAIN_MENU;
                        menu_index = 0;
                        update_menu();
                        if (music_on) {
                            current_melody_frequencies = melody_frequencies_melody;
                            current_melody_durations = melody_durations_melody;
                            current_melody_size = MELODY_SIZE_MELODY;
                            melody_index = 0;
                            note_elapsed = 0;
                        }
                    }
                    select_last_state = 1;
                } else if (!select_pressed) {
                    select_last_state = 0;
                }
                break;
            case STATE_NEW_GAME_MENU:
                if (joy_y < (JOY_CENTER - JOY_DEADZONE) && last_joy_pos != 1) {
                    if (menu_index == 0) menu_index = NEW_GAME_MENU_SIZE - 1;
                    else menu_index--;
                    update_menu();
                    last_joy_pos = 1;
                } else if (joy_y > (JOY_CENTER + JOY_DEADZONE) && last_joy_pos != 2) {
                    menu_index = (menu_index + 1) % NEW_GAME_MENU_SIZE;
                    update_menu();
                    last_joy_pos = 2;
                } else if (abs((int)joy_y - JOY_CENTER) <= JOY_DEADZONE) {
                    last_joy_pos = 0;
                }

                if (select_pressed && !select_last_state) {
                    const char* selected_option = new_game_menu_options[menu_index];
                    if (strcmp(selected_option, "Quit") == 0) {
                        current_state = STATE_MAIN_MENU;
                        menu_index = 0;
                        update_menu();
                        if (music_on) {
                            current_melody_frequencies = melody_frequencies_melody;
                            current_melody_durations = melody_durations_melody;
                            current_melody_size = MELODY_SIZE_MELODY;
                            melody_index = 0;
                            note_elapsed = 0;
                        }

                    } else {
                        // Set player_HP based on difficulty
                        if (strcmp(selected_option, "Baby") == 0) {
                            player_HP = 20;
                        } else if (strcmp(selected_option, "Child") == 0) {
                            player_HP = 15;
                        } else if (strcmp(selected_option, "Adult") == 0) {
                            player_HP = 10;
                        } else if (strcmp(selected_option, "Senior") == 0) {
                            player_HP = 5;
                        }

                        current_state = STATE_GAME_MAP;
                        menu_index = 0;
                        current_page = 0;
                        selection_on_tft = false;
                        wave_started = false;
                        update_menu();
                        draw_map();
                        if (music_on) {
                            current_melody_frequencies = melody_frequencies_melody;
                            current_melody_durations = melody_durations_melody;
                            current_melody_size = MELODY_SIZE_MELODY;
                            melody_index = 0;
                            note_elapsed = 0;
                        }
                    }
                    select_last_state = 1;
                } else if (!select_pressed) {
                    select_last_state = 0;
                }
                break;
            case STATE_LOAD_GAME_MENU:
                if (joy_y < (JOY_CENTER - JOY_DEADZONE) && last_joy_pos != 1) {
                    if (menu_index == 0) menu_index = LOAD_GAME_MENU_SIZE - 1;
                    else menu_index--;
                    update_menu();
                    last_joy_pos = 1;
                } else if (joy_y > (JOY_CENTER + JOY_DEADZONE) && last_joy_pos != 2) {
                    menu_index = (menu_index + 1) % LOAD_GAME_MENU_SIZE;
                    update_menu();
                    last_joy_pos = 2;
                } else if (abs((int)joy_y - JOY_CENTER) <= JOY_DEADZONE) {
                    last_joy_pos = 0;
                }

                if (select_pressed && !select_last_state) {
                    const char* selected_option = load_game_menu_options[menu_index];
                    if (strcmp(selected_option, "Quit") == 0) {
                        current_state = STATE_MAIN_MENU;
                        menu_index = 0;
                        update_menu();
                        if (music_on) {
                            current_melody_frequencies = melody_frequencies_melody;
                            current_melody_durations = melody_durations_melody;
                            current_melody_size = MELODY_SIZE_MELODY;
                            melody_index = 0;
                            note_elapsed = 0;
                        }
                    }
                    select_last_state = 1;
                } else if (!select_pressed) {
                    select_last_state = 0;
                }
                break;
            case STATE_GAME_MAP:
                if (!selection_on_tft) {
                    if (joy_y < (JOY_CENTER - JOY_DEADZONE) && last_joy_pos != 1) {
                        if (menu_index == 0) {
                            menu_index = GAME_MAP_ITEMS - 1; 
                        } else {
                            menu_index--;
                        }
                        update_menu();
                        last_joy_pos = 1;
                    } else if (joy_y > (JOY_CENTER + JOY_DEADZONE) && last_joy_pos != 2) {
                        if (menu_index == GAME_MAP_ITEMS - 1) {
                            menu_index = 0;
                        } else {
                            menu_index++;
                        }
                        update_menu();
                        last_joy_pos = 2;
                    } else if (abs((int)joy_y - JOY_CENTER) <= JOY_DEADZONE) {
                        last_joy_pos = 0;
                    }

                    if (select_pressed && !select_last_state) {
                        if (menu_index == 2) {
                            current_state = STATE_IN_GAME_HELP_MENU;
                            menu_index = 0;
                            update_menu();
                        } else if (menu_index == 4) {
                            if (!wave_started) {
                                start_wave(1); 
                                LCD_command(0x01); _delay_ms(2);
                                LCD_set_cursor(0,0);
                                LCD_print("Wave started!");
                                LCD_set_cursor(1,0);
                                LCD_print("Balloon in 1s");
                            }
                        }
                        select_last_state = 1;
                    } else if (!select_pressed) {
                        select_last_state = 0;
                    }
                }
                break;
            case STATE_IN_GAME_HELP_MENU:
                if (joy_y < (JOY_CENTER - JOY_DEADZONE) && last_joy_pos != 1) {
                    if (menu_index == 0) menu_index = 1;
                    else menu_index--;
                    update_menu();
                    last_joy_pos = 1;
                } else if (joy_y > (JOY_CENTER + JOY_DEADZONE) && last_joy_pos != 2) {
                    menu_index = (menu_index + 1) % 2;
                    update_menu();
                    last_joy_pos = 2;
                } else if (abs((int)joy_y - JOY_CENTER) <= JOY_DEADZONE) {
                    last_joy_pos = 0;
                }

                if (select_pressed && !select_last_state) {
                    if (menu_index == 0) {
                        music_on = !music_on;
                        update_menu();
                        if (!music_on) {
                            TCCR1B &= ~((1 << CS11) | (1 << CS10));
                        } else {
                            melody_index = 0;
                            note_elapsed = 0;
                        }
                    } else if (menu_index == 1) {
                        current_state = STATE_GAME_MAP;
                        menu_index = 2; 
                        update_menu();
                    }
                    select_last_state = 1;
                } else if (!select_pressed) {
                    select_last_state = 0;
                }
                break;
            case STATE_TURRET_SELECTION:
                if (joy_y < (JOY_CENTER - JOY_DEADZONE) && last_joy_pos != 1) {
                    if (menu_index == 0) menu_index = TURRET_MENU_SIZE - 1;
                    else menu_index--;
                    update_menu();
                    last_joy_pos = 1;
                } else if (joy_y > (JOY_CENTER + JOY_DEADZONE) && last_joy_pos != 2) {
                    menu_index = (menu_index + 1) % TURRET_MENU_SIZE;
                    update_menu();
                    last_joy_pos = 2;
                } else if (abs((int)joy_y - JOY_CENTER) <= JOY_DEADZONE) {
                    last_joy_pos = 0;
                }

                if (select_pressed && !select_last_state) {
                    const char* selected_option = turret_options[menu_index];
                    uint8_t turret_type = 0;
                    if (strcmp(selected_option, "Quit") == 0) {
                        current_state = STATE_GAME_MAP;
                        menu_index = 0;
                        selection_on_tft = false;
                        update_menu();
                    } else {
                        if (strcmp(selected_option, "Purple") == 0) {
                            turret_type = 100; 
                        } else if (strcmp(selected_option, "Blue") == 0) {
                            turret_type = 101;
                        } else if (strcmp(selected_option, "Orange") ==0){
                            turret_type = 102;
                        }
                        map_matrix[selected_row][selected_col] = turret_type;
                        extern void draw_map_with_highlight(uint8_t,uint8_t,uint8_t,uint8_t);
                        draw_map_with_highlight(selected_row, selected_col, highlighted_row, highlighted_col);
                        draw_balloons_on_map();
                        current_state = STATE_GAME_MAP;
                        menu_index = 0;
                        selection_on_tft = false;
                        update_menu();
                    }
                    select_last_state = 1;
                } else if (!select_pressed) {
                    select_last_state = 0;
                }
                break;
            default:
                break;
        }
    }
}

#endif


