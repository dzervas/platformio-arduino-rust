import os

# PlatformIO specific
Import("env")

def ignore_main_cpp(node):
	# headers = f' -I {" -I ".join(env.get("CPPPATH"))}'
	headers = env.subst(env.get("_CPPINCFLAGS"))
	print(headers)

	# defines_list = [val[0] + "=" + str(val[1]) for val in env.get("CPPDEFINES", [])]
	# defines_list = list(set(defines_list))
	# defines = f' -D{" -D".join(defines_list)}'
	defines = env.subst(env.get("_CPPDEFFLAGS"))
	print(defines)

	env.Execute("bindgen /home/dzervas/.platformio/packages/framework-arduinoadafruitnrf52/cores/nRF5/Arduino.h -- " + defines + headers)

	# Link compiled libraries to Rust
	# libraries_list = []

	# for node_list in env.get("LIBS"):
	# 	if node_list  == "m": continue

	# 	for node_file in node_list:
	# 		libraries_list.append(node_file.get_abspath())

	# libraries = f' -L {" -L ".join(libraries_list)}'
	libraries = env.subst(env.get("_LIBDIRFLAGS"))

	env.Append(RUSTFLAGS=libraries)

	# Debug: Show Rust flags
	print(env.get("RUSTFLAGS"))

	env.Execute("cargo build")

	return None

env.AddBuildMiddleware(ignore_main_cpp, "*src/main.cpp*")
