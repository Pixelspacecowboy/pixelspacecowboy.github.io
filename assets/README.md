Final Project / Capstone Enhancement

🌡️ Smart Thermostat: A Journey in Embedded Systems & IoT

🔥 The Problem & The Solution

The challenge? Building an intelligent thermostat that efficiently manages heating and cooling while integrating real-time data monitoring, user interaction, fault tolerance, and future IoT capability.

The solution? A modular, state-driven thermostat system that:

🔢 Reads temperature and humidity in real time using the AHT20 sensor📊 Displays current state, temp, and humidity on a 16x2 LCD screen🔦 Controls heating & cooling using PWM LED indicators for feedback🔎 Allows users to toggle states and adjust set point with physical buttons📈 Logs data to CSV and serial UART for diagnostics and cloud expansion📁 Loads settings from a config.json and remembers set point across reboots🚨 Alerts users to sensor faults with clear LCD messaging

This system bridges software and hardware with a finite state machine (FSM) that drives the logic, making the entire system responsive, reliable, and ready for further automation.

🚀 Enhancements from CS-499 Capstone

Modularization & Architecture:

Split logic into thermostat_controller.py, utils.py, constants.py, setpoint_storage.py, and data_logger.py

Uses config.json for setting polling intervals, default set point, and LED modes

Persistence & Logging:

Saves set point to local file (setpoint.json) and reloads on reboot

Logs state, temperature, humidity to thermostat_log.csv

Error Handling & Fallbacks:

Displays “Sensor Error” on LCD when sensor data cannot be read

Uses -999.0 as a fallback and gracefully skips control logic if sensors fail

LCD Improvements:

Alternates between displaying time, temp, humidity, and state info

Testing Foundation:

Code now supports unit test scaffolding using mock GPIO/sensor interfaces (future-ready)

Documentation & Clarity:

Docstrings and comments added throughout for maintainability

Refined variable naming and structure

🎯 Skills Demonstrated

🛠️ Embedded Systems Development🌐 Config-driven Application Design🔁 Finite State Machine Implementation📋 CSV + Serial Logging for Diagnostics🚨 Error Handling & Resilience📁 Modular Software Architecture🔧 GPIO / I2C Sensor Integration📜 Python Code Documentation Best Practices

🌎 What's Next? (Future Enhancements)

🌫️ Humidity Control Expansion: Currently displayed and logged; will soon trigger alerts or automate fans/dehumidifiers

🌐 Web Dashboard (Flask): For viewing current temp/state and adjusting settings remotely

🗓 Schedule-Based Set Point: Load a daily heating/cooling schedule from JSON config

🌍 MQTT/HTTP Telemetry: Send data to cloud dashboard or integrate with smart home hubs

📊 Graph CSV Logs: Visualize trends with Plotly or Matplotlib to improve tuning

🚄 Dockerization & CI: Package project with mock testing to run in cloud/dev environment

🔍 Repository Contents

thermostat_controller.py

constants.py

utils.py

setpoint_storage.py

data_logger.py

config.json

thermostat_log.csv

README.md (this doc)

Flowchart.pdf

🎉 Final Thoughts

This thermostat is no longer a prototype—it’s a full-featured, extensible embedded platform. With strong error handling, modular code, and hardware abstraction, it stands as a polished artifact in both form and function.

“Do or do not. There is no try.” —Master Yoda 🚧🌌