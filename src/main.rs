#![no_std]
#![no_main]

#![allow(non_upper_case_globals)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]

include!(concat!(env!("OUT_DIR"), "/arduino.rs"));

// pick a panicking behavior
extern crate panic_halt; // you can put a breakpoint on `rust_begin_unwind` to catch panics
extern crate libc;
// extern crate panic_abort; // requires nightly
// extern crate panic_itm; // logs messages over ITM; requires ITM support
// extern crate panic_semihosting; // logs messages to the host stderr; requires a debugger

#[link(name = "FrameworkArduino")]
extern {
    fn digitalWrite(ulPin: u32, ulVal: u32);
    fn pinMode(ulPin: u32, ulMode: u32);
}

unsafe fn setup() {
    pinMode(0, 1);
    digitalWrite(0, 1);
}

fn r#loop() {}
