# I've unarchived the repo to enable the issues for further discussion :). The projects is still in a broken state and I don't see that changing 

# PlatformIO Arduino Rust bindings

This project serves as boilerplate for using the Arduino Framework
(this has nothing to do with the AVR based hardware, the IDE or the
company) with Rust.

It basically generates bindings of the Arduino library (or any other
platformIO library) in Rust code. Then the generated Rust object
is linked against those libraries using the `cargo_build.py`
script.

You can write regular Arduino code with `setup`, `loop`, `pinMode`
n' shit in Rust!

## Limitations

This is kinda a proof of concept so it has limitations.

First of all, I'm targeting the nrf52832 MCU. There's no
particular reason that I picked this MCU, other than:

1. Rust supports this architecture (Cortex-M4F) - even [Tier 2](https://forge.rust-lang.org/release/platform-support.html#tier-2) is good enough
2. PlatformIO supports this MCU (nrf52832)
3. I had a board lying around

Note that while Rust needs to support just the architecture to
generate a correct binary, PlatformIO is used as a HAL and needs
to know the specific MCU (memory map, memory regions, interrupts, etc.)

It's not that hard to target another MCU, changing the target in
`platformio.ini` and the header path on `cargo_build.py` should be enough.

Also I'm just generating bindings for `Arduino.h`. Also not hard to
change, just add the header on `cargo_build.py` `env.Execute` command.

Of course Rust is compiled with `no_std` - don't expect to build a
Rust binary for embedded target with `std` any time soon (if ever)...

## Usage

You will need to install:

- [rustup](https://rustup.rs/)
- [bindgen](https://github.com/rust-lang/rust-bindgen)
- [platformio](https://platformio.org/)

```shell
rustup target install thumbv7em-none-eabi
rustup toolchain install nightly  # Using features requires nightly
platformio run
```
