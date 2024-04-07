# Corrupted

Author: `Monk`

Can't seem to open the file.

The file was corrupted with operations used through this application:
https://tamuctf.com/5d6b407ee061e8696136d4dfd25f24b0/static/corrupted-cc.zip

## Solution

The file looks split into two parts the typical starting portion and the image data which is split with the "?" character.

In the starting portion, the first bytes don't have any magic bytes although the file extension has "jpg" so by knowing the file type these magic bytes could be put at the beginning of the file:

`ff d8 ff e0 00 10 4a 46 49 46`

However, the second part of the file is still corrupted somehow. By downloading the application the different operations that had been used could be seen in the "Favourites" section. Specifically "bit shift left" and "bit shift right" apply to the second section.

First copied the hex version, achieved with the "to hex" function on the image, of the corrupted data which was after the "?" character. Then by taking that and converting it back again with the "from hex" function and then performing a "bit shift right" with "logical shift" the correct hex data could be found. Note that using the "bit shift left" function at this point would give data that looks nothing like hex.

Now that the correct hex is given at the bottom of the file there are many "41" hex values that correspond to the letter A. This is unnecessary padding that will not let the image load. So these all have to be removed.

Now the first hex portion with the fixed magic bytes and the now fixed portion of hex could be combined and put back into CyberChef. Convert with "from hex" to get file data and then use "render image" to get the image. The flag is shown in the bottom right corner of the image. 

Flag: `gigem{uncorrupting_image_files_90812}`
