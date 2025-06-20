# thermostat_controller.py
# Smart Thermostat Controller using Raspberry Pi GPIO, LCD, and AHT20 Sensor
# Enhanced with config loading, persistent storage, CSV logging, and robust error handling

# === Imports ===
import time
import json
from datetime import datetime
from threading import Thread
from math import floor

# Hardware libraries
import board
import adafruit_ahtx0
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from gpiozero import Button, PWMLED
import serial
from statemachine import StateMachine, State

# Project modules
from constants import *
from utils import set_led_state
from setpoint_storage import save_setpoint, load_setpoint
from data_logger import log_temperature

# === Load Config ===
# Load parameters from JSON config file (e.g., polling interval, default set point)
with open("config.json") as f:
    config = json.load(f)

DEFAULT_SETPOINT = config.get("default_set_point", 72)
TEMP_POLL_INTERVAL = config.get("temp_poll_interval", 1)
SERIAL_LOG_INTERVAL = config.get("serial_log_interval", 30)

# === LCD Display Handler ===
class ManagedDisplay:
    """
    Manages the 16x2 character LCD using GPIO.
    """

    def __init__(self):
        # Initialize LCD pin mapping
        self.lcd_rs = digitalio.DigitalInOut(board.D17)
        self.lcd_en = digitalio.DigitalInOut(board.D27)
        self.lcd_d4 = digitalio.DigitalInOut(board.D5)
        self.lcd_d5 = digitalio.DigitalInOut(board.D6)
        self.lcd_d6 = digitalio.DigitalInOut(board.D13)
        self.lcd_d7 = digitalio.DigitalInOut(board.D26)

        # Set display size and initialize
        self.lcd = characterlcd.Character_LCD_Mono(
            self.lcd_rs, self.lcd_en,
            self.lcd_d4, self.lcd_d5,
            self.lcd_d6, self.lcd_d7,
            LCD_COLUMNS, LCD_ROWS
        )
        self.lcd.clear()

    def update_screen(self, message):
        """
        Display a message on the LCD (overwrites both rows).
        """
        self.lcd.clear()
        self.lcd.message = message

    def cleanup(self):
        """
        Safely deinitialize all LCD resources.
        """
        self.lcd.clear()
        self.lcd_rs.deinit()
        self.lcd_en.deinit()
        self.lcd_d4.deinit()
        self.lcd_d5.deinit()
        self.lcd_d6.deinit()
        self.lcd_d7.deinit()

# === Thermostat FSM ===
class TemperatureMachine(StateMachine):
    """
    Thermostat logic built with a Finite State Machine.
    States: off → heat → cool → off
    """

    # Define states
    off = State(initial=True)
    heat = State()
    cool = State()
    cycle = (off.to(heat) | heat.to(cool) | cool.to(off))

    def __init__(self, screen, sensor, red_led, blue_led, serial_port):
        self.set_point = load_setpoint(DEFAULT_SETPOINT)  # Load saved or default set point
        self.screen = screen
        self.sensor = sensor
        self.red_led = red_led
        self.blue_led = blue_led
        self.serial = serial_port
        self.end_display = False  # Controls thread shutdown
        super().__init__()
        self._start_display_thread()

    def _start_display_thread(self):
        """
        Launch background thread to update display and perform logging.
        """
        Thread(target=self._manage_display, daemon=True).start()

    def _manage_display(self):
        """
        Periodically update the LCD, log to CSV/serial, and control LEDs.
        """
        counter = 1
        lcd_cycle = 1

        while not self.end_display:
            now = datetime.now().strftime('%b %d %H:%M:%S')
            temp = self.get_temp_f()

            # Alternate between temp and state display
            if temp == -999.0:
                line = "Sensor Error\nCheck Wiring"
            elif lcd_cycle < 6:
                line = f"{now}\nTemp: {temp:.1f}°F"
            else:
                line = f"{now}\nState:{self.current_state.id} | SP:{self.set_point}°F"

            self.screen.update_screen(line)

            # Log only valid readings
            if temp != -999.0:
                log_temperature(self.current_state.id, temp, self.set_point)
                if counter % SERIAL_LOG_INTERVAL == 0:
                    self._log_to_serial(temp)
                    counter = 0

            counter += 1
            lcd_cycle = (lcd_cycle % 10) + 1
            self.update_leds(temp)

            time.sleep(TEMP_POLL_INTERVAL)

        # Cleanup when exiting
        self.screen.cleanup()

    def _log_to_serial(self, temp):
        """
        Sends thermostat state data to UART.
        """
        try:
            output = f"{self.current_state.id},{temp:.1f},{self.set_point}"
            self.serial.write(output.encode("utf-8"))
        except Exception as e:
            if DEBUG:
                print(f"Serial write failed: {e}")

    def get_temp_f(self):
        """
        Read and convert Celsius to Fahrenheit.
        Returns fallback value on error.
        """
        try:
            return (self.sensor.temperature * 9 / 5) + 32
        except Exception as e:
            if DEBUG:
                print(f"Sensor read failed: {e}")
            return -999.0

    def update_leds(self, temp):
        """
        Turn LEDs on/off/pulse based on state and temp.
        """
        set_led_state(self.red_led, "off")
        set_led_state(self.blue_led, "off")
        if temp == -999.0:
            return  # Skip LED logic if reading failed

        if self.current_state == self.heat:
            set_led_state(self.red_led, "pulse" if temp < self.set_point else "on")
        elif self.current_state == self.cool:
            set_led_state(self.blue_led, "pulse" if temp > self.set_point else "on")

    def process_state_button(self):
        """
        Handle physical button: cycle thermostat state.
        """
        if DEBUG:
            print("Cycling temperature state")
        self.cycle()

    def process_temp_inc(self):
        """
        Increase set point and save.
        """
        self.set_point += 1
        save_setpoint(self.set_point)
        if DEBUG:
            print(f"Set point increased to {self.set_point}")

    def process_temp_dec(self):
        """
        Decrease set point and save.
        """
        self.set_point -= 1
        save_setpoint(self.set_point)
        if DEBUG:
            print(f"Set point decreased to {self.set_point}")

# === System Initialization ===

# Setup I2C and hardware
i2c = board.I2C()
sensor = adafruit_ahtx0.AHTx0(i2c)
screen = ManagedDisplay()
red_led = PWMLED(RED_LED_PIN)
blue_led = PWMLED(BLUE_LED_PIN)
serial_port = serial.Serial('/dev/ttyS0', 115200, timeout=1)

# Create the thermostat FSM object
thermostat = TemperatureMachine(screen, sensor, red_led, blue_led, serial_port)

# Assign GPIO button callbacks
Button(BUTTON_STATE_PIN).when_pressed = thermostat.process_state_button
Button(BUTTON_INC_PIN).when_pressed = thermostat.process_temp_inc
Button(BUTTON_DEC_PIN).when_pressed = thermostat.process_temp_dec

# Keep the program running until interrupted
try:
    while True:
        time.sleep(30)
except KeyboardInterrupt:
    thermostat.end_display = True
    save_setpoint(thermostat.set_point)
    print("Shutting down system gracefully...")
    time.sleep(1)
