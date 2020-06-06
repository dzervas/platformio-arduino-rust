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

	# defines_list = [val[0] + "=" + str(val[1]) for val in env.get("CPPDEFINES", [])]
	# defines_list = list(set(defines_list))
	# defines = f' -D{" -D".join(defines_list)}'
	defines = env.subst(env.get("_CPPDEFFLAGS"))

	# -target should reflect cargo's target. Ex. thumbv7m-none-eabi becomes armv7m while thumbv7m-none-eabihf becomes armv7em
	# Floating point does not make a difference in target in clang, but it does in -mfloat-abi
	# -mfloat-abi=soft for software and hard for hardware. There's also softfp (?)
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
				   /home/dzervas/.platformio/packages/framework-arduinoststm32-maple/STM32F1/cores/maple/Arduino.h -- -x c++ -mfloat-abi=soft -target armv7m """ + defines + " " + headers)

	libraries_path = env.subst(env.get("_LIBDIRFLAGS"))

	env.Append(RUSTFLAGS=libraries_path)
	print(env.get("RUSTFLAGS"))

	env.Execute("cargo build --release")

	return node

env.get("BUILDERS")["Cargo"] = Builder(action=env.VerboseAction("cargo build --release", "Cargo Building $TARGET"),
									   suffix=".rs")
env.AddBuildMiddleware(ignore_main_cpp, "*src/main.cpp*")
