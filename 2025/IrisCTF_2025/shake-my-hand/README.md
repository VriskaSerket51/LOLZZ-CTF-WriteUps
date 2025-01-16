# Shake My Hand

## Description

## Solution

TCP 시뮬레이션 환경. 직접 TCP 패킷을 만들어서 보내야 함.

핸드셰이크랑 ACK 보내는 것만 잘 구현하면 됨.

연결 성공 시 `print flag? (yes/no)`가 출력되고 `yes`를 보내면 플래그를 보내 줌.
```python
import pwn
import scapy.all as scapy
import base64
pwn.context.log_level = 'debug'

r = pwn.remote("shake-my-hand.chal.irisc.tf", 10501)

r.recvuntil(b"Your IP: ")
my_ip = r.recvline().strip().decode()
print("MYIP", my_ip)
chall_ip = "192.168.1.10"

r.recv()
r.unrecv(b'> ')

def send_packet(p) -> bytes :
    r.recvuntil(b'> ')
    pr = base64.b64encode(scapy.raw(p))
    r.sendline(b"emit " + pr)

def recv_packet():
    r.recvuntil(b'> ')
    r.sendline(b"recv")
    r.recvuntil(b"done.\n")
    line = r.recvline().strip()
    if b'empty' in line:
        print("recv fail")
        exit()
    return scapy.IP(base64.b64decode(line))

# 1. syn
p = scapy.IP(src=my_ip, dst=chall_ip) / scapy.TCP(sport=1234,dport=9999, seq=0, flags="S")
send_packet(p)

# 2. synack
pr = recv_packet()

# 3. ack
p = scapy.IP(src=my_ip, dst=chall_ip) / scapy.TCP(sport=1234,dport=9999, seq=1, ack=pr.seq+1,flags="A")
send_packet(p)

# 4. receive data
pr = recv_packet()
print(pr.load)

# 5. ack + send yes
p = scapy.IP(src=my_ip, dst=chall_ip) / scapy.TCP(sport=1234,dport=9999, seq=1, ack=pr.seq+len(pr.load),flags="PA") / "yes\n"
send_packet(p)

# 6. get flag
pr = recv_packet()
print(pr.load.decode())
```

flag is: **irisctf{tcp_h4ndsh4k35_are_a_br33ze_1n_th3_p4rk}**