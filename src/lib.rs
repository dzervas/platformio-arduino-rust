#![feature(lang_items)]
#![no_std]
#![allow(non_upper_case_globals)]
#![allow(non_snake_case)]
#![allow(non_camel_case_types)]

#[allow(dead_code)]
mod pio_rust;

extern crate pio_include;
use pio_include::pio_include;
pio_include!("Arduino.h");

// include!("platformio.rs");

#[no_mangle]
#[allow(dead_code)]
pub extern "C" fn setup() {
    unsafe {
        pinMode(19, 1);
    }
}

#[no_mangle]
#[allow(dead_code)]
pub extern "C" fn r#loop() {
    unsafe {
        digitalWrite(19, 1);
        delay(2000);
        digitalWrite(19, 0);
        delay(100);
    }
}

#[panic_handler]
fn my_panic(_info: &core::panic::PanicInfo) -> ! {
    loop {}
}

#[lang = "eh_personality"]
fn eh_personality() {}
