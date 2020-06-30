
#![allow(dead_code)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(non_upper_case_globals)]
#![allow(clippy::approx_constant)]
#![allow(clippy::redundant_static_lifetimes)]

pub type c_schar = i8;
pub type c_uchar = u8;
pub type c_char = i8;
pub type c_short = i16;
pub type c_ushort = u16;
pub type c_int = i16;
pub type c_uint = u16;
pub type c_float = f32;
pub type c_double = f64;
pub type c_long = i32;
pub type c_ulong = u32;
pub type c_longlong = i64;
pub type c_ulonglong = u64;
pub type intmax_t = i64;
pub type uintmax_t = u64;

pub type size_t = usize;
pub type ptrdiff_t = isize;
pub type intptr_t = isize;
pub type uintptr_t = usize;
pub type ssize_t = isize;

pub type c_void = core::ffi::c_void;

pub mod Arduino_h;
// pub use Arduino_h::*;
