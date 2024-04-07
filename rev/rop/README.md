# ROP

Author: `nhwn`

"rev" and "pwn" have a hamming distance of 5, so they're basically the same thing, right?

## Solution

Loading the binary into Ghidra (this takes a couple years because the binary is statically linked), there's not much that looks interesting at first glance:
```c
undefined8 main(void) {
  vuln();
  return 0;
}

void vuln(void) {
  undefined local_48 [64];
  
  read(0,local_48,0x3d8);
  return;
}
```
However, if we run the binary:
```
$ ./rop
Usage: ./rop FLAG
```
Obviously, something is afoot. Something is clearly happening before/after `main`, so let's check constructors:

```
                             PTR___do_global_ctors_aux_004c17d0              XREF[4]:     call_fini:00401be1 (*), 
                                                                                          call_fini:00401be8 (R), 
                                                                                          __libc_start_main:004034a9 (R), 
                                                                                          __libc_start_main:004034e1 (R)  
        004c17d0     addr       __do_global_ctors_aux
                             //
                             // .fini_array 
                             // SHT_FINI_ARRAY  [0x4c17d8 - 0x4c17df]
                             // ram:004c17d8-ram:004c17df
                             //
```
Checking `__do_global_ctors_aux`, we have:
```c
void __do_global_ctors_aux(void) {
  return;
}
```
However, looking at the disassembly, there's a lot more happening:
```
        0040179d     LEA        RAX,[LAB_004017a6 ]
        004017a4     PUSH       RAX=>LAB_004017a6
        004017a5     RET
                                     LAB_004017a6                                    XREF[2]:     __do_global_ctors_aux:0040179d (*
                                                                                          __do_global_ctors_aux:004017a4 (*
        004017a6     MOV        ESI,0x0
        004017ab     LEA        RAX,[DAT_00498004 ]
        004017b2     MOV        RDI=>DAT_00498004 ,RAX
        004017b5     MOV        EAX,0x0
        004017ba     CALL       memfd_create                                            undefined memfd_create()
        004017bf     MOV        dword ptr [RBP + -0x4],EAX
        004017c2     MOV        EAX,dword ptr [RBP + -0x4]
        004017c5     MOV        ECX,0x0
        004017ca     MOV        EDX,0x500
        004017cf     LEA        RSI,[_data_start ]
        004017d6     MOV        EDI,EAX
        004017d8     CALL       pwrite                                                  ssize_t pwrite(int __fd, void * 
        004017dd     MOV        EAX,dword ptr [RBP + -0x4]
        004017e0     MOV        ESI,0x0
        004017e5     MOV        EDI,EAX
        004017e7     CALL       dup2                                                    int dup2(int __fd, int __fd2)
        004017ec     NOP
        004017ed     LEAVE
        004017ee     RET
```
In the decompilation for the code after the `ret`, we have a clearer view:
```c
void UndefinedFunction_004017a6(void) {
  undefined4 uVar1;
  long unaff_RBP;
  
  uVar1 = memfd_create(&DAT_00498004,0);
  *(undefined4 *)(unaff_RBP + -4) = uVar1;
  pwrite(*(int *)(unaff_RBP + -4),_data_start,0x500,0);
  dup2(*(int *)(unaff_RBP + -4),0);
  return;
}
```
This code replaces the standard input file descriptor with one that's backed by a memory region (in this case, `_data_start`). As a result, any subsequent calls to `read` will pull data `_data_start` instead of the keyboard. Going back to `vuln`, `read` tries to read in 0x3d8 bytes into a buffer of size 64. This will result in a buffer overflow, so the contents of `_data_start` will most likely consist of a ROP chain.

