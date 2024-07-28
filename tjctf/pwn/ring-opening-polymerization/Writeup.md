# TJCTF 2024

Note: out is referenced within the writeup and is provided within tjctf/rop/out. Note it is a binary file, run at own risk.
solve.py is mentioned and is provided within tjctf/rop/solve.py

## Challenge: pwn/ring-opening-polymerization

The ring-opening polymerization of cyclic esters is a powerful method for the synthesis of biodegradable polymers.

Connect to the server with nc tjc.tf 31457.

## Difficulty

108 solves / 126 points

## Solution

### Analysis

First, we need to figure out what our goal is. We open `out` in a disassembler (in my case Binary Ninja) and find the `win/1` function. Using pseudo_C as our conversion language, we get the following
```c
int64_t win(int64_t arg1)
{
    void var_78;
    fgets(&var_78, 0x23, fopen("flag.txt", &data_402004));
    printf(&data_40200f, arg1);
    int64_t rax_3;
    if (arg1 != 0xdeadbeef)
    {
        rax_3 = puts("Bad!");
    }
    else
    {
        puts(&var_78);
        rax_3 = fflush(__TMC_END__);
    }
    return rax_3;
}
```

This function checks whether the argument it takes is equal to 0xdeadbeef and if it is then it opens up flag.txt and prints the contents. This is clearly our goal, so now we need to figure out how to get it and to set its argument to 0xdeadbeef. Now we observe the main function

```c
int32_t main(int32_t argc, char** argv, char** envp)
{
    void buf;
    gets(&buf);
    return 0;
}
```

We clearly have a buffer overflow here due to the `gets` function which doesn't check for buffer size. This gives us a means to override the return address to `win/1`, but we still need to change the argument. Thankfully, ROP can help us. We need some gadget that allows us to set the `rdi` pointer since we need to modify the first argument.

Now we need to figure out where the return address is. There are many ways to do this, but if we inspect the assembly itself we see a `lea rax, [rbp-0x8 {buf}]` instruction. buf is the variable to which we can input. We know that the return address is right behind `rbp`, so to get to it, we need to overwrite 0x8 for buf + 0x8 for rbp = 0x10. With a more powerful dissasembler, we can see the allocation of the array and determine it that way or we can use gdb with gef. To use gdb with gef, we run 'pattern create', copy it, run the program and paste the string, this will overflow the return address, but you can do `pattern search $rsp` to find the offset. Regardless we know the offset is 0x10.

### Construction Solution

Given the above, I used pwntools to accomplish this. The final solution is found in `solve.py`.

Most of the script is pretty clear in what it does, and is commented to explain what is happening. The [pwntools rop documentation](https://docs.pwntools.com/en/stable/rop/rop.html) provides more information in how to do ROP with it.
