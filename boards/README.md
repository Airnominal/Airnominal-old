# Airnominal Arduino Library

## About

We provide a library for Arduino-compatible microcontrollers that allows a wide range of supported measuring devices and sensors. It is designed to be lightweight and extensible, so it can run on many different platforms.

The library itself only handles packing data into server-compatible MsgPack format and does not enforce any specific sensors or transport protocols. However, we also provide [examples](examples) for commonly used sensors and transport using Wi-Fi. We encourage users to design their own measurement stations to fit their own needs, and contribute their code to our examples so others can benefit from it.

## Setup

After [registering the station](../README.md#registering-stations) on the website, you will need to obtain station's key and IDs. They need to be set inside `Config.h` file. This file also needs to contain Wi-Fi network information and station's location (if you are using a station/example without a GPS module).

You then need to select one of available examples and customize it if needed, or develop your own sketch for your sensors. You can then use the official Arduino IDE to upload the code to your board.

## Examples

### [ESP8266 with PMS5003](examples/pm)

| Measures     | Board   | Sensor | Communication Type | Supports GPS Module |
|--------------|---------|--------|--------------------|---------------------|
| PM particles | ESP8266 | PM5003 | Wi-Fi              | No                  |
