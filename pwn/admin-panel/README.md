# Admin Panel

Author: `FlamePyromancer`

I made a secure login panel for administrators to access. 
I might not be the best C programmer out there, but just in case, I decided to enable several standard security measures to prevent unauthorized access. 

NOTE: Successful exploit attempts may take several tries, due to security measures.

## Solution

It's not apparent from the source, but the `password` buffer lies before the `status` buffer. Since there's a length mismatch (44 bytes are read into a 24-byte buffer), we can overflow into the `status` buffer, allowing us to overwrite "Login Successful!\n" to be a format string of our choice. Since we get another buffer overflow when execution reaches `admin()`, I chose to leak the canary and the return address of `main()` (`__libc_start_main()` is in libc, so this can be used to compute libc's base address) from the format string. With ASLR broken, I used a libc gadget to set `rax` to 0, then jumped to a one\_gadget (`rax == 0` was the only constraint).

Note that the exploit may need to be thrown multiple times since whitespace characters in either the canary or libc gadget addresses may prematurely truncate input. See `solve.py` for details. 

Flag: `gigem{l3ak1ng_4ddre55e5_t0_byp4ss_s3cur1t1e5!!}`
