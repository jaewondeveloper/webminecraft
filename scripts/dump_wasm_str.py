d = open(r"C:\Users\루\Projects\eaglercraft-1.12.2\eaglymc-wasm\classes.wasm", "rb").read()
idx = 0
while True:
    i = d.find(b"Chocofush", idx)
    if i == -1:
        break
    print(repr(d[i : i + 55]))
    idx = i + 1