Treating `_data_start` as an array of `addr`, we have:
```
004c5100     addr[166]
   004c5100 00 00 00 00 00  addr      00000000                [0]                               XREF[2]:     Entry Point (*), 004017cf (*)  
            00 00 00
   004c5108 00 00 00 00 00  addr      00000000                [1]
            00 00 00
   004c5110 00 00 00 00 00  addr      00000000                [2]
            00 00 00
   004c5118 00 00 00 00 00  addr      00000000                [3]
            00 00 00
   004c5120 00 00 00 00 00  addr      00000000                [4]
            00 00 00
   004c5128 00 00 00 00 00  addr      00000000                [5]
            00 00 00
   004c5130 00 00 00 00 00  addr      00000000                [6]
            00 00 00
   004c5138 00 00 00 00 00  addr      00000000                [7]
            00 00 00
   004c5140 00 00 00 00 00  addr      00000000                [8]
            00 00 00
   004c5148 0b f8 47 00 00  addr      LAB_0047f80b            [9]
            00 00 00
   004c5150 07 00 00 00 00  addr      DAT_00000007            [10]
            00 00 00
   004c5158 77 61 61 61 78  addr      DAT_6161617861616177    [11]
            61 61 61
   004c5160 4e 9f 40 00 00  addr      LAB_00409f4d+1          [12]
            00 00 00
   004c5168 00 20 00 00 00  addr      DAT_00002000            [13]
            00 00 00
   004c5170 df 1e 40 00 00  addr      LAB_00401ede+1          [14]
            00 00 00
   004c5178 00 00 50 00 00  addr      DAT_00500000            [15]
            00 00 00
   004c5180 8e 17 40 00 00  addr      LAB_0040178e            [16]
            00 00 00
   004c5188 00 00 00 00 00  addr      00000000                [17]
            00 00 00
   004c5190 8b 17 40 00 00  addr      LAB_0040178b            [18]
            00 00 00
   004c5198 ff ff ff ff ff  addr      ffffffffffffffff        [19]
            ff ff ff
   004c51a0 89 17 40 00 00  addr      LAB_00401789            [20]
            00 00 00
   004c51a8 22 00 00 00 00  addr      DAT_00000022            [21]
            00 00 00
   004c51b0 90 88 44 00 00  addr      mmap64                  [22]
            00 00 00
   004c51b8 0b f8 47 00 00  addr      LAB_0047f80b            [23]
            00 00 00
   004c51c0 f6 00 00 00 00  addr      DAT_000000f6            [24]
            00 00 00
   004c51c8 7a 61 61 63 62  addr      636161626361617a        [25]
            61 61 63
   004c51d0 4e 9f 40 00 00  addr      LAB_00409f4d+1          [26]
            00 00 00
   004c51d8 00 00 50 00 00  addr      DAT_00500000            [27]
            00 00 00
   004c51e0 df 1e 40 00 00  addr      LAB_00401ede+1          [28]
            00 00 00
   004c51e8 00 00 00 00 00  addr      00000000                [29]
            00 00 00
   004c51f0 b0 7b 44 00 00  addr      read                    [30]
            00 00 00
   004c51f8 4e 9f 40 00 00  addr      LAB_00409f4d+1          [31]
            00 00 00
   004c5200 f6 00 00 00 00  addr      DAT_000000f6            [32]
            00 00 00
   004c5208 df 1e 40 00 00  addr      LAB_00401ede+1          [33]
            00 00 00
   004c5210 00 00 50 00 00  addr      DAT_00500000            [34]
            00 00 00
   004c5218 10 d3 41 00 00  addr      memfrob                 [35]
            00 00 00
   004c5220 4e 9f 40 00 00  addr      LAB_00409f4d+1          [36]
            00 00 00
   004c5228 00 00 00 00 00  addr      00000000                [37]
            00 00 00
   004c5230 df 1e 40 00 00  addr      LAB_00401ede+1          [38]
            00 00 00
   004c5238 1c 18 40 00 00  addr      LAB_0040181c            [39]
            00 00 00
   004c5240 00 00 50 00 00  addr      DAT_00500000            [40]
            00 00 00
   004c5248 60 ae 40 00 00  addr      srandom                 [41]
            00 00 00
   004c5250 4e 9f 40 00 00  addr      LAB_00409f4d+1          [42]
            00 00 00
   004c5258 00 00 00 00 00  addr      00000000                [43]
            00 00 00
   004c5260 df 1e 40 00 00  addr      LAB_00401ede+1          [44]
            00 00 00
   004c5268 88 cb 4c 00 00  addr      __libc_argv             [45]          = ??
            00 00 00
   004c5270 00 00 50 00 00  addr      DAT_00500000            [46]
            00 00 00
   004c5278 4e 9f 40 00 00  addr      LAB_00409f4d+1          [47]
            00 00 00
   004c5280 08 00 00 00 00  addr      DAT_00000008            [48]
            00 00 00
   004c5288 00 00 50 00 00  addr      DAT_00500000            [49]
            00 00 00
   004c5290 4e 9f 40 00 00  addr      LAB_00409f4d+1          [50]
            00 00 00
   004c5298 d3 00 50 00 00  addr      DAT_005000d3            [51]
            00 00 00
   004c52a0 b9 00 50 00 00  addr      DAT_005000b9            [52]
            00 00 00
   004c52a8 4e 9f 40 00 00  addr      LAB_00409f4d+1          [53]
            00 00 00
   004c52b0 f6 00 50 00 00  addr      DAT_005000f6            [54]
            00 00 00
   004c52b8 05 00 50 00 00  addr      DAT_00500005            [55]
            00 00 00
   004c52c0 60 c4 41 00 00  addr      strlen                  [56]
            00 00 00
   004c52c8 31 00 50 00 00  addr      DAT_00500031            [57]
            00 00 00
   004c52d0 09 00 50 00 00  addr      DAT_00500009            [58]
            00 00 00
   004c52d8 4e 9f 40 00 00  addr      LAB_00409f4d+1          [59]
            00 00 00
   004c52e0 94 9d 64 25 00  addr      DAT_25649d94            [60]
            00 00 00
   004c52e8 0d 00 50 00 00  addr      DAT_0050000d            [61]
            00 00 00
   004c52f0 b9 00 50 00 00  addr      DAT_005000b9            [62]
            00 00 00
   004c52f8 4e 9f 40 00 00  addr      LAB_00409f4d+1          [63]
            00 00 00
   004c5300 00 00 00 00 00  addr      00000000                [64]
            00 00 00
   004c5308 df 1e 40 00 00  addr      LAB_00401ede+1          [65]
            00 00 00
   004c5310 f6 00 50 00 00  addr      DAT_005000f6            [66]
            00 00 00
   004c5318 00 00 50 00 00  addr      DAT_00500000            [67]
            00 00 00
   004c5320 34 00 50 00 00  addr      DAT_00500034            [68]
            00 00 00
   004c5328 df 1e 40 00 00  addr      LAB_00401ede+1          [69]
            00 00 00
   004c5330 f6 00 50 00 00  addr      DAT_005000f6            [70]
            00 00 00
   004c5338 80 c3 41 00 00  addr      strcpy                  [71]
            00 00 00
   004c5340 31 00 50 00 00  addr      DAT_00500031            [72]
            00 00 00
   004c5348 4e 9f 40 00 00  addr      LAB_00409f4d+1          [73]
            00 00 00
   004c5350 00 00 00 00 00  addr      00000000                [74]
            00 00 00
   004c5358 df 1e 40 00 00  addr      LAB_00401ede+1          [75]
            00 00 00
   004c5360 f6 00 50 00 00  addr      DAT_005000f6            [76]
            00 00 00
   004c5368 00 00 50 00 00  addr      DAT_00500000            [77]
            00 00 00
   004c5370 38 00 50 00 00  addr      DAT_00500038            [78]
            00 00 00
   004c5378 75 00 50 00 00  addr      DAT_00500075            [79]
            00 00 00
   004c5380 4e 9f 40 00 00  addr      LAB_00409f4d+1          [80]
            00 00 00
   004c5388 ba d5 92 37 52  addr      144e5d523792d5ba        [81]
            5d 4e 14
   004c5390 0d 00 50 00 00  addr      DAT_0050000d            [82]
            00 00 00
   004c5398 b9 00 50 00 00  addr      DAT_005000b9            [83]
            00 00 00
   004c53a0 4e 9f 40 00 00  addr      LAB_00409f4d+1          [84]
            00 00 00
   004c53a8 07 00 00 00 00  addr      DAT_00000007            [85]
            00 00 00
   004c53b0 df 1e 40 00 00  addr      LAB_00401ede+1          [86]
            00 00 00
   004c53b8 f6 00 50 00 00  addr      DAT_005000f6            [87]
            00 00 00
   004c53c0 00 00 50 00 00  addr      DAT_00500000            [88]
            00 00 00
   004c53c8 38 00 50 00 00  addr      DAT_00500038            [89]
            00 00 00
   004c53d0 75 00 50 00 00  addr      DAT_00500075            [90]
            00 00 00
   004c53d8 4e 9f 40 00 00  addr      LAB_00409f4d+1          [91]
            00 00 00
   004c53e0 01 59 8e 0c b8  addr      74673b80c8e5901         [92]
            73 46 07
   004c53e8 0d 00 50 00 00  addr      DAT_0050000d            [93]
            00 00 00
   004c53f0 b9 00 50 00 00  addr      DAT_005000b9            [94]
            00 00 00
   004c53f8 4e 9f 40 00 00  addr      LAB_00409f4d+1          [95]
            00 00 00
   004c5400 0e 00 00 00 00  addr      DAT_0000000e            [96]
            00 00 00
   004c5408 df 1e 40 00 00  addr      LAB_00401ede+1          [97]
            00 00 00
   004c5410 f6 00 50 00 00  addr      DAT_005000f6            [98]
            00 00 00
   004c5418 00 00 50 00 00  addr      DAT_00500000            [99]
            00 00 00
   004c5420 38 00 50 00 00  addr      DAT_00500038            [100]
            00 00 00
   004c5428 75 00 50 00 00  addr      DAT_00500075            [101]
            00 00 00
   004c5430 4e 9f 40 00 00  addr      LAB_00409f4d+1          [102]
            00 00 00
   004c5438 43 d0 44 e2 a2  addr      1602c4a2e244d043        [103]
            c4 02 16
   004c5440 0d 00 50 00 00  addr      DAT_0050000d            [104]
            00 00 00
   004c5448 b9 00 50 00 00  addr      DAT_005000b9            [105]
            00 00 00
   004c5450 4e 9f 40 00 00  addr      LAB_00409f4d+1          [106]
            00 00 00
   004c5458 15 00 00 00 00  addr      DAT_00000015            [107]
            00 00 00
   004c5460 df 1e 40 00 00  addr      LAB_00401ede+1          [108]
            00 00 00
   004c5468 f6 00 50 00 00  addr      DAT_005000f6            [109]
            00 00 00
   004c5470 00 00 50 00 00  addr      DAT_00500000            [110]
            00 00 00
   004c5478 38 00 50 00 00  addr      DAT_00500038            [111]
            00 00 00
   004c5480 75 00 50 00 00  addr      DAT_00500075            [112]
            00 00 00
   004c5488 4e 9f 40 00 00  addr      LAB_00409f4d+1          [113]
            00 00 00
   004c5490 73 82 9a a7 14  addr      89fd614a79a8273         [114]
            d6 9f 08
   004c5498 0d 00 50 00 00  addr      DAT_0050000d            [115]
            00 00 00
   004c54a0 b9 00 50 00 00  addr      DAT_005000b9            [116]
            00 00 00
   004c54a8 df 1e 40 00 00  addr      LAB_00401ede+1          [117]
            00 00 00
   004c54b0 e5 00 50 00 00  addr      DAT_005000e5            [118]
            00 00 00
   004c54b8 00 c9 40 00 00  addr      puts                    [119]
            00 00 00
   004c54c0 df 1e 40 00 00  addr      LAB_00401ede+1          [120]
            00 00 00
   004c54c8 00 00 00 00 00  addr      00000000                [121]
            00 00 00
   004c54d0 70 ab 40 00 00  addr      exit                    [122]
            00 00 00
   004c54d8 62 a1 16 1d e9  addr      14a362e91d16a162        [123]
            62 a3 14
   004c54e0 e9 62 a3 ed e9  addr      c27c7de9eda362e9        [124]
            7d 7c c2
   004c54e8 26 9f da d5 74  addr      1b627574d5da9f26        [125]
            75 62 1b
   004c54f0 ed 62 1b dd 62  addr      2aeded62dd1b62ed        [126]
            ed ed 2a
   004c54f8 2a 2a 2a 63 ed  addr      2a2bebed632a2a2a        [127]
            eb 2b 2a
   004c5500 2a 2a 63 25 6e  addr      dc1bd36e25632a2a        [128]
            d3 1b dc
   004c5508 e9 d5 fa e9 62  addr      e9d4a362e9fad5e9        [129]
            a3 d4 e9
   004c5510 62 eb cd 22 62  addr      22c5eb6222cdeb62        [130]
            eb c5 22
   004c5518 e9 62 a3 d2 62  addr      62ccdd62d2a362e9        [131]
            dd cc 62
   004c5520 eb c8 29 62 a3  addr      eb62eda36229c8eb        [132]
            ed 62 eb
   004c5528 c2 17 62 23 e8  addr      cdeb62e8236217c2        [133]
            62 eb cd
   004c5530 29 62 eb c5 29  addr      fd2b6229c5eb6229        [134]
            62 2b fd
   004c5538 62 a3 d2 62 94  addr      d5d5d59462d2a362        [135]
            d5 d5 d5
   004c5540 d5 d5 d5 d5 35  addr      da036235d5d5d5d5        [136]
            62 03 da
   004c5548 62 25 67 d2 e9  addr      ebed62e9d2672562        [137]
            62 ed eb
   004c5550 0f 2a 2a 2a 63  addr      63d2a3632a2a2a0f        [138]
            a3 d2 63
   004c5558 ed eb 2b 2a 2a  addr      af672a2a2a2bebed        [139]
            2a 67 af
   004c5560 ea 5e 00 63 dd  addr      2a2beadd63005eea        [140]
            ea 2b 2a
   004c5568 2a 2a 5e 24 66  addr      62e5a366245e2a2a        [141]
            a3 e5 62
   004c5570 a3 e4 c2 88 d5  addr      63d5d5d588c2e4a3        [142]
            d5 d5 63
   004c5578 a3 d3 62 a3 e5  addr      e4a362e5a362d3a3        [143]
            62 a3 e4
   004c5580 c2 be d5 d5 d5  addr      d3a362d5d5d5bec2        [144]
            62 a3 d3
   004c5588 63 fb c2 c1 fb  addr      e5a366fbc1c2fb63        [145]
            66 a3 e5
   004c5590 e9 62 af d5 5e  addr      62e92b5ed5af62e9        [146]
            2b e9 62
   004c5598 af dc 5e 22 62  addr      c2dda362225edcaf        [147]
            a3 dd c2
   004c55a0 1e e2 da d5 1b  addr      b7c3d51bd5dae21e        [148]
            d5 c3 b7
   004c55a8 80 da d5 7f 59  addr      4f4d4b597fd5da80        [149]
            4b 4d 4f
   004c55b0 10 0a 04 05 58  addr      a5a455805040a10         [150]
            45 5a 0a
   004c55b8 6c 66 6b 6d 2a  addr      4b427e2a6d6b666c        [151]
            7e 42 4b
   004c55c0 5e 0d 59 0a 5e  addr      a4f425e0a590d5e         [152]
            42 4f 0a
   004c55c8 4c 46 4b 4d 0b  addr      2a0b4d4b464c            [153]
            2a 00 00
```

