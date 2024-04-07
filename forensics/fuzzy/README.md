# Fuzzy

Author: `Monk`

The `image.jpg` file has a similar image file but not the same somewhere out of many jpg images. Can you find the similar image?

Images: https://drive.google.com/file/d/1pFFxyxBETIOec_FbwgjhzO7ARWqqV5YF/view

Note: The flag is not the file name, nor is the flag embedded in the image using metadata or any steg technique.

## Solution

There is the image that is given `image.jpg` and the zip file with around 30k images `image.zip`. When unzipping `images.zip` over 30k different images with all 16 character randomized names are shown. This makes it not possible to compare based on file name.

By using perceptual hashing, the hamming distance can be found on images that are similar. This can be implemented many ways however `script.py` demonstrates one possible method. It compares through all the files and only writes to the comparison results if the hamming distance is less than 15.

Comparison Results:

```
Image: hKiyfNvbXp6gBtCh.jpg, Hamming distance: 0
Image: WicL6IMHf0xg1H3E.jpg, Hamming distance: 12
Image: 0LIinznspcLN1Gy9.jpg, Hamming distance: 14
```

By looking at the output results of the script the value 0 is hKiyfNvbXp6gBtCh.jpg which is the original image. The next closest value out of all images is 12 represented by WicL6IMHf0xg1H3E.jpg file. When downloading that image from the dataset this is the image that has the flag.

It can be seen in the image however it is very dark so editing the image to brighten it would make it easier to read the flag.

Flag: `gigem{P3rC3P7U41_H45H1N6_M4NY_1M4635_94721}`
