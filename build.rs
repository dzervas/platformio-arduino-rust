fn main() {
    // Tell cargo to tell rustc to link the system bzip2
    // shared library.
    // println!("cargo:rustc-link-lib=dylib=m");

    // println!("cargo:rustc-link-lib=static=FrameworkArduino");
    // println!("cargo:rustc-link-lib=static=FrameworkArduinoVariant");

    // println!("cargo:rustc-link-search=native=.pio/build/default");
    // println!("cargo:rustc-link-search=native=/home/dzervas/.platformio/packages/framework-arduinoadafruitnrf52/cores/nRF5/linker");
    // println!("cargo:rustc-link-search=native=/home/dzervas/.platformio/packages/toolchain-gccarmnoneeabi/arm-none-eabi/lib/thumb/v7e-m/fpv4-sp/hard");

    // println!("cargo:rustc-link-lib=dylib=c");
    // println!("cargo:rustc-link-lib=dylib=gcc");
    // println!("cargo:rustc-link-lib=dylib=cc1");

    // println!("cargo:rustc-link-search=native=/home/dzervas/.platformio/packages/toolchain-gccarmnoneeabi/arm-none-eabi/lib/hard");
    // println!("cargo:rustc-link-search=native=/home/dzervas/.platformio/packages/toolchain-gccarmnoneeabi/arm-none-eabi/lib/thumb/v7e-m");

    // println!("cargo:rustc-link-search=native=/home/dzervas/.platformio/platforms/ststm32/ldscripts");
    // println!("cargo:rustc-link-search=native=/home/dzervas/.platformio/packages/framework-arduinoststm32-maple/STM32F1/variants/maple_mini/ld");

    // Tell cargo to invalidate the built crate whenever the wrapper changes
    // println!("cargo:rerun-if-changed=Arduino.h");
}
