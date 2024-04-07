# Reveille Petter

Author: `kit`

We got [this program](https://tamuctf.com/5d6b407ee061e8696136d4dfd25f24b0/static/reveille-petter.zip) that has our school mascot, and it promises a flag. Can you get the flag?

## Dev Notes

Source files are located in the `src` folder. The project is built with godot and just opening the folder after unzipping should pull up all of the project resources and scripts. Key for the encryption of pck file is located in `godot.gdkey`.

## Solution

Clone down and use gdsdecomp to get src code from the exe file. Then change the number of pets required variable to 1 or the amount of pets gained on click to reach the number of clicks to however much the number of required pets is. 

Flag: `gigem{r3v_1s_cut3!!}`
