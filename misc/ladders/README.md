# Ladders

Author: `Monk`

PLCs use ladder logic as a programming language. Where is the flag in the code?

## Solution

Based on the description the file is most likely a PLC file and with the extension being "ckp" it becomes clear that this is a Click PLC Programming Ladder Logic Project file. So by downloading the Click software it could be used to open the project file.

When running strings you can see some registers that have part of the flag:

```
g,DISCRETE,X001
i,DISCRETE,X002
e,DISCRETE,X004
m,DISCRETE,X005
l,DISCRETE,X007
a,DISCRETE,X008
d,DISCRETE,X009
r,DISCRETE,X012
```

When loading the project into the software multiple things can be seen. There are Rung comments (can be modified in "Edit Rung Comments"), an email, and the same registers X001, X002 that was seen in strings seem to have a nickname of the start of the flag "g" for X001 and "i" for X002. Not all of the addresses in the strings were shown in the ladder logic code. So when going to Address picker to see all of the addresses the nicknames of all the addresses could be seen but also for the ones that were seemingly skipped there was an "Address Comment" that had the other pieces of the flag.

By appending all of the characters from X001 to X034 the flag can be found.

Flag: `gigem{ladders_Address_x9y524z}`
