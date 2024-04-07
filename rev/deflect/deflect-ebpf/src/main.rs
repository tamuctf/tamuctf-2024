#![no_std]
#![no_main]

use aya_bpf::{
    bindings::xdp_action,
    macros::{map, xdp},
    maps::ring_buf::RingBuf,
    programs::XdpContext,
};
use deflect_common::{IngressSyn, PROTECTED_PORT};
use network_types::{
    eth::{EthHdr, EtherType},
    ip::{IpProto, Ipv4Hdr},
    tcp::TcpHdr,
};

#[xdp]
pub fn deflect(ctx: XdpContext) -> u32 {
    match try_deflect(ctx, true) {
        Ok(ret) => ret,
        Err(_) => xdp_action::XDP_ABORTED,
    }
}

#[xdp]
pub fn deflect_tun(ctx: XdpContext) -> u32 {
    match try_deflect(ctx, false) {
        Ok(ret) => ret,
        Err(_) => xdp_action::XDP_ABORTED,
    }
}

#[map]
static EVENTS: RingBuf = RingBuf::with_byte_size(0x1000 * 4, 0);

#[inline(always)]
unsafe fn ptr_at<T>(ctx: &XdpContext, offset: usize) -> Result<&T, ()> {
    let start = ctx.data();
    let end = ctx.data_end();
    let len = core::mem::size_of::<T>();

    if start + offset + len > end {
        return Err(());
    }

    Ok(&*((start + offset) as *const T))
}

#[inline(always)]
fn try_deflect(ctx: XdpContext, check_eth: bool) -> Result<u32, ()> {
    #[cfg(debug_assertions)]
    info!(&ctx, "got packet with len {}", ctx.data_end() - ctx.data());
    let base = if check_eth {
        let eth: &EthHdr = unsafe { ptr_at(&ctx, 0)? };
        let eth_ty = eth.ether_type;
        if eth_ty != EtherType::Ipv4 {
            return Ok(xdp_action::XDP_PASS);
        }
        EthHdr::LEN
    } else {
        0
    };

    let ipv4: &Ipv4Hdr = unsafe { ptr_at(&ctx, base)? };
    #[cfg(debug_assertions)]
    info!(&ctx, "got IPv4 packet");

    if ipv4.proto != IpProto::Tcp {
        return Ok(xdp_action::XDP_PASS);
    }

    let tcp: &TcpHdr = unsafe { ptr_at(&ctx, base + Ipv4Hdr::LEN) }?;
    #[cfg(debug_assertions)]
    info!(&ctx, "got TCP packet");

    if tcp.syn() != 0 && tcp.ack() == 0 && tcp.dest == PROTECTED_PORT.to_be() {
        #[cfg(debug_assertions)]
        {
            let [a, b, c, d] = ipv4.src_addr.to_ne_bytes();
            info!(&ctx, "got a SYN with seq {} ack {} from {}.{}.{}.{}:{}",
                u32::from_be(tcp.seq),
                u32::from_be(tcp.ack_seq),
                a, b, c, d, u16::from_be(tcp.source),
            );
        }
        if tcp.seq != 0x69696969 || tcp.ack_seq != 0x69696969 || tcp.source != 0x6969 {
            let src_port = tcp.source;
            let src_ip = ipv4.src_addr;
            let dst_ip = ipv4.dst_addr;
            if let Some(mut x) = EVENTS.reserve(0) {
                let e = IngressSyn::new(src_ip, dst_ip, tcp.seq, src_port);
                x.write(e);
                x.submit(0);
            }

            return Ok(xdp_action::XDP_DROP);
        }
    }

    Ok(xdp_action::XDP_PASS)
}

#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! {
    unsafe { core::hint::unreachable_unchecked() }
}
