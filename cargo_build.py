import os
from configparser import ConfigParser, NoOptionError
from glob import glob
from os import popen
from os.path import join, isfile
from pathlib import Path
from SCons.Script import Builder

# PlatformIO specific
Import("env")

CONFIG = ConfigParser()
CONFIG.read(env.subst("$PROJECT_CONFIG"))
MOD_PRELUDE = """
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
"""

def get_rust_headers():
	try:
		headers_to_process_str = CONFIG.get(env.subst("env:$PIOENV"), "rust_headers")
	except NoOptionError:
		return []

	if isinstance(headers_to_process_str, list):
		headers_to_process_str = headers_to_process_str[0]

	if not headers_to_process_str:
		return []

	headers_to_process = headers_to_process_str.split("\n")

	if len(headers_to_process) <= 1:
		headers_to_process = headers_to_process_str.split(",")

	if not headers_to_process:
		return []

	headers_to_process = [x.strip() for x in headers_to_process]

	print("Searching headers to generate bindings:", headers_to_process)

	headers_found = {}

	for header in headers_to_process:
		found = False

		for inc_path in env.get("CPPPATH"):
			header_path = inc_path + "/" + header

			if isfile(header_path):
				name = header.replace("/", "_")
				name = name.replace(".", "_")
				name += ".rs"

				headers_found[name] = header_path
				found = True
				break

		if not found:
			print("Unable to find header", header)

	print("Found headers:", headers_found)
	return headers_found

def ignore_main_cpp(node):
	defines = env.subst("$_CPPDEFFLAGS").replace("\\\"", "\"")
	sysroot = popen(env.subst("$CC -print-sysroot")).read().strip()
	target = CONFIG.get(env.subst("env:$PIOENV"), "rust_target").strip()

	mod_rs = open(env.subst("$PROJECT_SRC_DIR/platformio/mod.rs"), "w")
	mod_rs.write(MOD_PRELUDE)

	env.Execute("mkdir -p $PROJECT_SRC_DIR/platformio")

	for name, h in get_rust_headers().items():
		# -target should reflect cargo's target. Ex. thumbv7m-none-eabi becomes armv7m while thumbv7m-none-eabihf becomes armv7em
		# Floating point does not make a difference in target in clang, but it does in -mfloat-abi
		# -mfloat-abi=soft for software and hard for hardware. There's also softfp (?)
		# I have no idea why the nrf52, while being hard requires soft ABI. Gotta check that at some point
		env.Execute("""bindgen --ctypes-prefix super --use-core \
					   --blacklist-item std::* \
					   --blacklist-item FP_NAN \
					   --blacklist-item FP_INFINITE \
					   --blacklist-item FP_ZERO \
					   --blacklist-item FP_NORMAL \
					   --blacklist-item FP_SUBNORMAL \
					   --blacklist-item SVCALL \
					   --blacklist-function setup \
					   --blacklist-function loop \
					   -o $PROJECT_SRC_DIR/platformio/{name} \
					   {header} -- \
					   -DCMAKE_CROSSCOMPILING=True \
					   -DLLVM_DEFAULT_TARGET_TRIPLE={target} \
					   -DCMAKE_CXX_FLAGS="$CCFLAGS $CXXFLAGS" \
					   {defines} $_CPPINCFLAGS \
					   --sysroot "{sysroot}" \
					   -mfloat-abi=soft \
					   -target {target}""" .format(
						   name=name,
						   header=h,
						   sysroot=sysroot,
						   target=target,
						   defines=defines))

		# As the preprocessor does not have any idea abut namespaces, we can re-export all the functions safely
		mod_rs.write("""
pub mod {name};
pub use {name}::*;
		""".format(name=name[:-3]))  # Remove .rs extension

	mod_rs.close()
	env.Execute("cargo build --release -v --target=" + target)
	env.Append(PIOBUILDFILES=["$PROJECT_DIR/target/" + target + "/release/deps/firmware-platformio.o"])

	return None

env.AddBuildMiddleware(ignore_main_cpp, "*src/main.cpp*")