At a brief glance, the chain appears to initially do the following:

1. `mmap` an RWX region at 0x500000.
2. `read` more bytes into the RWX region.
3. Deobfuscate the bytes from #2 with `memfrob` (this is just xor with 42).

Starting from 0x004c54d8, we can use a [builtin GhidraScript](https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/Features/Base/ghidra_scripts/XorMemoryScript.java) to deobfuscate the memory after 0x04c54d8 (note that the script only takes input in hex, so use 0x2a).

Here's the deobfuscated region:
```
    004c54d8     MOV        RDI,qword ptr [RDI + RSI*0x1]
    004c54dc     RET
    004c54dd     MOV        qword ptr [RSI],RDI
    004c54e0     RET
    004c54e1     MOV        RDI,RAX
    004c54e4     RET
    004c54e5     PUSH       RDI
    004c54e6     PUSH       RSI
    004c54e7     CALL       SUB_003d09f8
    004c54ec     POP        RSI
    004c54ed     POP        RDI
    004c54ee     XOR        RDI,RAX
    004c54f1     XOR        RDI,RSI
    004c54f4     MOV        RDI,0x0
    004c54fb     MOV        R9,0x1
    004c5502     CMOVZ      RDI,R9
    004c5506     XOR        ESI,ESI
    004c5508     RET
    004c5509     CALL       RAX
    004c550b     RET
    004c550c     MOV        RSI,RDI
    004c550f     RET
    004c5510     SHL        RDI,0x8
    004c5514     SHR        RDI,0x8
    004c5518     RET
                         *************************************************************
                         *                           FUNCTION                          
                         *************************************************************
                         undefined  FUN_004c5519 ()
         undefined         AL:1           <RETURN>
                         FUN_004c5519                                    XREF[2]:     004c5572 (c), 004c5580 (c)  
    004c5519     MOV        RAX,RDI
    004c551c     MUL        RSI
    004c551f     SHL        RDX,0x3
    004c5523     MOV        RDI,RAX
    004c5526     SHR        RAX,0x3d
    004c552a     OR         RDX,RAX
    004c552d     SHL        RDI,0x3
    004c5531     SHR        RDI,0x3
    004c5535     ADD        RDI,RDX
    004c5538     MOV        RAX,RDI
    004c553b     MOV        RSI,0x1fffffffffffffff
    004c5545     SUB        RAX,RSI
    004c5548     CMOVGE     RDI,RAX
    004c554c     RET
    004c554d     MOV        RCX,0x25
    004c5554     MOV        R8,RDI
    004c5557     MOV        R9,0x1
                         LAB_004c555e                                    XREF[1]:     004c558b (j)  
    004c555e     TEST       R8,R8
    004c5561     JZ         LAB_004c558d
    004c5563     TEST       R8,0x1
    004c556a     JZ         LAB_004c557a
    004c556c     MOV        RDI,R9
    004c556f     MOV        RSI,RCX
    004c5572     CALL       FUN_004c5519                                            undefined FUN_004c5519()
    004c5577     MOV        R9,RDI
                         LAB_004c557a                                    XREF[1]:     004c556a (j)  
    004c557a     MOV        RDI,RCX
    004c557d     MOV        RSI,RCX
    004c5580     CALL       FUN_004c5519                                            undefined FUN_004c5519()
    004c5585     MOV        RCX,RDI
    004c5588     SHR        R8,0x1
    004c558b     JMP        LAB_004c555e
                         LAB_004c558d                                    XREF[1]:     004c5561 (j)  
    004c558d     MOV        RDI,R9
    004c5590     RET
    004c5591     TEST       RDI,RDI
    004c5594     JZ         LAB_004c5597
    004c5596     RET
                         LAB_004c5597                                    XREF[1]:     004c5594 (j)  
    004c5597     TEST       RSI,RSI
    004c559a     JZ         LAB_004c55a4
    004c559c     MOV        RDI,RSI
    004c559f     CALL       SUB_003d1dd8
                         LAB_004c55a4                                    XREF[1]:     004c559a (j)  
    004c55a4     XOR        EDI,EDI
    004c55a6     JMP        LAB_003d0048
    004c55ab     ds         "Usage: ./rop FLAG"
    004c55bd     ds         "That's the flag!"
```

