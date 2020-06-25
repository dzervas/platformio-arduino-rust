// #![feature(start)]
#![feature(lang_items)]
#![no_std]
// #![no_main]
#![allow(non_snake_case)]
#![allow(non_camel_case_types)]
#![allow(non_upper_case_globals)]

// extern crate panic_halt;

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

// #[no_mangle]
// pub extern "C" fn _start() {
    // setup();
// }

#[no_mangle]
pub extern "C" fn setup() {
    unsafe {
        pinMode(19, 1);
    }
}

#[no_mangle]
pub extern "C" fn r#loop() {
    unsafe {
        digitalWrite(19, 1);
        delay(2000);
        digitalWrite(19, 0);
        delay(1000);
    }
}

// #[no_mangle]
// pub extern "C" fn main(_argc: isize, _argv: *const *const u8) -> isize {
    // setup();

    // loop {
        // r#loop();
    // }
// }

#[panic_handler]
fn my_panic(_info: &core::panic::PanicInfo) -> ! {
    loop {}
}

#[lang = "eh_personality"]
fn eh_personality() {}
