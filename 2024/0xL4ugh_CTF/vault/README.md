# Vault

Reversing the binary, then you can get the logic:

```python
f = open("flag.txt.enc", "rb")

OVER = False
data = list(f.read())
for i in range(len(data) // 10):
    block = data[i*10:(i+1)*10]
    k = bin(block[0] ^ 0x99)[2:].rjust(10, "0")[::-1]
    z = []
    o2n = []
    for j in range(1, 10):
        v = (-19 - block[j]) ^ j
        # if j is 8 or 9, we may xor it or not...
        if k[j] == "1" or (OVER and (j == 8 or j == 9)):
            v ^= 0x55
        o2n.append(chr(v & 127))
        z.append((v & 128) >> 7)
    z = "".join(map(str, z[:7][::-1]))
    z = chr(int(z, 2))
    f = [z] + o2n
    print("".join(f))
```

Then you can get two outputs, whether `OVER` is true or false:
```
...
 \  0xL4u2
h{r1se_and
_r1se_ag1
n_unt1l_l@
mbs_b3c0m0
_l1ons_ee9
9c665_0b}_
...
```
```
...
 \  0xL4 g
h{r1se_a;1
_r1se_ag@d
n_unt1l_9
mbs_b3c08e
_l1ons_e0l
9c665_0b(
...
```

We have to cherry-pick between two outputs.

> '0xL4ugh{r1se_and_r1se_ag@1n_unt1l_l@mbs_b3c0me_l1ons_e099c665_0b}'

flag is: **0xL4ugh{r1se_and_r1se_ag@1n_unt1l_l@mbs_b3c0me_l1ons_e099c665_0b}**