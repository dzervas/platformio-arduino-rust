extern crate bindgen;
extern crate proc_macro;
extern crate syn;

use std::env;
use std::path::{Path, PathBuf};

use proc_macro::TokenStream;
use syn::{parse_macro_input, LitStr};

#[proc_macro]
pub fn pio_include(input: TokenStream) -> TokenStream {
    let header = parse_macro_input!(input as LitStr);
    let header_str = header.value();

    let include_paths = env::var("CPPPATH").expect("Unable to read CPPPATH environment variable");
    let mut try_path = header_str.clone();
    let mut header_path = Path::new(&header_str);

    for path in include_paths.split(":") {
        if header_path.exists() { break; }

        try_path = format!("{}/{}", path, header_str);

        header_path = Path::new(&try_path);
    }

    if !header_path.exists() { panic!(format!("Header file {} was not found", header_str)); }

    // The bindgen::Builder is the main entry point
    // to bindgen, and lets you build up options for
    // the resulting bindings.
    // For more options check https://llvm.org/docs/HowToCrossCompileLLVM.html
    // Probably need:
    // -DCMAKE_CROSSCOMPILING=True
    // -DCMAKE_CXX_FLAGS='<CC FLAGS>'
    println!("Generating bindings for {}", &try_path);
    let bindings = bindgen::Builder::default()
        .header(try_path)
        // .parse_callbacks(Box::new(bindgen::CargoCallbacks))

        .ctypes_prefix("pio_rust")
        .use_core()
        .blacklist_item("std::*")
        .blacklist_item("FP_NAN")
        .blacklist_item("FP_INFINITE")
        .blacklist_item("FP_ZERO")
        .blacklist_item("FP_NORMAL")
        .blacklist_item("FP_SUBNORMAL")
        .blacklist_item("SVCALL")
        .blacklist_function("setup")
        .blacklist_function("loop")
        .clang_arg("-DCMAKE_CROSSCOMPILING=True")
        .clang_arg("-DCMAKE_CXX_FLAGS=-Wl,--gc-sections,--relax -mcpu=cortex-m4 -mfloat-abi=hard -mfpu=fpv4-sp-d16")
        // .clang_arg("-mfloat-abi").clang_arg("hard")
        // .clang_arg("-target").clang_arg("armv7em")
        // .clang_arg("-sysroot").clang_arg("~/.platformio/packages/toolchain-gccarmnoneeabi/arm-none-eabi/")
        .rustfmt_bindings(false)

        .generate()
        .expect("Unable to generate bindings");

    // Write the bindings to the $OUT_DIR/bindings.rs file.
    // let out_path = PathBuf::from(env::var("OUT_DIR").unwrap());
    // let out_file = out_path.join(format!("{}.rs", header_str));

    // println!("Writing bindings to {:?}", &out_file);

    // bindings
    //     .write_to_file(out_file)
    //     .expect("Couldn't write bindings!");

    // println!("cargo:rerun-if-changed=build.rs");

    // (quote!{
        // concat!("include!(\"", #header_str, ".rs\");")
        // }).into()
    // format!("include!(\"{}\");", header_str)
    format!("include!(\"platformio.rs\");")
        .parse().unwrap()
}
