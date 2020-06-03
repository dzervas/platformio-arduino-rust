#![feature(start)]
#![no_std]
#![no_main]

#![allow(non_snake_case)]
#![allow(non_camel_case_types)]
#![allow(non_upper_case_globals)]

extern crate panic_halt;
#[allow(dead_code)]
mod pio_rust;

include!("platformio.rs");
// mod platformio;
// use crate::platformio::{pinMode, digitalWrite};

#[link(name = "FrameworkArduino")]
// extern {
//     fn digitalWrite(ulPin: u32, ulVal: u32);
//     fn pinMode(ulPin: u32, ulMode: u32);
// }

#[start]
#[no_mangle]
unsafe fn setup() {
    pinMode(0, 1);
    digitalWrite(0, 1);
}

#[allow(dead_code)]
#[no_mangle]
fn r#loop() {}
