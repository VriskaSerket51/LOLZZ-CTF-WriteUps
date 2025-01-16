# Now this will run on my 486?

`Description`

`Solution`
직접 실행해 보면 디스어셈블리가 가능해짐.
표준 입력으로 0x20바이트를 읽는다.
먼저 모든 바이트의 합이 0xcff인지 확인한다.
```
128:    b9 00 20 00 00          mov    ecx,0x2000
130:    42 8b 04 01             mov    eax,DWORD PTR [rcx+r8*1]
138:    ba d7 b0 51 bf          mov    edx,0xbf51b0d7
140:    31 c2                   xor    edx,eax
148:    b8 be c2 38 cc          mov    eax,0xcc38c2be
150:    39 d0                   cmp    eax,edx
```
이후 앞에서 차례대로 4바이트씩 무언가(edx)와 xor하여 무언가(eax)와 같은지 확인한다.
edx에 들어갈 내용은 17 02 00 이후 4바이트씩 나오고, eax에 들어갈 내용은 17 00 00 이후 4바이트씩 나온다.
규칙성이 있는 부분을 찾아 적당히 연결하면
```
    d7b051bf7b54cc753ad80f4f447711a2c6ced0ecfaf9192ed983ea32e061ebe5
    bec238cc1820aa0e4db77810321263db99a1a0989394784286e085568540ca98
```
두 개를 XOR하면
```
     697269736374667b776f775f766572795f6f7074696d616c5f636f646521217d
```
플래그가 나옴

flag is: **irisctf{wow_very_optimal_code!!}**