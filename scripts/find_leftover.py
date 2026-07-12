d = open(r"C:\Users\루\Projects\eaglercraft-1.12.2\eaglymc-wasm\classes.wasm", "rb").read()
i = d.find(b"EaglyMC")
print(repr(d[i - 20 : i + 40]))
