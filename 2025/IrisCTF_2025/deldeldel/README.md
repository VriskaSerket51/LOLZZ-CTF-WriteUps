# deldeldel

It is wireshark capture file. We can see the log of keyboard inputs. So extract and merge them.

```python
urb = {
        '04':'A',    '05':'B',    '06':'C',    '07':'D',
        '08':'E',    '09':'F',    '0a':'G',    '0b':'H',
        '0c':'I',    '0d':'J',    '0e':'K',    '0f':'L',
        '10':'M',    '11':'N',    '12':'O',    '13':'P',
        '14':'Q',    '15':'R',    '16':'S',    '17':'T',
        '18':'U',    '19':'V',    '1a':'W',    '1b':'X',
        '1c':'Y',    '1d':'Z',    '1e':'1',    '1f':'2',
        '20':'3',    '21':'4',    '22':'5',    '23':'6',
        '24':'7',    '25':'8',    '26':'9',    '27':'0',
        '28':'\n',   '29':'[ESC]','2a':'[del]','2a':'[tab]',
        '2c':' ',    '2d':'_',    '2e':'=',    '2f':'{',
        '30':'}',    '33':';',    '34':'"',    '3a':'[F1]',
        '4c':'[DELETE]',    '4f':'[RIGHT]',    '50':'[LEFT]'
        ,'51':'[DOWN]',     '52':'[UP]'
        }

a = open("output.txt").read().split('\n')[:-1]

r = ''

for i in range(len(a)):
    print(a[i])
    b = [a[i][j:j+2] for j in range(0, len(a[i]), 2)]
    print(b)
    if b[2] == '00':
        continue
    if b[0] == '00':
        r += urb[b[2]].lower()
    else:
        r += urb[b[2]]
print(r)
```

flag is: **irisctf{this_keylogger_is_too_hard_to_use}**