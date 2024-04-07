# Truncated 1

Author: `Monk`

Only part of the private key was able to be retrieved. Decrypt the flag.txt.enc file.

## Solution

With `script.py`, q can be extracted from the private key and is the only thing needed to reconstruct the private key. From the public key, n and e can be retreived with this command:

```
openssl rsa -pubin -in public.pem -inform PEM -text -noout
```

Then, convert the hex to decimal. Once all values are retrieved, use RsaCtfTool to get the private key.

```
python3 RsaCtfTool.py --private -n [number] -q [number] -e [number]
```

Copy the private key into a new file and make sure permissions are 600 (chmod 600). Then you can use this command to get the flag:

```
openssl pkeyutl -decrypt -inkey reconstructedprivate.pem -in flag.txt.enc -out flag.txt
```

This is a good resource to see the different parts of the RSA private key: https://crypto.stackexchange.com/questions/6593/what-data-is-saved-in-rsa-private-key.

Flag: `gigem{Q_Fr0M_Pr1V473_K3Y_89JD54}`
