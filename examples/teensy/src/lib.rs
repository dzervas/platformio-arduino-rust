#![no_std]

mod platformio;

use platformio::Arduino_h::{pinMode, digitalWrite, delay, LED_BUILTIN, HIGH, LOW, OUTPUT};

#[no_mangle]
pub extern "C" fn setup() {
    unsafe {
        pinMode(LED_BUILTIN as u8, OUTPUT as u8);
    }
}

#[no_mangle]
pub extern "C" fn r#loop() {
    unsafe {
        digitalWrite(LED_BUILTIN as u8, HIGH as u8);
        delay(2000);
        digitalWrite(LED_BUILTIN as u8, LOW as u8);
        delay(100);
    }
}

#[panic_handler]
fn my_panic(_info: &core::panic::PanicInfo) -> ! {
    loop {}
}
