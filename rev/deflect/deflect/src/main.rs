#![feature(try_blocks)]
use anyhow::anyhow;
use aya::maps::ring_buf::RingBuf;
use aya::programs::{Xdp, XdpFlags};
use aya::{include_bytes_aligned, Bpf};
use deflect_common::{IngressSyn, PROTECTED_PORT};
use nix::sys::resource::{setrlimit, Resource, RLIM_INFINITY};
use nix::sys::socket::{
    sendto, socket, AddressFamily, MsgFlags, SockFlag, SockProtocol, SockType, SockaddrIn,
};
use pnet_packet::ip::IpNextHeaderProtocols;
use pnet_packet::ipv4::MutableIpv4Packet;
use pnet_packet::tcp::MutableTcpPacket;
use pnet_packet::tcp::TcpFlags;
use std::net::Ipv4Addr;
use std::os::fd::{AsRawFd, OwnedFd};
use tokio::io::{unix::AsyncFd, Interest};
use tokio::signal;
use warp::Filter;

struct Killer(OwnedFd);

impl Killer {
    fn new() -> Result<Self, anyhow::Error> {
        Ok(Self(socket(
            AddressFamily::Inet,
            SockType::Raw,
            SockFlag::empty(),
            SockProtocol::Raw,
        )?))
    }
    fn kill(&self, i: &IngressSyn) -> Result<(), anyhow::Error> {
        let src_port = u16::from_be(i.src_port as u16);
        let ack = u32::from_be(i.seq) + 1;
        let src = i.src_ip.to_ne_bytes();
        let dst = i.dst_ip.to_ne_bytes();
        let actual_src = Ipv4Addr::new(dst[0], dst[1], dst[2], dst[3]);
        let actual_dst = Ipv4Addr::new(src[0], src[1], src[2], src[3]);
        let sin = SockaddrIn::new(src[0], src[1], src[2], src[3], src_port);

        let mut packet = [0u8; MutableIpv4Packet::minimum_packet_size()
            + MutableTcpPacket::minimum_packet_size()];
        let (a, b) = packet.split_at_mut(MutableIpv4Packet::minimum_packet_size());
        let mut ipv4 = MutableIpv4Packet::new(a).unwrap();
        let mut tcp = MutableTcpPacket::new(b).unwrap();
        ipv4.set_version(4);
        ipv4.set_header_length(5);
        ipv4.set_total_length(40);
        ipv4.set_flags(2);
        ipv4.set_ttl(64);
        ipv4.set_next_level_protocol(IpNextHeaderProtocols::Tcp);
        ipv4.set_source(actual_src);
        ipv4.set_destination(actual_dst);
        let chk = pnet_packet::ipv4::checksum(&ipv4.to_immutable());
        ipv4.set_checksum(chk);

        tcp.set_data_offset(5);
        tcp.set_source(PROTECTED_PORT);
        tcp.set_destination(src_port);
        tcp.set_flags(TcpFlags::RST | TcpFlags::ACK);
        tcp.set_acknowledgement(ack);
        let chk = pnet_packet::tcp::ipv4_checksum(&tcp.to_immutable(), &actual_src, &actual_dst);
        tcp.set_checksum(chk);

        // blocking is extremely unlikely
        sendto(self.0.as_raw_fd(), &packet, &sin, MsgFlags::empty())?;

        Ok(())
    }
}

#[tokio::main]
async fn main() -> Result<(), anyhow::Error> {
    let iface = std::env::args().nth(1).unwrap_or("lo".to_string());
    let flag = std::fs::read_to_string("flag.txt").map_or("test", |x| x.leak());
    let bind_ip = nix::ifaddrs::getifaddrs()?
        .filter(|x| x.interface_name == iface)
        .find_map(|x| Some(x.address?.as_sockaddr_in()?.ip().to_be_bytes()))
        .ok_or(anyhow!("no IPv4 address for {iface}"))?;

    setrlimit(Resource::RLIMIT_MEMLOCK, RLIM_INFINITY, RLIM_INFINITY)?;

    #[cfg(debug_assertions)]
    let mut bpf = Bpf::load(include_bytes_aligned!(
        "../../target/bpfel-unknown-none/debug/deflect"
    ))?;
    #[cfg(not(debug_assertions))]
    let mut bpf = Bpf::load(include_bytes_aligned!(
        "../../target/bpfel-unknown-none/release/deflect"
    ))?;

    env_logger::init();
    if let Err(e) = aya_log::BpfLogger::init(&mut bpf) {
        log::warn!("failed to initialize eBPF logger: {}", e);
    }

    let program_name = if iface.contains("tun") {
        "deflect_tun"
    } else {
        "deflect"
    };
    let program: &mut Xdp = bpf
        .program_mut(program_name)
        .ok_or(anyhow!("missing program"))?
        .try_into()?;
    program.load()?;
    program.attach(&iface, XdpFlags::SKB_MODE)?;

    let events: RingBuf<_> = bpf
        .take_map("EVENTS")
        .ok_or(anyhow!("missing map"))?
        .try_into()?;
    let mut fd = AsyncFd::with_interest(events, Interest::READABLE)?;
    let killer = Killer::new()?;
    tokio::task::spawn(async move {
        loop {
            let res: Result<(), anyhow::Error> = try {
                let mut guard = fd.readable_mut().await?;
                let ring_buf = guard.get_inner_mut();
                while let Some(x) = ring_buf.next() {
                    killer.kill(IngressSyn::from_bytes(&x))?;
                }
                guard.clear_ready();
            };
            if let Err(e) = res {
                eprintln!("{e}");
            }
        }
    });

    tokio::select! {
        _ = signal::ctrl_c() => {},
        _ = warp::serve(warp::path::end().map(move || flag)).run((bind_ip, PROTECTED_PORT)) => {},
    }
    Ok(())
}
