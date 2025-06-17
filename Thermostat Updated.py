# thermostat_controller.py
# Main script for the Raspberry Pi Thermostat Controller

# Import required libraries
import time
from datetime import datetime
from threading import Thread
from math import floor

import board
import adafruit_ahtx0
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from gpiozero import Button, PWMLED
import serial
from statemachine import StateMachine, State

from constants import *
from utils import set_led_state

class ManagedDisplay:
    """
    Manages a 16x2 LCD character display.
    """

    def __init__(self):
        # Initialize GPIO connections for LCD
        self.lcd_rs = digitalio.DigitalInOut(board.D17)
        self.lcd_en = digitalio.DigitalInOut(board.D27)
        self.lcd_d4 = digitalio.DigitalInOut(board.D5)
        self.lcd_d5 = digitalio.DigitalInOut(board.D6)
        self.lcd_d6 = digitalio.DigitalInOut(board.D13)
        self.lcd_d7 = digitalio.DigitalInOut(board.D26)

        # Initialize the display with configured dimensions
        self.lcd = characterlcd.Character_LCD_Mono(
            self.lcd_rs, self.lcd_en,
            self.lcd_d4, self.lcd_d5,
            self.lcd_d6, self.lcd_d7,
            LCD_COLUMNS, LCD_ROWS
        )
        self.lcd.clear()

    def update_screen(self, message):
        """
        Displays a message on the LCD.
        Clears any previous content.
        """
        self.lcd.clear()
        self.lcd.message = message

    def cleanup(self):
        """
        Clears and deinitializes the display.
        Should be called during shutdown.
        """
        self.lcd.clear()
        self.lcd_rs.deinit()
        self.lcd_en.deinit()
        self.lcd_d4.deinit()
        self.lcd_d5.deinit()
        self.lcd_d6.deinit()
        self.lcd_d7.deinit()

class TemperatureMachine(StateMachine):
    """
    Thermostat Finite State Machine using statemachine library.
    Handles Off, Heating, and Cooling states.
    """

    off = State(initial=True)
    heat = State()
    cool = State()
    cycle = (off.to(heat) | heat.to(cool) | cool.to(off))  # Cycle through states

    def __init__(self, screen, sensor, red_led, blue_led, serial_port):
        self.set_point = 72                     # Desired room temperature
        self.screen = screen                    # LCD display manager
        self.sensor = sensor                    # AHT20 temperature sensor
        self.red_led = red_led                  # Heating LED
        self.blue_led = blue_led                # Cooling LED
        self.serial = serial_port               # Serial port for logging
        self.end_display = False                # Used to cleanly stop the LCD thread
        super().__init__()
        self._start_display_thread()

    def _start_display_thread(self):
        """
        Starts a background thread to manage the display and serial logging.
        """
        Thread(target=self._manage_display, daemon=True).start()

    def _manage_display(self):
        """
        Background thread that handles:
        - Alternating LCD display messages
        - Logging temperature to serial port
        - Updating LEDs based on current state
        """
        counter = 1
        lcd_cycle = 1
        while not self.end_display:
            now = datetime.now().strftime('%b %d %H:%M:%S')
            temp = self.get_temp_f()

            # Alternate LCD lines every few seconds
            lcd_line = (
                f"Temp: {temp:.1f}°F" if lcd_cycle < 6
                else f"State: {self.current_state.id} | SP: {self.set_point}°F"
            )

            self.screen.update_screen(f"{now}\n{lcd_line}")

            # Log to serial periodically
            if counter % SERIAL_LOG_INTERVAL == 0:
                self._log_to_serial(temp)
                counter = 0

            counter += 1
            lcd_cycle = (lcd_cycle % 10) + 1
            self.update_leds(temp)

            time.sleep(TEMP_POLL_INTERVAL)

        # Cleanup when ending thread
        self.screen.cleanup()

    def _log_to_serial(self, temp):
        """
        Sends current system state and temperature to serial output.
        """
        try:
            output = f"{self.current_state.id},{temp:.1f},{self.set_point}"
            self.serial.write(output.encode("utf-8"))
        except Exception as e:
            if DEBUG:
                print(f"Serial write failed: {e}")

    def get_temp_f(self):
        """
        Converts temperature from Celsius to Fahrenheit.
        Returns fallback if sensor fails.
        """
        try:
            return (self.sensor.temperature * 9/5) + 32
        except Exception as e:
            if DEBUG:
                print(f"Sensor read failed: {e}")
            return -999.0  # Fallback temperature

    def update_leds(self, temp):
        """
        Updates the LED indicators based on state and temperature vs set point.
        """
        set_led_state(self.red_led, "off")
        set_led_state(self.blue_led, "off")

        if self.current_state == self.heat:
            set_led_state(self.red_led, "pulse" if temp < self.set_point else "on")
        elif self.current_state == self.cool:
            set_led_state(self.blue_led, "pulse" if temp > self.set_point else "on")

    def process_state_button(self):
        """
        Cycles to the next thermostat state (off -> heat -> cool -> off).
        """
        if DEBUG:
            print("Cycling temperature state")
        self.cycle()

    def process_temp_inc(self):
        """
        Increases the set point by 1°F.
        """
        self.set_point += 1
        if DEBUG:
            print(f"Set point increased to {self.set_point}")

    def process_temp_dec(self):
        """
        Decreases the set point by 1°F.
        """
        self.set_point -= 1
        if DEBUG:
            print(f"Set point decreased to {self.set_point}")

# === System Initialization ===

# Initialize sensor via I2C
i2c = board.I2C()
sensor = adafruit_ahtx0.AHTx0(i2c)

# Initialize display and LED hardware
screen = ManagedDisplay()
red_led = PWMLED(RED_LED_PIN)
blue_led = PWMLED(BLUE_LED_PIN)

# Initialize serial port for logging
serial_port = serial.Serial('/dev/ttyS0', 115200, timeout=1)

# Create state machine instance
thermostat = TemperatureMachine(screen, sensor, red_led, blue_led, serial_port)

# Assign button event handlers
Button(BUTTON_STATE_PIN).when_pressed = thermostat.process_state_button
Button(BUTTON_INC_PIN).when_pressed = thermostat.process_temp_inc
Button(BUTTON_DEC_PIN).when_pressed = thermostat.process_temp_dec

# Main loop — waits until user exits
try:
    while True:
        time.sleep(30)
except KeyboardInterrupt:
    thermostat.end_display = True
    print("Shutting down system gracefully...")
    time.sleep(1)
