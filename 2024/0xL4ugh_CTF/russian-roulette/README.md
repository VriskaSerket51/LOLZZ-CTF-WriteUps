# Russian Roulette

APK file made with Unity.

Using il2cppdumper, you can get the flag decryptor function.

```cs
	// Token: 0x06000002 RID: 2 RVA: 0x00002052 File Offset: 0x00000252
	[Token(Token = "0x6000002")]
	[Address(RVA = "0x169FD48", Offset = "0x169ED48", VA = "0x169FD48")]
	private string GetLeadBullet(string secret)
	{
		return null;
	}
```

Look inside the address `0x169FD48` of `libil2cpp.so`, now you can get the flag decryption logic.

Converting it into python code:
```python
flag = "60,170,114,64,165,147,150,173,41,156,137,125,156,41,67,71,137,67,150,63,162,63,137,41,65,137,65,67,162,63,156,147,67,150,175"\
    .split(",")
flag = list(map(lambda v: int(v, 8), flag))
flag = bytes(flag)

print(flag)
```

> b'0xL4ugh{!n_Un!79_7h3r3_!5_57r3ng7h}'

flag is: **0xL4ugh{!n_Un!79_7h3r3_!5_57r3ng7h}**