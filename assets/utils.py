# utils.py
# Contains reusable helper functions to reduce code duplication

from gpiozero import PWMLED

def set_led_state(led: PWMLED, mode: str):
    """
    Set the state of a PWM LED.

    Parameters:
    led (PWMLED): The LED to control
    mode (str): One of "on", "off", or "pulse"
    """
    if mode == "pulse":
        led.pulse()
    elif mode == "on":
        led.on()
    elif mode == "off":
        led.off()
    else:
        raise ValueError("Invalid LED mode. Use 'on', 'off', or 'pulse'.")
