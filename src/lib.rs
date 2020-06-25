#![feature(lang_items)]
#![no_std]
#![allow(dead_code)]
#![allow(non_snake_case)]
#![allow(non_camel_case_types)]
#![allow(non_upper_case_globals)]

mod pio_rust;

include!("platformio.rs");

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

#[panic_handler]
fn my_panic(_info: &core::panic::PanicInfo) -> ! {
    loop {}
}

#[lang = "eh_personality"]
fn eh_personality() {}
