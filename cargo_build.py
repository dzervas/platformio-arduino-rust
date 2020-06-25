import os
from os.path import join
from glob import glob
from pathlib import Path
from SCons.Script import Builder

# PlatformIO specific
Import("env")

def ignore_main_cpp(node):
	headers = env.subst(env.get("_CPPINCFLAGS"))

	toolchain_dir = env.PioPlatform().get_package_dir("toolchain-gccarmnoneeabi")
	toolchain_headers_path = join(toolchain_dir, "lib/gcc/arm-none-eabi/*/include")
	toolchain_headers_paths = [str(Path(p)) for p in glob(toolchain_headers_path)]
	toolchain_headers = " -I" + " -I".join(toolchain_headers_paths)

	headers += toolchain_headers + " "

	defines = env.subst(env.get("_CPPDEFFLAGS")).replace("\\\"", "\"")

	# -target should reflect cargo's target. Ex. thumbv7m-none-eabi becomes armv7m while thumbv7m-none-eabihf becomes armv7em
	# Floating point does not make a difference in target in clang, but it does in -mfloat-abi
	# -mfloat-abi=soft for software and hard for hardware. There's also softfp (?)
	# I have no idea why the nrf52, while being hard requires soft ABI. Gotta check that at some point
	env.Execute("""bindgen --ctypes-prefix pio_rust --use-core \
				   --blacklist-item std::* \
				   --blacklist-item FP_NAN \
				   --blacklist-item FP_INFINITE \
				   --blacklist-item FP_ZERO \
				   --blacklist-item FP_NORMAL \
				   --blacklist-item FP_SUBNORMAL \
				   --blacklist-item SVCALL \
				   --blacklist-function setup \
				   --blacklist-function loop \
				   -o src/platformio.rs \
				   """ + env.get("PROJECT_PACKAGES_DIR") +"""/framework-arduinoadafruitnrf52/cores/nRF5/Arduino.h -- \
				   -mfloat-abi=soft \
				   -target armv7em """ + defines + " " + headers)

	env.Execute("cargo build --release --target=thumbv7em-none-eabihf -v")
	env.Append(PIOBUILDFILES=["$PROJECT_DIR/target/thumbv7em-none-eabihf/release/deps/ardurust-platformio.o"])

	return None

env.AddBuildMiddleware(ignore_main_cpp, "*src/main.cpp*")
