with open("hra.py", "r", encoding="utf-8") as f:
    content = f.read()

# ── 1. Přidáme import base64 za import json ──
content = content.replace(
    "import json",
    "import json\nimport base64",
    1
)

# ── 2. Přidáme funkce uloz_save a nacti_save za save_path funkci ──
save_funkce = '''
def uloz_save(data):
    json_str = json.dumps(data, ensure_ascii=False)
    zasifrovano = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
    with open(save_path("summer_fish_data"), "w", encoding="utf-8") as f:
        f.write("GAME SAVED DATA - DO NOT DELETE OR CHANGE THIS FILE\n")
        f.write(zasifrovano)

def nacti_save():
    with open(save_path("summer_fish_data"), "r", encoding="utf-8") as f:
        f.readline()  # přeskočí první řádek s textem
        zasifrovano = f.read()
    json_str = base64.b64decode(zasifrovano).decode("utf-8")
    return json.loads(json_str)
'''

content = content.replace(
    "def resource_path",
    save_funkce + "def resource_path",
    1
)

# ── 3. Nahradíme ukládání save ──
content = content.replace(
    'with open(save_path("summer_fish_data"), "w", encoding="utf-8") as f:\n                    json.dump(ziskej_data_pro_save(), f, indent=2, ensure_ascii=False)',
    'uloz_save(ziskej_data_pro_save())'
)

# ── 4. Nahradíme načítání save ──
content = content.replace(
    'with open(save_path("summer_fish_data"), "r", encoding="utf-8") as f:\n                            aplikuj_save(json.load(f))',
    'aplikuj_save(nacti_save())'
)

# ── 5. Nahradíme os.path.exists ──
content = content.replace(
    'os.path.exists(save_path("summer_fish_data"))',
    'os.path.exists(save_path("summer_fish_data"))'
)

# ── 6. Nahradíme os.remove ──
content = content.replace(
    'os.remove(save_path("summer_fish_data"))',
    'os.remove(save_path("summer_fish_data"))'
)

with open("hra.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Hotovo! hra.py upraven.")
print("   Save se teď ukládá jako 'summer_fish_data' a je zašifrovaný base64.")
