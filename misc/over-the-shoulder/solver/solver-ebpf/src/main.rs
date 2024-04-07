#![no_std]
#![no_main]

use aya_ebpf::helpers::bpf_probe_read_user_str_bytes;
use aya_ebpf::{macros::tracepoint, programs::TracePointContext, EbpfContext};
use aya_log_ebpf::info;

#[tracepoint]
pub fn solver(ctx: TracePointContext) -> u32 {
    unsafe { try_solver(ctx) }.unwrap_or_else(|ret| ret)
}

unsafe fn try_solver(ctx: TracePointContext) -> Result<u32, u32> {
    let command = ctx.command().map_err(|_| 1u32)?;
    if &command[..4] == b"cat\0" {
        if ctx.read_at::<i64>(16).map_err(|_| 2u32)? == 1 {
            let buf: *const u8 = ctx.read_at(24).map_err(|_| 3u32)?;
            let mut scratch = [0u8; 64];
            let flag = unsafe {
                core::str::from_utf8_unchecked(
                    bpf_probe_read_user_str_bytes(buf, &mut scratch).map_err(|_| 4u32)?,
                )
            };
            info!(&ctx, "found flag: {}", flag);
        }
    }
    Ok(0)
}

#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! {
    unsafe { core::hint::unreachable_unchecked() }
}
