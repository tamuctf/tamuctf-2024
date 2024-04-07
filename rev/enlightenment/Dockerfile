FROM rust:alpine

ARG name

RUN apk update
RUN apk add --no-cache alpine-sdk openssl-dev openssl-libs-static

ADD src /$name/src
ADD Cargo.toml /$name/Cargo.toml

WORKDIR /$name
RUN cargo build --release
