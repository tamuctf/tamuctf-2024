# Jumbled

Author: `Monk`

The RSA public and private keys are provided. However, the private key seems to be jumbled in a block size of 10 hex characters. Can you get the flag?

## Solution

Provided is the private key that is shuffled (private) in hex, the unshuffled public key in hex, and the `flag.txt` file encrypted with RSA. It's also provided in the description that the shuffle occurred in a block size of 10.

All private keys have the same beginning, which is represented by this in hex:

```
2D 2D 2D 2D 2D 42 45 47 49 4E 20 50 52 49 56 41 54 45 20 4B 45 59 2D 2D 2D 2D 2D
```

When taking the first 10 hex characters from that, you get:

```
2d 2d 2d 2d 2d 42 45 47 49 4e
```

Now when compared against the private key provided:

Correct: `2d 2d 2d 2d 2d 42 45 47 49 4e`

Shuffled: `49 45 4e 42 47 2d 2d 2d 2d 2d`

From this, a permutation order of this can be found:

`8,6,9,5,7,?,?,?,?,?`

Because of the `2d` values, the last 5 can't be confirmed until looking at the second block of 10 hex characters, which is also provided in the first bytes of the RSA private key.

Correct: `20 50 52 49 56 41 54 45 20 4b`

Shuffled: `20 54 4b 41 45 49 50 56 20 52`

From here, the first 5 can be confirmed, and the last 5 in the permutation order can be found. This is the permutation order:

```
8,6,9,5,7,3,1,4,0,2
```

Now, a simple Python script can be run over the entire private key jumbled hex values to get the original private key. This script is shown in `unshuffle.py`. After that, convert the hex to text and put it in `private.pem` file. 

The same can be done for the public key hex, which was unshuffled and can be put into a `public.pem` file. This file isn't needed for this challenge; however, it can provide more information about the private key file, so this can be solved by looking at the public key values that correspond with the private key as well.

Once the `private.pem` file is retrieved, openssl can be used to get the flag.

```
openssl pkeyutl -decrypt -inkey private.pem -in flag.txt.enc -out flag.txt
```

Flag: `gigem{jumbl3d_r54_pr1v473_k3y_z93kd74lx}`
