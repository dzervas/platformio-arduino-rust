#![no_std]

// Requires -x c++
mod platformio;

use platformio::Arduino_h::{pinMode, digitalWrite, delay, HIGH, LOW};

#[no_mangle]
pub extern "C" fn setup() {
    unsafe {
        pinMode(19, 1);
    }
}

#[no_mangle]
pub extern "C" fn r#loop() {
    unsafe {
        digitalWrite(19, HIGH as u8);
        delay(2000);
        digitalWrite(19, LOW as u8);
        delay(100);
    }
}

#[panic_handler]
fn my_panic(_info: &core::panic::PanicInfo) -> ! {
    loop {}
}
