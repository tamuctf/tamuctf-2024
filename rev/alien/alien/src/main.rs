#![deny(unsafe_code)]
#![deny(warnings)]
#![no_main]
#![no_std]

use rtic::app;

const FLAG_BYTES: &[u8] = include_bytes!(concat!(env!("OUT_DIR"), "/flag.bin"));

#[app(device = lm3s6965, dispatchers = [GPIOA, GPIOB, GPIOC])]
mod app {
    use hex_literal::hex;
    use lm3s6965_uart::{
        ManageUART, ReadUART, UARTAddress, UARTPeripheral, UARTPeripheralManageHalf, UARTPeripheralReadHalf, UARTPeripheralWriteHalf, WriteUART,
    };
    use rand_chacha::ChaChaRng;
    use rand_chacha::rand_core::{RngCore, SeedableRng};
    use crate::FLAG_BYTES;

    #[shared]
    struct Shared {}

    #[local]
    struct Local {
        sender_manage: UARTPeripheralManageHalf,
        sender_rx: UARTPeripheralReadHalf,
        sender_tx: UARTPeripheralWriteHalf,
    }

    #[init]
    #[allow(unsafe_code)]
    #[allow(unreachable_code)]
    fn init(_: init::Context) -> (Shared, Local, init::Monotonics) {
        let (sender_manage, sender_rx, sender_tx) =
            unsafe { UARTPeripheral::new(UARTAddress::UART0) }
                .enable_transmit(true)
                .enable_receive(true)
                .enable_fifo(true)
                .enable_break_interrupt(true)
                .enable_receive_interrupt(true)
                .finish()
                .split();

        (
            Shared {},
            Local {
                sender_manage,
                sender_rx,
                sender_tx,
            },
            init::Monotonics(),
        )
    }

    #[idle]
    fn idle(_: idle::Context) -> ! {
        loop {
            cortex_m::asm::wfi(); // peacefully sleep *honk mimimimi*
        }
    }

    #[task(binds = UART0, priority = 1, local = [sender_rx])]
    fn recv_msg_sender(cx: recv_msg_sender::Context) {
        let uart = cx.local.sender_rx;

        while uart.rx_avail() {
            if uart.readb().is_err() { return; }
            let _ = send_msg_sender::spawn();
        }
    }

    #[task(priority = 2, capacity = 1, local = [sender_manage, sender_tx])]
    fn send_msg_sender(cx: send_msg_sender::Context) {
        let sender_manage = cx.local.sender_manage;
        let sender_tx = cx.local.sender_tx;

        let mut rng = ChaChaRng::from_seed(hex!("81d3819285d86672c1faeb1b5f9df9f21699431b8199707613d80c002d8319be"));
        let mut flag = [0u8; FLAG_BYTES.len()];
        rng.fill_bytes(&mut flag);

        for (r, f) in flag.iter_mut().zip(FLAG_BYTES) {
            *r ^= *f;
        }

        sender_manage
            .update_interrupts()
            .update_transmit_interrupt(true)
            .commit();

        for b in flag {
            while !sender_tx.tx_avail() {
                cortex_m::asm::wfi();
            }
            sender_tx.writeb(b);
        }

        sender_manage
            .update_interrupts()
            .update_transmit_interrupt(false)
            .commit();
    }
}

#[panic_handler]
fn panic_handler(_: &core::panic::PanicInfo) -> ! {
    loop {
        cortex_m::asm::nop()
    }
}
