# Capawchino Cafe

`Crypto/ECDSA`

`Phase 1: solve with AES-CTR (just xor)`
`Phase 2: find d with related nonce, r and s`

`solve with this paper's code`
[https://eprint.iacr.org/2023/305.pdf](https://eprint.iacr.org/2023/305.pdf)

`code for phase 1`
```
from pwn import *
import hashlib
import json
import os
import random

import ecdsa
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import bytes_to_long, long_to_bytes
HOST = "16537d70a669d6e0049357622eb91de3.chal.ctf.ae"
p = remote(HOST, 443, ssl=True, sni=HOST)
p.recvuntil(b'branch in ')
g = p.recvline()[:-2]
print(g)
p.recvuntil(b'Dirty plate: ')
plate = p.recvline()[:-1]
p.recvuntil(b'Cleaned plate: ')
cleaned = bytes.fromhex(p.recvline()[:-1].decode())
ctr = xor(plate,cleaned)
cheq = list()
for i in range(8):
    p.sendlineafter(b'> ', b'3')
    p.recvuntil(b'plate: ')
    plt = p.recvline()[:-1]
    p.sendlineafter(b'> ', xor(ctr,plt).hex().encode())
    p.recvuntil(b'cheque: ')
    cheq.append(p.recvline()[:-1])
print(cheq)
order = ecdsa.curves.NIST224p.order
credit = "100 EGP"
sha256 = hashlib.sha256()
sha256.update(credit.encode())
hash = bytes_to_long(sha256.digest()) % order
p.interactive()
```

`code for phase 2`
```
#!/usr/bin/env sage

from sage.all import GF, PolynomialRing
import hashlib
import ecdsa
import random

def separator():
	print("-" * 150)


#####################
# global parameters #
#####################

# choose any curve
usedcurve = ecdsa.curves.NIST224p
# usedcurve = ecdsa.curves.NIST521p
# usedcurve = ecdsa.curves.BRAINPOOLP160r1

print("Selected curve :")
print(usedcurve.name)
separator()

# the private key that will be guessed
# g = usedcurve.generator
# d = random.randint(1, usedcurve.order - 1)
# print("TYPES: ", type(g), type(d))

# pubkey = ecdsa.ecdsa.Public_key( g, g * d )
# privkey = ecdsa.ecdsa.Private_key( pubkey, d )
# print("Private key :")
# print(d)
# separator()

# N = the number of signatures to use, N >= 4
# the degree of the recurrence relation is N-3
# the number of unknown coefficients in the recurrence equation is N-2
# the degree of the final polynomial in d is 1 + Sum_(i=1)^(i=N-3)i

N = 8
assert N >= 4

############################################################
# nonces and signature generation with recurrence relation #
############################################################

# first, we randomly generate the coefficients of the recurrence relation
# a = []
# for i in range(N-2):
# 	a.append(random.randint(1, usedcurve.order - 1))

# # then, we generate the N nonces
# k = []
# # the first one is random
# k.append(random.randint(1, usedcurve.order - 1))
# # the other ones are computed with the recurrence equation
# for i in range(N-1):
# 	new_k = 0
# 	for j in range(N-2):
# 		new_k += a[j]*(k[i]**j) % usedcurve.order
# 	k.append(new_k)

# sanity check to see if we generated the parameters correctly
# print(k[1] % usedcurve.n)
# print((a[1]*k[0] + a[0]) % usedcurve.n)
# assert k[1] == ((a[1]*k[0] + a[0]) % usedcurve.n)

# then, we generate the signatures using the nonces
# h = []
# sgns = []
# for i in range(N):
# 	digest_fnc = hashlib.new("sha256")
# 	digest_fnc.update(b"recurrence test ")
# 	digest_fnc.update(i.to_bytes(1, 'big'))
# 	h.append(digest_fnc.digest())
# 	# get hash values as integers and comply with ECDSA
# 	# strangely, it seems that the ecdsa module does not take the leftmost bits of hash if hash size is bigger than curve... perahps is because i use low level functions
# 	if usedcurve.order.bit_length() < 256:
# 		h[i] = (int.from_bytes(h[i], "big") >> (256 - usedcurve.order.bit_length())) % usedcurve.order
# 	else:
# 		h[i] = int.from_bytes(h[i], "big") % usedcurve.order
# 	sgns.append(privkey.sign( h[i], k[i] ))

sgns = [{'s': 9329749591316880406221714968748461989219904339100230726529523450395, 'r': 2046368324293646044452445503183921041201432223060843378718870740025}, {'s': 25436474581744304571838411836396523068608772247220708872452930307079, 'r': 22263399028043939723508941963595399026892972093218445560022568478891}, {'s': 24607028140533273872183222173652569425988038689921121959332177078703, 'r': 22704599746992121473418243102793531595897297974956983999090667019863}, {'s': 25114759021627529990474996693646462216227453648130172712015842125733, 'r': 23008538226510582149766728607950713618207373926778706527368454068884}, {'s': 5754521323273687654722396009019368943560722548631803763674785699201, 'r': 16608193793706285783815424171893878200411535907931376647798245552370}, {'s': 17170347157209168993262575989745865266546542533150063879092551070889, 'r': 10242825728860227644466060137408595702528612442505423320865524787554}, {'s': 6452493402906666017542846737277546813755583311345238788580696518112, 'r': 9728805303690827119709302470337505442670335336234025371084629004112}, {'s': 851370973205129534834972712852401693526127359416353340831620471731, 'r': 16706230755521253829368040574827314438462111553139659856975837131466}]


# get signature parameters as arrays
s_inv = []
s = []
r = []
h = [17652096005390789500184919532088101572530464893898551787768088100952] * N
for i in range(N):
	s.append(sgns[i]['s'])
	r.append(sgns[i]['r'])
	s_inv.append(ecdsa.numbertheory.inverse_mod(s[i], usedcurve.order))


#########################################
# generating the private-key polynomial #
#########################################

# declaring stuff for manipulating polynomials with SAGE
Z = GF(usedcurve.order)
R = PolynomialRing(Z, names=('dd',))
(dd,) = R._first_ngens(1)

# the polynomial we construct will have degree 1 + Sum_(i=1)^(i=N-3)i in dd
# our task here is to compute this polynomial in a constructive way starting from the N signatures in the given list order
# the generic formula will be given in terms of differences of nonces, i.e. k_ij = k_i - k_j where i and j are the signature indexes
# each k_ij is a first-degree polynomial in dd
# this function has the goal of returning it given i and j
def k_ij_poly(i, j):
	hi = Z(h[i])
	hj = Z(h[j])
	s_invi = Z(s_inv[i])
	s_invj = Z(s_inv[j])
	ri = Z(r[i])
	rj = Z(r[j])
	poly = dd*(ri*s_invi - rj*s_invj) + hi*s_invi - hj*s_invj
	return poly

# the idea is to compute the polynomial recursively from the given degree down to 0
# the algorithm is as follows:
# for 4 signatures the second degree polynomial is:
# k_12*k_12 - k_23*k_01
# so we can compute its coefficients.
# the polynomial for N signatures has degree 1 + Sum_(i=1)^(i=N-3)i and can be derived from the one for N-1 signatures

# let's define dpoly(i, j) recursively as the dpoly of degree i starting with index j

def dpoly(n, i, j):
	if i == 0:
		return (k_ij_poly(j+1, j+2))*(k_ij_poly(j+1, j+2)) - (k_ij_poly(j+2, j+3))*(k_ij_poly(j+0, j+1))
	else:
		left = dpoly(n, i-1, j)
		for m in range(1,i+2):
			left = left*(k_ij_poly(j+m, j+i+2))
		right = dpoly(n, i-1, j+1)
		for m in range(1,i+2):
			right = right*(k_ij_poly(j, j+m))
		return (left - right)

def print_dpoly(n, i, j):
	if i == 0:
		print('(k', j+1, j+2, '*k', j+1, j+2, '-k', j+2, j+3, '*k', j+0, j+1, ')', sep='', end='')
	else:
		print('(', sep='', end='')
		print_dpoly(n, i-1, j)
		for m in range(1,i+2):
			print('*k', j+m, j+i+2, sep='', end='')
		print('-', sep='', end='')
		print_dpoly(n, i-1, j+1)
		for m in range(1,i+2):
			print('*k', j, j+m, sep='', end='')
		print(')', sep='', end='')


print("Nonces difference equation :")
print_dpoly(N-4, N-4, 0)
print(' = 0', sep='', end='')
print()
separator()

poly_target = dpoly(N-4, N-4, 0)
print("Polynomial in d :")
print(poly_target)
separator()

d_guesses = poly_target.roots()
print("Roots of the polynomial :")
print(d_guesses)
separator()

d = 20385607131491248456433973085276506604606604491282891727583085227810
print(d)
enc= '7ff5b38fbcf6dddaf6a1751a348e381df92dc97463dbe31cd773a6e3ccbf9abece24131798818a2a995af38f443459242e661376bd7dd63976361defcf9669a9'
enc = bytes.fromhex(enc)
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
sha256 = hashlib.sha256()
sha256.update(long_to_bytes(d))
key = sha256.digest()
iv = enc[:16]
enc = enc[16:]
cipher = AES.new(key, AES.MODE_CBC, iv)
print(cipher.decrypt(enc))
```

flag is: **flag{r8bTphbK8L10vsSKxG9siyU5mw74R3Sp}**
