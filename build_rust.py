import os
from os.path import join
from glob import glob
from pathlib import Path

# PlatformIO specific
Import("env")

def ignore_main_cpp(node):
	headers = env.subst(env.get("_CPPINCFLAGS"))

	toolchain_dir = env.PioPlatform().get_package_dir("toolchain-gccarmnoneeabi")
	toolchain_headers_path = join(toolchain_dir, "lib/gcc/arm-none-eabi/*/include")
	toolchain_headers_paths = [str(Path(p)) for p in glob(toolchain_headers_path)]
	toolchain_headers = " -I" + " -I".join(toolchain_headers_paths)

	headers += toolchain_headers + " "

	# defines_list = [val[0] + "=" + str(val[1]) for val in env.get("CPPDEFINES", [])]
	# defines_list = list(set(defines_list))
	# defines = f' -D{" -D".join(defines_list)}'
	defines = env.subst(env.get("_CPPDEFFLAGS"))

	env.Execute("""bindgen --ctypes-prefix pio_rust --use-core \
				   --blacklist-item FP_NAN \
				   --blacklist-item FP_INFINITE \
				   --blacklist-item FP_ZERO \
				   --blacklist-item FP_NORMAL \
				   --blacklist-item FP_SUBNORMAL \
				   --blacklist-function setup \
				   --blacklist-function loop \
				   --blacklist-item std::* \
				   --blacklist-item SVCALL \
				   -o src/platformio.rs \
				   /home/dzervas/.platformio/packages/framework-arduinoadafruitnrf52/cores/nRF5/Arduino.h -- -target armv7em """ + defines + " " + headers)

	# Link compiled libraries to Rust
	# libraries_list = []

	# for node_list in env.get("LIBS"):
	# 	if node_list  == "m": continue

	# 	for node_file in node_list:
	# 		libraries_list.append(node_file.get_abspath())

	# libraries = f' -L {" -L ".join(libraries_list)}'
	libraries_path = env.subst(env.get("_LIBDIRFLAGS"))

	env.Append(RUSTFLAGS=libraries_path)

	env.Execute("cargo build")

	return node

env.AddBuildMiddleware(ignore_main_cpp, "*src/main.cpp*")
