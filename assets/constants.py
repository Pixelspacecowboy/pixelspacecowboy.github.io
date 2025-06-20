# constants.py
# Contains named constants for GPIO pin mappings and system configuration

# Button GPIO pin assignments
BUTTON_STATE_PIN = 24     # Button to cycle thermostat state
BUTTON_INC_PIN = 25       # Button to increase set point
BUTTON_DEC_PIN = 12       # Button to decrease set point

# LED GPIO pin assignments
RED_LED_PIN = 18          # Red LED for Heating state
BLUE_LED_PIN = 23         # Blue LED for Cooling state

# LCD GPIO pin mappings
LCD_RS = 17
LCD_EN = 27
LCD_D4 = 5
LCD_D5 = 6
LCD_D6 = 13
LCD_D7 = 26

# LCD display size
LCD_COLUMNS = 16
LCD_ROWS = 2

# Polling intervals
TEMP_POLL_INTERVAL = 1        # Time (in seconds) between temperature updates
SERIAL_LOG_INTERVAL = 30      # Time (in seconds) between serial log updates

# Debug mode toggle
DEBUG = True
# constants.py
# Contains named constants for GPIO pin mappings and system configuration

# Button GPIO pin assignments
BUTTON_STATE_PIN = 24     # Button to cycle thermostat state
BUTTON_INC_PIN = 25       # Button to increase set point
BUTTON_DEC_PIN = 12       # Button to decrease set point

# LED GPIO pin assignments
RED_LED_PIN = 18          # Red LED for Heating state
BLUE_LED_PIN = 23         # Blue LED for Cooling state

# LCD GPIO pin mappings
LCD_RS = 17
LCD_EN = 27
LCD_D4 = 5
LCD_D5 = 6
LCD_D6 = 13
LCD_D7 = 26

# LCD display size
LCD_COLUMNS = 16
LCD_ROWS = 2

# Polling intervals
TEMP_POLL_INTERVAL = 1        # Time (in seconds) between temperature updates
SERIAL_LOG_INTERVAL = 30      # Time (in seconds) between serial log updates

# Debug mode toggle
DEBUG = True
