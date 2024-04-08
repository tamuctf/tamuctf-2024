# Deflect

Author: `nhwn`

An overworked TAMUctf dev went rogue and started leaking flags on one of our internal networks! The service was last seen online at http://10.8.0.1:1337, but we can't seem to connect to the server for some reason. We've managed to recover the server binary and some of the source code; can you figure out a way to communicate with the server?

Once you've figured it out, use the provided OpenVPN configuration file to connect to the internal network.

## Solution

Reading the provided source code, we're looking at a simple HTTP server that sits behind an [Aya](https://github.com/aya-rs/aya) [eBPF](https://ebpf.io/) [XDP](https://www.tigera.io/learn/guides/ebpf/ebpf-xdp/) program. At first glance, it seems like sending a GET request to `/` should just give us the flag, but this doesn't work:
```
$ curl http://10.8.0.1:1337
curl: (7) Failed to connect to 10.8.0.1 port 1337 after 59 ms: Couldn't connect to server
```
In other words, the port appears closed. Looking at the source code, the `kill` function appears to manually craft and send back a TCP packet with the RST and ACK flags set (this is the standard response for attempting to connect to a port without a server listening on it), so it's clear that the eBPF program is doing some kind of filtering to incoming TCP packets.

Even though source of the eBPF program is not provided, we have the binary itself, and the userspace source code shows that the eBPF program is embedded directly inside the binary with `include_bytes!`, so we can simply use `binwalk --dd='.*' deflect` to recover the ELF file that Aya loads.

Loading the ELF into Ghidra, we can observe how the eBPF program checks incoming TCP packets by comparing the offsets to standard network packet headers:
```c
undefined4 * deflect(longlong *param_1)

{
  undefined4 *ret;
  undefined4 *puVar1;
  longlong *plVar2;
  longlong *plVar3;
  longlong packet;
  longlong seq;
  longlong src_port;
  undefined8 uVar4;
  undefined8 uVar5;
  
  plVar3 = *(longlong **)((longlong)param_1 + 4);
  packet = *param_1;
  ret = (undefined4 *)0x0;
  if (((longlong *)(packet + 0xeU) <= plVar3) &&
     (ret = (undefined4 *)0x2, (*(longlong *)(packet + 0xd) << 8 | *(ulonglong *)(packet + 0xc)) == 8)) {
    plVar2 = (longlong *)(packet + 0x22);
    ret = (undefined4 *)0x0;
    if (((plVar2 <= plVar3) &&
        (((ret = (undefined4 *)0x2, *(longlong *)(packet + 0x17) == 6 &&
          (ret = (undefined4 *)0x0, (longlong *)(packet + 0x36U) <= plVar3)) &&
          /* & 0x12 == 2 checks for SYN without ACK flag */
         (puVar1 = (undefined4 *)0x2, ret = puVar1, (*(ulonglong *)(packet + 0x2f) & 0x12) == 2)))) &&
       (*(longlong *)(packet + 0x24) == 0x3905)) {
      seq = *(longlong *)(packet + 0x26);
      if (seq == 0x69696969) {
        src_port = *plVar2;
        /* 0x2a is the acknowledgment number offset */
        if ((*(longlong *)(packet + 0x2a) == 0x69696969) && (src_port == 0x6969)) {
          return (undefined4 *)0x2;
        }
      }
      else {
        src_port = *plVar2;
      }
      uVar5 = *(undefined8 *)(packet + 0x1e);
      uVar4 = *(undefined8 *)(packet + 0x1a);
      /* probably writes back into an eBPF map to tell userspace that this is a bad packet since ret == 1 */
      bpf_undef();
      ret = (undefined4 *)0x1;
      if (puVar1 != (undefined4 *)0x0) {
        puVar1[3] = (int)src_port;
        puVar1[2] = (int)seq;
        puVar1[1] = (int)uVar5;
        *puVar1 = (int)uVar4;
        bpf_undef();
        ret = (undefined4 *)0x1;
      }
    }
  }
  return ret;
}
```

In short, every incoming SYN packet must meet 3 conditions:

1. The sequence number field must be 0x69696969 (technically in big-endian, but all the bytes are the same, so it's whatever).
2. The acknowledgement number field must be 0x69696969.
3. The source port must be 0x6969.

If any of these conditions are unmet, the eBPF program will signal userspace to send RST/ACK back to the client. Thus, we just need to modify the outbound SYN packet of our connection to satisfy the above conditions.

There are 3 main ways to do this:
1. Use raw sockets.
2. Write another eBPF program that intercepts and modifies packets.
3. Use [nfqueue](https://home.regit.org/netfilter-en/using-nfqueue-and-libnetfilter_queue/) to redirect the packets to a userspace program for modification.

I decided to go with the third strategy since implementing a TCP/IP stack in userspace is annoying (for example, if you use raw sockets, you need to drop outbound RST packets since the Linux kernel will try to terminate TCP connections that it didn't make). The second strategy is implemented courtesy of Addison in `solver2`.

To correctly implement custom sequence numbers using the third strategy, we need to be careful about what sequence numbers are perceived by our client program that makes the GET request. In particular, we need the sequence/acknowledgment numbers in the server's response packets to match the client's expected values prior to modification of the initial sequence number (if they don't match, then the connection will be closed by the kernel).

This Python script will modify TCP connections to port 1337 such that all the requirements are satisfied:
```py
from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP
from subprocess import run

PORT = 1337
SHIFT = 0
ORIGINAL_SRC_PORT = 0
MAGIC = 0x69696969
MAGIC_PORT = 0x6969

def sh(x):
    run(x.split())

sh(f"iptables -A INPUT -p tcp -m tcp --sport {PORT} -j NFQUEUE --queue-num 1")
sh(f"iptables -A OUTPUT -p tcp -m tcp --dport {PORT} -j NFQUEUE --queue-num 1")

def mod(x: int):
    return x & 0xffffffff

def callback(pkt):
    global SHIFT
    global ORIGINAL_SRC_PORT
    p = IP(pkt.get_payload())
    print(p, p[TCP].seq, p[TCP].ack)
    if p[TCP].dport == PORT:
        if p[TCP].flags.S:
            SHIFT = mod(MAGIC - p[TCP].seq)
            p[TCP].seq = MAGIC
            p[TCP].ack = MAGIC
            ORIGINAL_SRC_PORT = p[TCP].sport
        else:
            p[TCP].seq = mod(p[TCP].seq + SHIFT)
        p[TCP].sport = MAGIC_PORT
    else:
        p[TCP].ack = mod(p[TCP].ack - SHIFT)
        p[TCP].dport = ORIGINAL_SRC_PORT
    del p[TCP].chksum
    p = IP(bytes(p))
    print(p, p[TCP].seq, p[TCP].ack)
    pkt.set_payload(bytes(p))
    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, callback)

try:
    nfqueue.run()
except KeyboardInterrupt:
    pass

nfqueue.unbind()

sh(f"iptables -D INPUT -p tcp -m tcp --sport {PORT} -j NFQUEUE --queue-num 1")
sh(f"iptables -D OUTPUT -p tcp -m tcp --dport {PORT} -j NFQUEUE --queue-num 1")
```

After connecting to the VPN using `sudo openvpn deflect.ovpn` and starting the filter with `sudo python3 filter.py`, we just need to make the GET request:
```
$ curl http://10.8.0.1:1337
gigem{l3t_m3_1n_l3t_m3_1n_l3t_m3_1n}
```

Flag: `gigem{l3t_m3_1n_l3t_m3_1n_l3t_m3_1n}`
