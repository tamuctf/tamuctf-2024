# Volatile

Author: `Monk`

The RAM was able to be captured in a memory dump on the machine of the discord administrator that was tasked with hiding the flag. Can you find the flag in the memory dump?

Download from here:
https://tamuctf.com/5d6b407ee061e8696136d4dfd25f24b0/static/volatile.zip

## Solution

Volatility can be used to analyze the memory dump. Using the `userassist` plugin will dump the items which are used to populate the user's start menu. This includes all of the files relevant to this challenge. The first two files I noticed were `attachments_1220077759921913966_flag.jpg.exe` and `attachments_1220077759921913966_flag.jpg`. Knowing that the challenge prompt indicates that the memory dump was on a Discord admin's computer, the file names looked a lot like Discord's CDN links. Navigating to `https://media.discordapp.net/attachments/994115000769724416/1220077759921913966/flag.jpg` however, displays `This content is no longer available.`. I decided to compare this link to a sample link on Discord. The fresh link has 3 extra parameters, `ex`, `is`, and `hm`, which, when removed, display the same error message. I decided to check the `userassist` output again for files with names containing `ex`, `is`, and `hm`, and I found 3 files as shown below.

```
ex_660da0f5
is_65fb2bf5
hm_cdf9154025cad44fd5bd9edaebc8ee6c345bfa92fc99110ac1f56ffab993de4d
```

Using all of the discovered fragments it is possible to reconstruct the link.

`https://media.discordapp.net/attachments/994115000769724416/1220077759921913966/flag.jpg?ex=660da0f5&is=65fb2bf5&hm=cdf9154025cad44fd5bd9edaebc8ee6c345bfa92fc99110ac1f56ffab993de4d`

Flag: `gigem{v0l471l17y_15_u53ful_h8945d}`