Note that the resolved calls are broken since they're intended to execute from a base address of 0x500000. The new instructions appear to consist mostly of primitive gadgets, with a couple of big functions. At this point, it's probably more useful to look at the program in gdb. After some manual analysis, it looks like the conditional behavior for user input is routed through this gadget:
```
    004c54e5     PUSH       RDI
    004c54e6     PUSH       RSI
    004c54e7     CALL       SUB_003d09f8 /* rand() in gdb */
    004c54ec     POP        RSI
    004c54ed     POP        RDI
    004c54ee     XOR        RDI,RAX
    004c54f1     XOR        RDI,RSI
    004c54f4     MOV        RDI,0x0
    004c54fb     MOV        R9,0x1
    004c5502     CMOVZ      RDI,R9
    004c5506     XOR        ESI,ESI
    004c5508     RET
```
Translating to C, we have something like this:
```c
uint64_t gadget(uint64_t input, uint64_t constant) {
    if (input ^ rand() == constant) {
        return 1;
    } else {
        return 0;
    }
}
```
Computing `rand() ^ constant` for the first time through the gadget yields 28, and since this is preceded by a call to `strlen`, the flag is probably 28 characters long. By supplying a dummy string of 28 characters, we can hit this gadget 4 more times. Now, let's take a closer look at what happens before each of those comparisons. After some more investigation, we see that our input is split into 4 chunks of 7 bytes each, then fed to this function:

