fn main() {
    // Tell cargo to tell rustc to link the system bzip2
    // shared library.
    println!("cargo:rustc-link-lib=static=m");
    println!("cargo:rustc-link-lib=static=gcc");
    println!("cargo:rustc-link-lib=static=FrameworkArduino");
    println!("cargo:rustc-link-lib=static=FrameworkArduinoVariant");

    println!("cargo:rustc-link-search=native=.pio/build/default");
    println!("cargo:rustc-link-search=native=/home/dzervas/.platformio/platforms/ststm32/ldscripts");
    println!("cargo:rustc-link-search=native=/home/dzervas/.platformio/packages/framework-arduinoststm32-maple/STM32F1/variants/maple_mini/ld");

    // Tell cargo to invalidate the built crate whenever the wrapper changes
    // println!("cargo:rerun-if-changed=Arduino.h");
}
