# Architecture

## System Overview

The 4CSCC IoT system is meant to provide a low-cost, reliable, and easy to setup and use, integrated physical computing platform for the automated collection of data in academic and educational settings. To date, the system has been mainly built around various Raspberry Pi devices, namely the Single-Board Computers(SBCs) such as the Raspberry Pi 3B+ and 4 used as a network hosting, data logging, brokering device and the Raspberry Pi Pico W microcontroller as an inexpensive, low power device to run various sensors from. This repository(`sensor-hub`), is used to setup/configure the SBC devices. It performs upgrades, installs necessary dependencies, ensures that automatic time setting is on, installs and sets up as services that run automaticall on boot for MQTT brokerage, database setup, datalogging, as well as hosting a server to display recorded data. In the future, a command line utility for setting up sensor devices is planned.

Briefly, the setup/configuration flow goes something like:

    - Flash microSD card with Raspberry Pi OS. A public SSH key is also added at this time, to allow access to run the setup scripts found here.
    - Ensure the Pi OS is up to date.
    - Install necessary basal dependencies, such as a recent Python version on the Pi using the OS package management.
    - Create a standard hosted network for sensor devices to connect to.
    - Create and configure necessary filepath locations for the various components.
    - Install, create, and initilize a SQLite database for storing sensor data to.
    - Install and run an [MQTT broker](https://mosquitto.org/), so that data can be passed around on the hosted network and to the hosted logger.
    - Install and run a [data-logger](https://github.com/4cscc/mqtt-data-logger/tree/main), which is an MQTT client that provides the write access to the database, as well timestamping and providing some basic data processing(such as binning wind data into cardinal-directions).
    - Installing a server to provide a dashboard of all of the data being recorded by the Raspberry Pi.
