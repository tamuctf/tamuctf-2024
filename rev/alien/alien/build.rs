use std::fs::write;
use std::path::PathBuf;
use hex_literal::hex;
use rand_chacha::ChaChaRng;
use rand_chacha::rand_core::{RngCore, SeedableRng};

fn main() {
    let mut rng = ChaChaRng::from_seed(hex!("81d3819285d86672c1faeb1b5f9df9f21699431b8199707613d80c002d8319be"));
    let flag = include_str!("../flag.txt").as_bytes();
    let mut hexstr = vec![0u8; flag.len()];
    rng.fill_bytes(&mut hexstr);
    for (r, f) in hexstr.iter_mut().zip(flag) {
        *r ^= *f;
    }

    let mut flag_file = PathBuf::from(std::env::var_os("OUT_DIR").unwrap());
    flag_file.push("flag.bin");

    write(flag_file, hexstr).unwrap();
}