pairs = [
    ("the EaglyMC team", "Minecraft       "),
    ("           EaglyMC", "     Minecraft  "),
    ("           EaglyMC ", "    Minecraft   "),
    ("EaglyMC 1.20-u5 eventual [", "Minecraft 1.8.8           ["),
    ("           EaglyMC 1.20 u5", "     Minecraft 1.8.8      "),
    ("           EaglyMC 1.20 u5 (site origin)", "     Minecraft 1.8.8 (local)        "),
    ("EaglyMC 1.20-u5 - ", "Minecraft 1.8.8 - "),
    ("Made by the EaglyMC team", "Happy mining!           "),
    ("Minecraft 1.20.1 (kinda)", "Minecraft 1.8.8         "),
    ("eaglymc/realms/textures/title.png", "textures/gui/title/minecraft.png "),
    ("https://discord.gg/S96sKenDhV", "                               "),
    ("https://gitlab.com/lax1dude/eaglercraftx-1.8", "                                              "),
    ("Chocofush's Cool Experimental Features:", "Experimental features (disabled):      "),
    ("Chocofush's cool/misc extra stuff", "Extra features (disabled)          "),
    ("You have been given a cool Chocofush!", "You received an item!                "),
    ("Based Off EaglercraftX", "                        "),
    ("By lax1dude (u44)", "                   "),
    ("client_origin_name", "client_display_nm "),
    ("EaglyMC", "Minecrft"),
    ("1.20", "1.8 "),
    ("Discord", "       "),
    ("Connecting to services...", "                         "),
]
for o, n in pairs:
    status = "OK" if len(o) == len(n) else "BAD"
    print(f"{status} {len(o)} vs {len(n)}: {o!r}")