```c
void UndefinedFunction_004c554d(ulong param_1) {
  undefined8 uVar1;
  undefined8 uVar2;
  
  uVar1 = 0x25;
  uVar2 = 1;
  for (; param_1 != 0; param_1 >>= 1) {
    if ((param_1 & 1) != 0) {
      FUN_004c5519(uVar2,uVar1);
    }
    FUN_004c5519(uVar1,uVar1);
  }
  return;
}
```
This looks a lot like [exponentiation by squaring](https://en.wikipedia.org/wiki/Exponentiation_by_squaring). Looking at the disassembly for `FUN_004c5519`, it looks like modular multiplication modulo 0x1fffffffffffffff (this number comes from the conditional subtraction at the end and can be verified with test inputs). Putting the pieces together, the flag check amounts to something like this:

```py
guess = b"A" * 28
check = [0x144e5d522649ff85, 0x74673b83c0d340e, 0x1602c4a2e8905106, 0x89fd614b95180c8]
for i in range(4):
    chunk = int.from_bytes(guess[i * 7:(i + 1) * 7], byteorder="little")
    assert pow(37, chunk, 0x1fffffffffffffff) == check[i]
```
Now, it's just a matter of solving the discrete logarithms to recover the flag. In SageMath:

```py
from sage.all import *
# 0x1fffffffffffffff is 2^61 - 1, which is prime
K = GF(0x1fffffffffffffff)
# 37 is a primitve root modulo 2^61 - 1, so solutions are guaranteed
g = K(37)

check = [0x144e5d522649ff85, 0x74673b83c0d340e, 0x1602c4a2e8905106, 0x89fd614b95180c8]
flag = b""
for c in check:
    dlog = int(discrete_log(K(c), g))
    chunk = dlog.to_bytes(7, byteorder="little")
    flag += chunk
print(flag.decode())
```
Flag: `gigem{i_<3_m3rs3nn3_pr1m35!}`
