FROM rust:slim-buster

ARG name

RUN apt update; apt install -y gcc-arm-none-eabi
RUN rustup target add thumbv7m-none-eabi

ADD .cargo /$name/.cargo
ADD alien /$name/alien
ADD lm3s6965-uart /$name/lm3s6965-uart
ADD Cargo.toml /$name/Cargo.toml
ADD flag.txt /$name/flag.txt

WORKDIR /$name
RUN cargo build --release
RUN mv /$name/target/thumbv7m-none-eabi/release/$name /$name/$name.elf

# stripping doesn't seem to be possible with cargo settings?
RUN arm-none-eabi-strip /$name/$name.elf
