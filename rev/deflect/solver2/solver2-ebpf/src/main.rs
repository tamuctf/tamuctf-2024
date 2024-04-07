#![feature(ip_bits)]
#![no_std]
#![no_main]

use core::ffi::c_void;
use core::mem;
use core::mem::offset_of;
use core::net::Ipv4Addr;
use core::ptr::read_unaligned;

use aya_ebpf::bindings::BPF_F_RECOMPUTE_CSUM;
use aya_ebpf::helpers::{
    bpf_l3_csum_replace, bpf_l4_csum_replace, bpf_set_hash_invalid, bpf_skb_store_bytes,
};
use aya_ebpf::macros::map;
use aya_ebpf::maps::{Array, HashMap, Stack};
use aya_ebpf::{macros::classifier, programs::TcContext};
use aya_log_ebpf::{info, warn};
use network_types::eth::{EthHdr, EtherType};
use network_types::ip::Ipv4Hdr;
use network_types::tcp::TcpHdr;

#[cfg(feature = "tun")]
const INITIAL_OFFSET: usize = 0;
#[cfg(not(feature = "tun"))]
const INITIAL_OFFSET: usize = EthHdr::LEN;

#[cfg(feature = "tun")]
const TARGET: Ipv4Addr = Ipv4Addr::new(10, 8, 0, 1);
#[cfg(not(feature = "tun"))]
const TARGET: Ipv4Addr = Ipv4Addr::new(172, 17, 0, 2);

#[inline(always)]
unsafe fn ptr_at<T>(ctx: &TcContext, offset: usize) -> Result<*mut T, i32> {
    let start = ctx.data();
    let end = ctx.data_end();
    let len = mem::size_of::<T>();

    if start + offset + len > end {
        return Err(1);
    }

    let ptr = (start + offset) as *mut T;
    Ok(&mut *ptr)
}

#[repr(C)]
struct StashedSeq {
    seq: u32,
}

#[map]
static SEQ_STASH: Array<u32> = Array::with_max_entries(1, 0);

#[classifier]
pub fn solver2_egress(ctx: TcContext) -> i32 {
    unsafe { try_solver2_egress(&ctx) }.unwrap_or_else(|ret| ret)
}

unsafe fn try_solver2_egress(ctx: &TcContext) -> Result<i32, i32> {
    #[cfg(not(feature = "tun"))]
    {
        let ethhdr: *const EthHdr = unsafe { ptr_at(&ctx, 0)? };
        if read_unaligned(ethhdr.byte_add(offset_of!(EthHdr, ether_type)) as *const EtherType)
            != EtherType::Ipv4
        {
            return Ok(0); // we can't do anything with this packet
        }
    }

    // only affect traffic to localhost:80
    let ipv4hdr: *const Ipv4Hdr = unsafe { ptr_at(&ctx, INITIAL_OFFSET)? };
    let dst = u32::from_be(unsafe { (*ipv4hdr).dst_addr });
    let dst = Ipv4Addr::from_bits(dst);

    let octets = dst.octets();
    info!(
        ctx,
        "caught packet to: {}.{}.{}.{}", octets[0], octets[1], octets[2], octets[3]
    );

    if TARGET == dst {
        let mut tcphdr: &mut TcpHdr = unsafe { &mut *ptr_at(&ctx, INITIAL_OFFSET + Ipv4Hdr::LEN)? };
        if tcphdr.dest.swap_bytes() == 80 {
            // LBB0_4
            // mask is 0x12 = 0x10 | 0x2
            // 0x10 is ack, 0x2 is syn because r2 is offset 0xd
            // (r2 & 0x12) == 0x2 means ack is not set, syn is set
            // goddamn bitmagic
            let base_seq;
            if tcphdr.syn() != 0 && tcphdr.ack() == 0 {
                info!(ctx, "original sequence header is {}", tcphdr.seq);
                base_seq = tcphdr.seq.swap_bytes();
                *SEQ_STASH.get_ptr_mut(0).ok_or(1)? = base_seq;

                // this will be overridden by remote anyway
                let orig_ack_seq = tcphdr.ack_seq;
                tcphdr.ack_seq = 0x69696969;

                // rather than rewriting the source, we just force this in curl
                // tcphdr.source = 0x6969; // 41
            } else {
                base_seq = *SEQ_STASH.get(0).ok_or(1)?;
            }
            let orig_seq = tcphdr.seq;
            tcphdr.seq = tcphdr
                .seq
                .swap_bytes()
                .overflowing_sub(base_seq)
                .0
                .overflowing_add(0x69696969)
                .0
                .swap_bytes();
            info!(ctx, "rewrote client => server");
        }
    }
    Ok(0)
}

#[classifier]
pub fn solver2_ingress(ctx: TcContext) -> i32 {
    unsafe { try_solver2_ingress(&ctx) }.unwrap_or_else(|ret| ret)
}

unsafe fn try_solver2_ingress(ctx: &TcContext) -> Result<i32, i32> {
    #[cfg(not(feature = "tun"))]
    {
        let ethhdr: *const EthHdr = unsafe { ptr_at(&ctx, 0)? };
        if read_unaligned(ethhdr.byte_add(offset_of!(EthHdr, ether_type)) as *const EtherType)
            != EtherType::Ipv4
        {
            return Ok(0); // we can't do anything with this packet
        }
    }

    // only affect traffic to localhost:80
    let ipv4hdr: *const Ipv4Hdr = unsafe { ptr_at(&ctx, INITIAL_OFFSET)? };
    let src = u32::from_be(unsafe { (*ipv4hdr).src_addr });
    let src = Ipv4Addr::from_bits(src);

    if TARGET == src {
        let tcphdr: &mut TcpHdr = unsafe { &mut *ptr_at(&ctx, INITIAL_OFFSET + Ipv4Hdr::LEN)? };
        if tcphdr.source.swap_bytes() == 80 {
            let base_seq = *SEQ_STASH.get(0).ok_or(1)?;

            let new_ack_seq = tcphdr
                .ack_seq
                .swap_bytes()
                .overflowing_sub(0x69696969)
                .0
                .overflowing_add(base_seq)
                .0
                .swap_bytes();
            bpf_skb_store_bytes(
                ctx.skb.skb,
                (INITIAL_OFFSET + Ipv4Hdr::LEN + offset_of!(TcpHdr, ack_seq)) as u32,
                &new_ack_seq as *const u32 as *const c_void,
                4,
                BPF_F_RECOMPUTE_CSUM as u64,
            );
            info!(ctx, "rewrote server => client");
        }
    }
    Ok(0)
}

#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! {
    unsafe { core::hint::unreachable_unchecked() }
}
