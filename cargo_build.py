import os
from configparser import ConfigParser, NoOptionError
from os import listdir, popen
from os.path import isdir, isfile
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

def get_header_search_paths():
	# Include search in standard gcc search paths and Arduino core
	search_paths = env.subst("$_CPPINCFLAGS").split("-I")

	# Include search in platformio libraries
	for d in env.get("LIBSOURCE_DIRS"):
		d_path = env.subst(d)
		if not isdir(d_path):
			continue

		for directory in listdir(d_path):
			if isdir(d_path + "/" +directory + "/src"):
				search_paths.append(d_path + "/" + directory + "/src")
			else:
				search_paths.append(d_path + "/" + directory)

	return search_paths

def option_list(option):
	result = []

	if isinstance(option, list):
		option = option[0]

	result = option.split("\n")

	if len(result) <= 1:
		result = option.split(",")

	result = [x.strip() for x in result]

	return result


def get_rust_headers():
	# Parse rust_headers option from the config
	try:
		headers_to_process_str = CONFIG.get(env.subst("env:$PIOENV"), "rust_c_headers")
		headers_to_process = option_list(headers_to_process_str)
	except NoOptionError:
		headers_to_process = []
		pass

	try:
		cxx_headers_to_process_str = CONFIG.get(env.subst("env:$PIOENV"), "rust_cxx_headers")
		cxx_headers_to_process = option_list(cxx_headers_to_process_str)

		headers_to_process.extend([x + "+" for x in cxx_headers_to_process])
	except NoOptionError:
		pass


	print("Searching headers to generate bindings:", headers_to_process)

	headers_found = {}

	search_paths = get_header_search_paths()

	# Search for the header in the paths above
	for header in headers_to_process:
		found = False
		cxx = (header[-1] == "+")
		if cxx:
			header = header[:-1]

		for inc_path in search_paths:
			inc_path = inc_path.strip()
			header_path = inc_path + "/" + header

			if isfile(header_path):
				name = header.replace("/", "_")
				name = name.replace(".", "_")
				name += ".rs"

				if cxx:
					name += "+"

				headers_found[name] = header_path
				found = True
				break

		if not found:
			raise Exception("Unable to find header", header)

	print("Found headers:", headers_found)
	return headers_found

def ignore_main_cpp(node):
	defines = env.subst("$_CPPDEFFLAGS").replace("\\\"", "\"")
	sysroot = popen(env.subst("$CC -print-sysroot")).read().strip()
	target = CONFIG.get(env.subst("env:$PIOENV"), "rust_target").strip()

	env.Execute("mkdir -p $PROJECT_SRC_DIR/platformio")
	mod_rs = open(env.subst("$PROJECT_SRC_DIR/platformio/mod.rs"), "w")
	mod_rs.write(MOD_PRELUDE)

	for name, h in get_rust_headers().items():
		cxx = (name[-1] == "+")
		if cxx:
			name = name[:-1]

		# -target should reflect cargo's target. Ex. thumbv7m-none-eabi becomes armv7m while thumbv7m-none-eabihf becomes armv7em
		# Floating point does not make a difference in target in clang, but it does in -mfloat-abi
		# -mfloat-abi=soft for software and hard for hardware. There's also softfp (?)
		# I have no idea why the nrf52, while being hard requires soft ABI. Gotta check that at some point
		result = env.Execute("""bindgen --ctypes-prefix super --use-core \
					   --blacklist-item std \
					   --blacklist-item std::* \
					   --blacklist-item *va_list \
					   --blacklist-item FP_NAN \
					   --blacklist-item FP_INFINITE \
					   --blacklist-item FP_ZERO \
					   --blacklist-item FP_NORMAL \
					   --blacklist-item FP_SUBNORMAL \
					   --blacklist-item SVCALL \
					   --blacklist-item tusb_desc_endpoint_t \
					   --blacklist-item tusb_desc_endpoint_t__bindgen_ty_2 \
					   --blacklist-function setup \
					   --blacklist-function loop \
					   --blacklist-function *printf \
					   --blacklist-function *printf_r \
					   --blacklist-function *scanf \
					   --blacklist-function *scanf_r \
					   --blacklist-item random \
					   --enable-function-attribute-detection \
					   --no-derive-debug \
					   --no-derive-copy \
					   --conservative-inline-namespaces \
					   -o $PROJECT_SRC_DIR/platformio/{name} \
					   {header} -- {cxx} \
					   -DCMAKE_CROSSCOMPILING=True \
					   -DLLVM_DEFAULT_TARGET_TRIPLE={target} \
					   -DCMAKE_C_FLAGS="$CCFLAGS" \
					   -DCMAKE_CXX_FLAGS="$CXXFLAGS" \
					   {defines} {includes} \
					   -I/home/dzervas/.platformio/packages/toolchain-gccarmnoneeabi/arm-none-eabi/include/c++/7.2.1/ \
					   -I/home/dzervas/.platformio/packages/toolchain-gccarmnoneeabi/arm-none-eabi/include/c++/7.2.1/arm-none-eabi \
					   --sysroot "{sysroot}" \
					   -mfloat-abi=soft \
					   -target {target}""" .format(
						   name=name,
						   header=h,
						   cxx="-x c++" if cxx else "",
						   sysroot=sysroot,
						   target=target,
						   defines=defines,
						   includes=" -I".join(get_header_search_paths())))

		if result:
			env.Exit(1)

		# As the preprocessor does not have any idea abut namespaces, we can re-export all the functions safely
		mod_rs.write("""
pub mod {name};
// pub use {name}::*;
""".format(name=name[:-3]))  # Remove .rs extension

	mod_rs.close()

	if "RUSTFLAGS" not in env.get("ENV"):
		env.get("ENV")["RUSTFLAGS"] = ""

	env.get("ENV")["RUSTFLAGS"] += "--emit obj -C extra-filename=-platformio -C default-linker-libraries=no"

	env.Execute("cargo build --release -v --target=" + target)
	env.Append(PIOBUILDFILES=["$PROJECT_DIR/target/" + target + "/release/deps/firmware-platformio.o"])

	return None

env.AddBuildMiddleware(ignore_main_cpp, "*src/main.cpp*")
