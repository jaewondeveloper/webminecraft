olds = [
    b"Chocofush\\'s Cool Experimental Features:",
    b"Chocofush\\'s cool/misc extra stuff",
]
for old in olds:
    new_text = "Experimental features (off):" if b"Cool" in old else "Extra features (off)     "
    new = new_text.encode("utf-8")
  # pad
    if len(new) < len(old):
        new = new + b" " * (len(old) - len(new))
    elif len(new) > len(old):
        new = new[: len(old)]
    print(len(old), repr(old))
    print(len(new), repr(new))
    print()
