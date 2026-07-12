pairs = [
    (b"Chocofush's Cool Experimental Features:", b"Experimental features (off):           "),
    (b"Chocofush's cool/misc extra stuff", b"Extra features (off)             "),
]
for o, n in pairs:
    print(len(o), len(n), "OK" if len(o) == len(n) else "BAD", o, n)
