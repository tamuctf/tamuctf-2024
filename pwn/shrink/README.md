# Shrink

Author: `nhwn`

The ++ in C++ means extra security, right?

## Solution

This challenge exploits the short-string optimization that almost every modern implementation of `std::string` does. In particular, strings that are shorter than a certain threshold are stored inline on the stack; after exceeding this threshold, the contents are placed inside a buffer on the heap. More concretely, the layout of `std::string` in the provided version of libstdc++ looks something like this:

```cpp
struct string {
    uint8_t* buf;
    size_t len;
    union {
        uint8_t stack_buf[16];
        size_t capacity;
    } stack_buf_or_capacity;
};
```
Since `std::string` also stores a null terminator, the threshold of stack storage is 15 bytes (the capacity is hardcoded to 15 when the stack buffer is active). When the length exceeds 15 bytes, the contents are placed on the heap, and the first 8 bytes of the stack buffer are used for the capacity. The key observation is that this optimization is re-applied when the user calls `shrink_to_fit`; if the length is less than or equal to 15 bytes, then the contents of `buf` will be relocated to `stack_buf`.

Now, for the actual exploitation. A `win` function is provided, so the general goal is to get a stack buffer overflow with a short string, then overwrite the return address.

The `change` function in the `Username` struct takes in input of size `len`, then uses `resize` and `shrink_to_fit` to make the size of the string equal to the size of the input. However, the `len` field is not correctly tracked alongside the internal length of the `buf` field inside `Username`. Using `add_exclamation` to repeatedly increment the `len` field, we can use the `read` call to write in a large number of bytes and smash the saved return address on the stack.

In summary: 
1. Select `add_exclamation` at least 40 times, increasing the input size for the `read` call in `change`. 
2. Select `change` and set the string to a small size, which will move the string to the stack via short-string optimization. 
3. Select `change` again, then smash the return address with `win`. 
4. Select `exit`, which will trigger the final `ret` and jump to `win`. 

Flag: `gigem{https://i.redd.it/sayk4pi4ood81.png}`
