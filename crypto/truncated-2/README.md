# Truncated 2

Author: `Monk`

It seems even less was able to be retrieved this time. Decrypt the flag.txt.enc file.

## Solution

By using `script.py`, you can get dp and dq. With the following openssl command used on the public key, you can get n and e values:

```
openssl rsa -pubin -in public.pem -inform PEM -text -noout
```

You can convert the hex to a number, then plug the numbers into [this script](https://github.com/jvdsn/crypto-attacks/blob/master/attacks/rsa/known_crt_exponents.py), which will give p and q.

From there, you have all the values you need to recontruct the private key. You can now use RsaCtfTool to get the private key:

```
python3 RsaCtfTool.py --private -n [number] -p [number] -q [number] -e [number]
```

Now with the private key the, `flag.txt.enc` can be decrypted.

```
openssl pkeyutl -decrypt -inkey reconstructedprivate.pem -in flag.txt.enc -out flag.txt
```

Be sure to use `chmod 600` on the private key before using it.

Flag: `gigem{DP_DQ_r54_7rUNC473D_SDA79}`
