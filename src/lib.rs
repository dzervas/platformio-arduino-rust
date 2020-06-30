#![no_std]

mod platformio;

use platformio::Arduino_h::{pinMode, digitalWrite, delay};

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
        delay(100);
    }
}

#[panic_handler]
fn my_panic(_info: &core::panic::PanicInfo) -> ! {
    loop {}
}
