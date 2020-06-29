FROM ubuntu:latest

RUN apt-get update && apt-get install -y build-essential curl python3 python3-distutils vim

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y --default-toolchain nightly
RUN python3 -c "$(curl -fsSL https://raw.githubusercontent.com/platformio/platformio/develop/scripts/get-platformio.py)" && \
	echo 'export "PATH=$HOME/.platformio/penv/bin:$PATH"' >> ~/.profile

RUN ~/.cargo/bin/rustup target install thumbv7em-none-eabi

RUN ~/.cargo/bin/cargo install bindgen
