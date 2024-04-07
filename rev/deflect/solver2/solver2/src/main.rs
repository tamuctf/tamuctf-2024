use aya::programs::{tc, SchedClassifier, TcAttachType};
use aya::{include_bytes_aligned, Ebpf};
use aya_log::EbpfLogger;
use clap::Parser;
use log::{debug, info, warn};
use tokio::signal;

#[cfg(feature = "tun")]
const IFACE: &'static str = "tun0";
#[cfg(not(feature = "tun"))]
const IFACE: &'static str = "docker0";

#[tokio::main]
async fn main() -> Result<(), anyhow::Error> {
    env_logger::init();

    // Bump the memlock rlimit. This is needed for older kernels that don't use the
    // new memcg based accounting, see https://lwn.net/Articles/837122/
    let rlim = libc::rlimit {
        rlim_cur: libc::RLIM_INFINITY,
        rlim_max: libc::RLIM_INFINITY,
    };
    let ret = unsafe { libc::setrlimit(libc::RLIMIT_MEMLOCK, &rlim) };
    if ret != 0 {
        debug!("remove limit on locked memory failed, ret is: {}", ret);
    }

    // This will include your eBPF object file as raw bytes at compile-time and load it at
    // runtime. This approach is recommended for most real-world use cases. If you would
    // like to specify the eBPF program at runtime rather than at compile-time, you can
    // reach for `Bpf::load_file` instead.
    #[cfg(debug_assertions)]
    let mut bpf = Ebpf::load(include_bytes_aligned!(
        "../../target/bpfel-unknown-none/debug/solver2"
    ))?;
    #[cfg(not(debug_assertions))]
    let mut bpf = Ebpf::load(include_bytes_aligned!(
        "../../target/bpfel-unknown-none/release/solver2"
    ))?;
    if let Err(e) = EbpfLogger::init(&mut bpf) {
        // This can happen if you remove all log statements from your eBPF program.
        warn!("failed to initialize eBPF logger: {}", e);
    }
    // error adding clsact to the interface if it is already added is harmless
    // the full cleanup can be done with 'sudo tc qdisc del dev eth0 clsact'.
    let _ = tc::qdisc_add_clsact(IFACE);
    let program: &mut SchedClassifier = bpf.program_mut("solver2_egress").unwrap().try_into()?;
    program.load()?;
    program.attach(IFACE, TcAttachType::Egress)?;
    let program: &mut SchedClassifier = bpf.program_mut("solver2_ingress").unwrap().try_into()?;
    program.load()?;
    program.attach(IFACE, TcAttachType::Ingress)?;

    info!("Waiting for Ctrl-C...");
    signal::ctrl_c().await?;
    info!("Exiting...");

    Ok(())
}
