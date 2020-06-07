// #![feature(start)]
#![no_std]
#![no_main]

#![allow(non_snake_case)]
#![allow(non_camel_case_types)]
#![allow(non_upper_case_globals)]

extern crate panic_halt;

#[allow(dead_code)]
mod pio_rust;

// #[link(name = "FrameworkArduino")]
include!("platformio.rs");
// mod platformio;
// use crate::platformio::{pinMode, digitalWrite};

// extern {
    // fn digitalWrite(ulPin: u32, ulVal: u32);
    // fn pinMode(ulPin: u32, ulMode: u32);
// }

#[no_mangle]
pub extern fn setup() {
    unsafe {
        pinMode(33, 1);
    }
}

#[no_mangle]
pub extern fn r#loop() {
    unsafe {
        digitalWrite(0, 1);
        delay(200);
        digitalWrite(0, 0);
        delay(100);
    }
}

// #[start]
// fn main(_argc: isize, _argv: *const *const u8) -> isize {
//     setup();

//     loop {
//         r#loop();
//     }
// }
