#![no_std]
use bytemuck::{Pod, Zeroable};

pub const PROTECTED_PORT: u16 = 80;

#[repr(C)]
#[derive(Clone, Copy)]
// fields are in big-endian
pub struct IngressSyn {
    pub src_ip: u32,
    pub dst_ip: u32,
    pub seq: u32,
    pub src_port: u32,
}

impl IngressSyn {
    pub fn new(src_ip: u32, dst_ip: u32, seq: u32, src_port: u16) -> Self {
        Self {
            src_ip,
            dst_ip,
            seq,
            src_port: src_port as u32,
        }
    }
    pub fn from_bytes(bs: &[u8]) -> &Self {
        bytemuck::from_bytes(&bs[..core::mem::size_of::<Self>()])
    }
    pub fn as_bytes(&self) -> &[u8] {
        bytemuck::bytes_of(self)
    }
}

unsafe impl Zeroable for IngressSyn {}
unsafe impl Pod for IngressSyn {}
