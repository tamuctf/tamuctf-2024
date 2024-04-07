# Forgotten Password

Author: `bit`

We discovered that this blog owner's email is `b8500763@gmail.com` through reconnaissance. We do not have access to the password of the account, how could we login regardless?

## Dev Notes

Source is provided.

## Solution

The exploit is that you can force mailing API fields to cc additional emails despite only designating one recipient using commas or semicolons.

First, we bypass the front-end email verification by using Burp Suite or even the browser developer tools where we send an HTTPS request without being verified by the actual text box, then simply add another email (the email you actually have control to) after the email that we are aware exists. This will bypass the validation that the user must be a registered user on this website.

Afterwards, you will receive the email with the flag.

Flag: `gigem{sptfy.com/Qhnv}`
