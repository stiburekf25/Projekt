import pygame
import sys
import random
pygame.init()

# PRIPRAVA HRY

def vyber_predmet(predmety, bait):
    los = random.randint(1, 100)
    
    for p in predmety[:-1]:
        realna_sance = p["sance"]
        
        if p["jmeno"] not in ("Plechovka", "Bota"):
            realna_sance += bait["sance"]
            
        if los <= realna_sance:
            return p.copy()
    else:
        return predmety[-1].copy()

def penalizace_cekani_z_hladu():
    if hlad > 70:
        return 0
    elif hlad > 50:
        return 2000
    elif hlad > 30:
        return 4000
    elif hlad > 15:
        return 5000
    else:
        return 7000

def rychlost_na_text():
    if hrac_aktualni_rychlost == hrac_rychlost:
        return "Normal"
    elif hrac_aktualni_rychlost >= hrac_rychlost * 0.75:
        return "Slow"
    elif hrac_aktualni_rychlost >= hrac_rychlost * 0.625:
        return "Very slow"
    elif hrac_aktualni_rychlost >= hrac_rychlost * 0.5:
        return "Exhausted"
    elif hrac_aktualni_rychlost >= hrac_rychlost * 0.25:
        return "Critical"
    
def penalizace_kliknuti_z_deprese():
    if deprese < 10:
        return 0
    elif deprese < 20:
        return 1
    elif deprese < 30:
        return 2
    elif deprese < 40:
        return 3
    elif deprese < 50:
        return 4
    elif deprese < 60:
        return 5
    elif deprese < 70:
        return 6
    elif deprese < 80:
        return 7
    elif deprese < 90:
        return 8
    elif deprese < 100:
        return 9
    else:
        return 10
    
    
    
    
    
    
def najdi_predmet_podle_jmena(predmety, jmeno):
    for p in predmety:
        if p["jmeno"] == jmeno:
            return p

def odeber_z_inventare(jmeno_predmetu):
    for i, p in enumerate(inventar_order):
        if p["jmeno"] == jmeno_predmetu:
            del inventar_order[i]
            break
def prodej_predmet(jmeno):
    if obsah_inventare[jmeno] <= 0:
        return 
    predmet = najdi_predmet_podle_jmena(predmety,jmeno)
    obsah_inventare[jmeno] -= 1
    coins_add = predmet["cena"]
    odeber_z_inventare(jmeno)
    return coins_add

def soucet_vsech_baits():
    return sum(bait["pocet"] for bait in baits.values())

    
okno_sirka = 800
okno_vyska = 600

hrac_pozice_x = 380
hrac_pozice_y = 315
hrac_rychlost = 4
hrac_aktualni_rychlost = 4
hrac_velikostX= 110
hrac_velikostY = 170

info_cesta_rozcestnik = 1575
info_jezero = 1570
info_shop = 920
info_dum = 190
info_vnitrek_domu = 750

kamera_x = 0



soubor = open("shop.txt", "r", encoding="utf-8")

seznam_vet = []

for radek in soubor:
    seznam_vet.append(radek[:-1])

soubor.close()



soubor_barman = open("barman.txt", "r", encoding="utf-8")

seznam_vet_barman = []

for radek in soubor_barman:
    seznam_vet_barman.append(radek[:-1])
    
soubor_barman.close()


rozliseni_okna = (okno_sirka, okno_vyska)

leva_zona = 300
prava_zona = 400

pocitadlo = 0

okno = pygame.display.set_mode(rozliseni_okna)
clock = pygame.time.Clock()
pocitadlo += 1

#BARVICKY
zluta = (205, 235, 98)
cerna = (0, 0, 0)
bila = (255, 255, 255)
seda = (94, 94, 94)
hneda = (148, 96, 56)
Shneda = (173, 112, 66)
Sseda = (158, 158, 158)
cervena = (191, 53, 21)
zelena = (29, 166, 14)
modra = (59, 64, 207)
fialova = (130, 49, 196)


#inventar
baits_mode = None
inventar = False
obsah_inventare = 0
obsah_inventare_max = 6
plny_inventar_upozorneni = False
plny_inventar_cas = 0
plny_inventar_doba = 300
sloty = []
start_slotu_x = 50
start_slotu_y = 20
slot_sirka = 115
slot_vyska = 95
mezera = 1
sloty_v_rade = 6
odemcene_sloty = 24
rady = 4
inventar_order = []

for i in range(odemcene_sloty):
    slot_x = start_slotu_x + (i % sloty_v_rade) * (slot_sirka + mezera)
    slot_y = start_slotu_y + (i // sloty_v_rade) * (slot_vyska + mezera)
    sloty.append(pygame.Rect(slot_x, slot_y, slot_sirka, slot_vyska))

odemcene_sloty = min(odemcene_sloty + 6, 24)
vylovene_predmety = []

slot = sloty[i]

#predmety
coins = 100
obsah_inventare = {
    "Plechovka":0, "Bota":0, "Kapr":0, "Štika":0, "Sumec":0, "Rak":0}

#Rybareni
posledni_ulovek = None
plus_ikona = pygame.image.load("plus_ikona.png")
posledni_ulovek_cas = 0
posledni_ulovek_doba = 2000
prut = False
zpet_tlacitko_rect = pygame.draw.rect(okno, bila, (350, 530, 100, 50))
minihra = False
zpet_tlacitko = False
predmety = [
    {
        "jmeno": "Plechovka",
        "sance": 40,
        "cekani": 4000,
        "zmacknuti": 5,
        "limit_cekani": 3000,
        "cena": 30,
        "obrazek": pygame.image.load("plechovka.png"),
    },
    {
        "jmeno": "Bota",
        "sance": 65,
        "cekani": 5000,
        "zmacknuti": 7,
        "limit_cekani": 2500,
        "cena": 50,
        "obrazek": pygame.image.load("bota.png"),
    },
    {
        "jmeno": "Kapr",
        "sance": 80,
        "cekani": 6000,
        "zmacknuti": 12,
        "limit_cekani": 2000,
        "cena": 140,
        "obrazek": pygame.image.load("kapr.png"),
    },
    {
        "jmeno": "Štika",
        "sance": 90,
        "cekani": 7000,
        "zmacknuti": 15,
        "limit_cekani": 1300,
        "cena": 280,
        "obrazek": pygame.image.load("stika.png"),
    },
    {
        "jmeno": "Sumec",
        "sance": 97,
        "cekani": 11000,
        "zmacknuti": 18,
        "limit_cekani": 1000,
        "cena": 500,
        "obrazek": pygame.image.load("sumec.png"),
    },
    {
        "jmeno": "Rak",
        "sance": 100,
        "cekani": 9000,
        "zmacknuti": 23,
        "limit_cekani": 1100,
        "cena": 1000,
        "obrazek": pygame.image.load("tajnaRyba.png"),
    },
]
        
inventar_order = []  # nejdriv prazdny seznam
for jmeno, pocet in obsah_inventare.items():
    if pocet > 0:
        predmet = najdi_predmet_podle_jmena(predmety, jmeno)
        for _ in range(pocet):
            inventar_order.append(predmet)

#velikosti
buy_velikost = 60
sell_velikost = 60
leave_velikost =  40
leave_buy_velikost = 40
leave_sell_velikost = 40
shop_hlaska = None
hlaska_velikost = 25
zpet_tlacitko_velikost = 40
space_to_fish_velikost = 60
pismeno_velikost = 40
plny_inventory_velikost = 60
cislo_u_polozky_velikost = 30
rarita_velikost = 25
popis_polozky_velikost = 30
inventory_tlacitko_velikost = 30
cislo_u_upgradu_velikost = 30
inventory_info_velikost = 20
upgrades_shop_velikost = 60
upgrades_inventory_velikost = 20
baits_shop_velikost = 60
buy_baits_velikost = 30
info_o_baits_velikost = 18
inventory_baits_tlacitko_velikost = 30
krb_leave_velikost = 40
statistika_velikost = 20
exit_bar_velikost = 40
info_barman_velikost = 30
drink_cena_velikost = 30
hlaska_barman_velikost = 26
barman_hlaska = None
exit_shop_s_jidlem_velikost = 40
jidlo_cena_velikost = 30
jidlo_jmeno_velikost = 30
jidlo_popis_velikost = 23

#pozice polozek v shopu + velikost
polozky_velikost_x = 230
polozky_velikost_y = 120

sell_plechovka_pozice_x = 100
sell_plechovka_pozice_y = 80
za_plechovka_sell = pygame.draw.rect(okno, cerna, (sell_plechovka_pozice_x - 1, sell_plechovka_pozice_y - 1, polozky_velikost_x + 2, polozky_velikost_y + 2))
plechovka_sell = pygame.draw.rect(okno, hneda, (sell_plechovka_pozice_x, sell_plechovka_pozice_y, polozky_velikost_x, polozky_velikost_y))

sell_bota_pozice_x = 100
sell_bota_pozice_y = 240
za_bota_sell = pygame.draw.rect(okno, cerna, (sell_bota_pozice_x - 1, sell_bota_pozice_y - 1, polozky_velikost_x + 2, polozky_velikost_y + 2))
bota_sell = pygame.draw.rect(okno, hneda, (sell_bota_pozice_x, sell_bota_pozice_y, polozky_velikost_x, polozky_velikost_y))

sell_kapr_pozice_x = 100
sell_kapr_pozice_y = 400
za_kapr_sell = pygame.draw.rect(okno, cerna, (sell_kapr_pozice_x - 1, sell_kapr_pozice_y - 1, polozky_velikost_x + 2, polozky_velikost_y + 2))
kapr_sell = pygame.draw.rect(okno, hneda, (sell_kapr_pozice_x, sell_kapr_pozice_y, polozky_velikost_x, polozky_velikost_y))

sell_stika_pozice_x = 470
sell_stika_pozice_y = 80
za_stika_sell = pygame.draw.rect(okno, cerna, (sell_stika_pozice_x - 1, sell_stika_pozice_y - 1, polozky_velikost_x + 2, polozky_velikost_y + 2))
stika_sell = pygame.draw.rect(okno, hneda, (sell_stika_pozice_x, sell_stika_pozice_y, polozky_velikost_x, polozky_velikost_y))

sell_sumec_pozice_x = 470
sell_sumec_pozice_y = 240
za_sumec_sell = pygame.draw.rect(okno, cerna, (sell_sumec_pozice_x - 1, sell_sumec_pozice_y - 1, polozky_velikost_x + 2, polozky_velikost_y + 2))
sumec_sell = pygame.draw.rect(okno, hneda, (sell_sumec_pozice_x, sell_sumec_pozice_y, polozky_velikost_x, polozky_velikost_y))

sell_tajnaRyba_pozice_x = 470
sell_tajnaRyba_pozice_y = 400
za_tajnaRyba_sell = pygame.draw.rect(okno, cerna, (sell_tajnaRyba_pozice_x - 1, sell_tajnaRyba_pozice_y - 1, polozky_velikost_x + 2, polozky_velikost_y + 2))
tajnaRyba_sell = pygame.draw.rect(okno, hneda, (sell_tajnaRyba_pozice_x, sell_tajnaRyba_pozice_y, polozky_velikost_x, polozky_velikost_y))

upgrady_velikost_x = 170
upgrady_velikost_y = 150

kyblik_buy_pozice_x = 100
kyblik_buy_pozice_y = 80
za_kyblik_buy = pygame.draw.rect(okno, hneda, (kyblik_buy_pozice_x - 1, kyblik_buy_pozice_y - 1, upgrady_velikost_x + 2, upgrady_velikost_y + 2))
kyblik_buy = pygame.draw.rect(okno, hneda, (kyblik_buy_pozice_x, kyblik_buy_pozice_y, upgrady_velikost_x, upgrady_velikost_y))
kyblik_cena = 3000
kyblik_buy_ikona = pygame.image.load("buy_kyblik.png")

zmacknuti_buy_pozice_x = 315
zmacknuti_buy_pozice_y = 80
za_zmacknuti_buy = pygame.draw.rect(okno, cerna, (zmacknuti_buy_pozice_x - 1, zmacknuti_buy_pozice_y - 1, upgrady_velikost_x + 2, upgrady_velikost_y + 2))
zmacknuti_buy = pygame.draw.rect(okno, hneda, (zmacknuti_buy_pozice_x, zmacknuti_buy_pozice_y, upgrady_velikost_x, upgrady_velikost_y))
zmacknuti_cena = 700
zmacknuti_buy_ikona = pygame.image.load("buy_zmacknuti.png")

cekani_buy_pozice_x = 530
cekani_buy_pozice_y = 80
za_cekani_buy = pygame.draw.rect(okno, cerna, (cekani_buy_pozice_x -1, cekani_buy_pozice_y -1, upgrady_velikost_x +2, upgrady_velikost_y +2))
cekani_buy = pygame.draw.rect(okno, hneda, (cekani_buy_pozice_x, cekani_buy_pozice_y, upgrady_velikost_x, upgrady_velikost_y))
cekani_cena = 200
cekani_buy_ikona = pygame.image.load("buy_cekani.png")

def vykresli_popis_baitu(bait_data, x, y):
    for i, (klic, text) in enumerate(bait_popisy):
        hodnota = bait_data[klic]
        
        if klic == "cekani":
            sekundy = hodnota / 1000
            
            if sekundy > 0:
                hodnota = f"+{sekundy:.1f}s"
            elif sekundy < 0:
                hodnota = f"{sekundy:.1f}s"
                
        elif klic == "sance":
            if hodnota > 0:
                hodnota = f"+{hodnota}"
        else:
            hodnota = str(hodnota) 
        
        surface = info_o_baits_font.render(
            f"{text}: {hodnota}", True, cerna
        )

        okno.blit(surface, (x - 3, y + 40 +i * 20))


baits = {
    "bread": {
        "pocet":0,
        "sance":-5, #horsi
        "cekani": +500, #horsi
        "zmacknuti": 0,     #normal  
    },
    "worm": {
        "pocet":0,
        "sance":+5, #lepsi
        "cekani":-200, # lepsi
        "zmacknuti": 0, #normal   
    },
    "corn": {
        "pocet":0,
        "sance":+5,
        "cekani": +500, # horsi
        "zmacknuti": -1,  # lepsi
        
    },
    "fish_head": {
        "pocet":0,
        "sance": +10, # lepsi
        "cekani": -1000, # lepsi
        "zmacknuti": -2, # lepsi
    },

}

#BAITS
baits_pozadi_velikost_x = 640
baits_pozadi_velikost_y = 225

baits_pozadi_pozice_x = 80
baits_pozadi_pozice_y = 290
za_baits_pozadi = pygame.draw.rect(okno, cerna, (baits_pozadi_pozice_x - 1, baits_pozadi_pozice_y - 1, baits_pozadi_velikost_x + 2, baits_pozadi_velikost_y + 2))
baits_pozadi = pygame.draw.rect(okno, hneda, (baits_pozadi_pozice_x, baits_pozadi_pozice_y, baits_pozadi_velikost_x, baits_pozadi_velikost_y))

baits_okenko_velikost_x = 100
baits_okenko_velikost_y = 205

bread_bait_pozice_x = 100 
bread_bait_pozice_y = 300
za_bread_bait = pygame.draw.rect(okno, cerna, (bread_bait_pozice_x -1, bread_bait_pozice_y -1, baits_okenko_velikost_x + 2, baits_okenko_velikost_y +2))
bread_bait = pygame.draw.rect(okno, hneda, (bread_bait_pozice_x, bread_bait_pozice_y, baits_okenko_velikost_x, baits_okenko_velikost_y))
bread_bait_cena = 20
bread_bait_ikona = pygame.image.load("bread_bait_ikona.png")

worm_bait_pozice_x = 220
worm_bait_pozice_y = 300
za_worm_bait = pygame.draw.rect(okno, cerna, (worm_bait_pozice_x - 1, worm_bait_pozice_y - 1, baits_okenko_velikost_x + 2, baits_okenko_velikost_y + 2))
worm_bait = pygame.draw.rect(okno, hneda, (worm_bait_pozice_x, worm_bait_pozice_y, baits_okenko_velikost_x, baits_okenko_velikost_y))
worm_bait_cena = 40
worm_bait_ikona = pygame.image.load("worm_bait_ikona.png")

baits_upgrade_pozice_x = 340
baits_upgrade_pozice_y = 300
za_baits_upgrade = pygame.draw.rect(okno, cerna, (baits_upgrade_pozice_x - 1, baits_upgrade_pozice_y - 1, baits_okenko_velikost_x + 22, baits_okenko_velikost_y + 2))
baits_upgrade = pygame.draw.rect(okno, hneda, (baits_upgrade_pozice_x, baits_upgrade_pozice_y, baits_okenko_velikost_x +20, baits_okenko_velikost_y))
baits_upgrade_cena = 200
baits_upgrade_ikona = pygame.image.load("baits_upgrade_ikona.png")

corn_bait_pozice_x = 480
corn_bait_pozice_y = 300
za_corn_bait = pygame.draw.rect(okno, cerna, (corn_bait_pozice_x - 1, corn_bait_pozice_y - 1, baits_okenko_velikost_x + 2, baits_okenko_velikost_y + 2))
corn_bait = pygame.draw.rect(okno, hneda, (corn_bait_pozice_x, corn_bait_pozice_y, baits_okenko_velikost_x, baits_okenko_velikost_y))
corn_bait_cena = 45
corn_bait_ikona = pygame.image.load("corn_bait_ikona.png")

fish_head_bait_pozice_x = 600
fish_head_bait_pozice_y = 300
za_fish_head_bait =pygame.draw.rect(okno, cerna, (fish_head_bait_pozice_x - 1, fish_head_bait_pozice_y - 1, baits_okenko_velikost_x + 2, baits_okenko_velikost_y + 2))
fish_head_bait = pygame.draw.rect(okno, hneda, (fish_head_bait_pozice_x, fish_head_bait_pozice_y, baits_okenko_velikost_x, baits_okenko_velikost_y))
fish_head_bait_cena = 100
fish_head_bait_ikona = pygame.image.load("fish_head_bait.png")

baits_lvl = 0
max_upgrade_baits = 5
obsah_baits_max = 4

bait_ui = [
    ("bread", bread_bait_pozice_x, bread_bait_pozice_y),
    ("worm", worm_bait_pozice_x, worm_bait_pozice_y),
    ("corn", corn_bait_pozice_x, corn_bait_pozice_y),
    ("fish_head", fish_head_bait_pozice_x, fish_head_bait_pozice_y),
]

bait_ui_inv = [
    ("bread", 505, 420),
    ("worm", 565, 420),
    ("corn", 625, 420),
    ("fish_head", 685, 420),
]

bait_popisy = [
    ("sance", "Luck"),
    ("cekani", "Wait time"),
    ("zmacknuti", "presses"),
]



#inv baits ctverecky a obrazky baitu
za_bread_tlacitko_inventory =pygame.draw.rect(okno, cerna,(514, 484, inventory_baits_tlacitko_velikost + 2, inventory_baits_tlacitko_velikost + 2)) 
bread_tlacitko_inventory =pygame.draw.rect(okno, zelena,(515, 485, inventory_baits_tlacitko_velikost, inventory_baits_tlacitko_velikost))

za_worm_tlacitko_inventory =pygame.draw.rect(okno, cerna,(574, 484, inventory_baits_tlacitko_velikost + 2, inventory_baits_tlacitko_velikost + 2)) 
worm_tlacitko_inventory =pygame.draw.rect(okno, zelena,(575, 485, inventory_baits_tlacitko_velikost, inventory_baits_tlacitko_velikost))

za_corn_tlacitko_inventory =pygame.draw.rect(okno, cerna,(634, 484, inventory_baits_tlacitko_velikost + 2, inventory_baits_tlacitko_velikost + 2)) 
corn_tlacitko_inventory =pygame.draw.rect(okno, zelena,(635, 485, inventory_baits_tlacitko_velikost, inventory_baits_tlacitko_velikost))

za_fish_head_tlacitko_inventory =pygame.draw.rect(okno, cerna,(694, 484, inventory_baits_tlacitko_velikost + 2, inventory_baits_tlacitko_velikost + 2)) 
fish_head_tlacitko_inventory =pygame.draw.rect(okno, zelena,(695, 485, inventory_baits_tlacitko_velikost, inventory_baits_tlacitko_velikost))

za_bait_leave_tlacitko_inventory =pygame.draw.rect(okno, cerna,(694, 524, inventory_baits_tlacitko_velikost + 2, inventory_baits_tlacitko_velikost + 2)) 
bait_leave_tlacitko_inventory =pygame.draw.rect(okno, cervena,(695, 525, inventory_baits_tlacitko_velikost, inventory_baits_tlacitko_velikost))





fish_head_inventory_ikona = pygame.image.load("fish_head_inventory_ikona.png")
corn_inventory_ikona = pygame.image.load("corn_inventory_ikona.png")
bread_inventory_ikona = pygame.image.load("bread_inventory_ikona.png")
worm_inventory_ikona = pygame.image.load("worm_inventory_ikona.png")



#kolikrat koupeno
kyblik_lvl = 0
zmacknuti_lvl = 0
cekani_lvl = 0

max_upgrade_kybliku = 3
max_upgrade_zmacknuti = 6
max_upgrade_cekani = 8

momentalni_cekani = 0

sell_items = [
    (plechovka_sell, "Plechovka"),
    (bota_sell, "Bota"),
    (kapr_sell, "Kapr"),
    (stika_sell, "Štika"),
    (sumec_sell, "Sumec"),
    (tajnaRyba_sell, "Rak"),
]


za_koupit = pygame.draw.rect(okno, (cerna), (124, 394, 202, 102))
za_prodat = pygame.draw.rect(okno, (cerna), (474, 394, 202, 102))
za_opustit = pygame.draw.rect(okno, (cerna), (669, 534, 102, 52))
za_opustit_buy = pygame.draw.rect(okno, (cerna), (39, 534, 102, 52))
za_opustit_sell = pygame.draw.rect(okno, (cerna), (39, 534, 102, 52))


buy = pygame.draw.rect(okno, (hneda), (125, 395, 200, 100))
sell = pygame.draw.rect(okno, (hneda), (475, 395, 200, 100))
leave = pygame.draw.rect(okno, (hneda), (670, 535, 100, 50))
leave_buy = pygame.draw.rect(okno, (cerna), (40, 535, 100, 50))
leave_sell = pygame.draw.rect(okno, (cerna), (40, 535, 100, 50))
shop_mode = None # nic / buy / sell

# obrazky levelu
rozcestnik = pygame.image.load("rozcestnik.png")
venek = pygame.image.load("venek.png")
jezero = pygame.image.load("level_2.png")
shop = pygame.image.load("shop.png")
pozadi_shop = pygame.image.load("pozadi_shop.png")
pozadi_shop_jidlo = pygame.image.load("pozadi_shop_jidlo.png")
rybareni = pygame.image.load("rybareni.png")
ikona_prut = pygame.image.load("ikona_prut.png")
rybareni_dole = pygame.image.load("rybareni_dole.png")
rybareni_pozor = pygame.image.load("rybareni_pozor.png")
dum = pygame.image.load("dum.png")
krb = pygame.image.load("krb.png")

bar = pygame.image.load("bar.png")
za_bar_exit = pygame.draw.rect(okno, cerna, (19, 529 , 102, 52))
bar_exit = pygame.draw.rect(okno, hneda, (20, 530 , 100, 50))

zidle_bar = pygame.image.load("zidle_bar.png")
zidle_bar_rect = zidle_bar.get_rect(bottomright=(699, 380))

slot_bar = pygame.image.load("slot.png")
slot_bar_rect = slot_bar.get_rect(topleft=(70, 180))

barman = pygame.image.load("barman.png")
za_barman_exit = pygame.draw.rect(okno, cerna, (9, 544 , 102, 52))
barman_exit = pygame.draw.rect(okno, hneda, (10, 545 , 100, 50))

slotmachine = pygame.image.load("slotmachine.png")
garaz = pygame.image.load("garaz.png")
bouda = pygame.image.load("bouda.png")


pozadi = rozcestnik

pozadi_sirka = pozadi.get_width()
pozadi_vyska = pozadi.get_height()

#obrazky pepy
postava = pygame.image.load("pepa.png")
TEXTURApostava = pygame.transform.scale(postava, (hrac_velikostX, hrac_velikostY))

pepa1 = pygame.image.load("pepa_pravo.png")
TEXTURApepa1 = pygame.transform.scale(pepa1, (hrac_velikostX, hrac_velikostY))

pepa2 = pygame.image.load("pepa_pravo_2.png")
TEXTURApepa2 = pygame.transform.scale(pepa2, (hrac_velikostX, hrac_velikostY))


pepa_1 = pygame.image.load("pepa_levo.png")
TEXTURApepa_1 = pygame.transform.scale(pepa_1, (hrac_velikostX, hrac_velikostY))

pepa_2 = pygame.image.load("pepa_levo_2.png")
TEXTURApepa_2 = pygame.transform.scale(pepa_2, (hrac_velikostX, hrac_velikostY))

pepa_lod = pygame.image.load("pepa_beznohy.png")
TEXTURApepa_lod = pygame.transform.scale(pepa_lod, (hrac_velikostX, hrac_velikostY))

pepa_1_lod = pygame.image.load("pepa_beznohy_levo.png")
TEXTURApepa_1_lod = pygame.transform.scale(pepa_1_lod, (hrac_velikostX, hrac_velikostY))

pepa_2_lod = pygame.image.load("pepa_beznohy_pravo.png")
TEXTURApepa_2_lod = pygame.transform.scale(pepa_2_lod, (hrac_velikostX, hrac_velikostY))

#obrazek inv
inv = pygame.image.load("inventar.png")
inv2 = pygame.image.load("inventar_2.png")
inv3 = pygame.image.load("inventar_3.png")
inv4 = pygame.image.load("inventar_4.png")
ikona_inv = pygame.image.load("ikona_inv.png") # x 70 y 80
ikona_inv_rect = ikona_inv.get_rect(topleft=(700, 20))
tlacitko = pygame.draw.rect(okno, Sseda, (413 - inventory_tlacitko_velikost, 517 ,inventory_tlacitko_velikost, inventory_tlacitko_velikost))
za_tlacitko = pygame.draw.rect(okno, seda, (412 - inventory_tlacitko_velikost, 516, inventory_tlacitko_velikost, inventory_tlacitko_velikost))



#obrazky shopu
plechovka = pygame.image.load("plechovka.png")
bota = pygame.image.load("bota.png")
kapr = pygame.image.load("kapr.png")
stika = pygame.image.load("stika.png")
sumec = pygame.image.load("sumec.png")
tajnaRyba = pygame.image.load("tajnaRyba.png")

coin_ikona = pygame.image.load("coin_ikon.png")

#priprava textu
E_font = pygame.font.SysFont("Aharoni", 40)
E_text = E_font.render("E", True, (cerna))
za_e_u_jezera = pygame.draw.rect(okno, (cerna), (721, 339, 52, 52))
za_space_u_jezera = pygame.draw.rect(okno, cerna, (721, 339, 52, 52))


coins_font = pygame.font.Font("CHAOS16.otf", 30)
buy_font = pygame.font.SysFont("Aharoni", buy_velikost)
buy_text = buy_font.render("BUY", True, (cerna))
sell_font = pygame.font.SysFont("Aharoni", sell_velikost)
sell_text = sell_font.render("SELL", True, cerna)
leave_font = pygame.font.SysFont("Aharoni", leave_velikost)
leave_text = leave_font.render("EXIT", True, cerna)
leave_buy_font = pygame.font.SysFont("Aharoni", leave_buy_velikost)
leave_buy_text = leave_buy_font.render("EXIT", True, cerna)
leave_sell_font = pygame.font.SysFont("Aharoni", leave_sell_velikost)
leave_sell_text = leave_sell_font.render("EXIT", True, cerna)
zpet_tlacitko_font = pygame.font.SysFont("Aharoni", zpet_tlacitko_velikost)
zpet_tlacitko_text = zpet_tlacitko_font.render("EXIT", True, cerna)
pismeno_font = pygame.font.SysFont("Aharoni", pismeno_velikost)
plny_inv_font = pygame.font.SysFont("Aharoni", plny_inventory_velikost)
plny_inv_text = plny_inv_font.render("!!FULL INVENTORY!!", True, cervena)
cislo_u_polozky_font = pygame.font.SysFont("Aharoni", cislo_u_polozky_velikost)
rarita_font = pygame.font.SysFont("Aharoni", rarita_velikost)
popis_polozky_font = pygame.font.SysFont("Aharoni", popis_polozky_velikost)
hodnota_polozky_font = pygame.font.Font("CHAOS16.otf", 30)
space_to_fish_font = pygame.font.SysFont("Aharoni", space_to_fish_velikost)
space_to_fish_text = space_to_fish_font.render("PRESS SPACE TO CAST", True, cerna)
pocet_upgradu_font = pygame.font.SysFont("Aharoni", cislo_u_upgradu_velikost)
coins_cena_buy_font = pygame.font.Font("CHAOS16.otf",  30)
inventory_info_font = pygame.font.SysFont("Aharoni", inventory_info_velikost)
upgrades_shop_font = pygame.font.SysFont("Aharoni", upgrades_shop_velikost)
upgrades_inventory_font = pygame.font.SysFont("Aharoni", upgrades_inventory_velikost)
baits_shop_font = pygame.font.SysFont("Aharoni", baits_shop_velikost)
buy_baits_cena_font = pygame.font.Font("CHAOS16.otf", buy_baits_velikost)
info_o_baits_font = pygame.font.SysFont("Aharoni", info_o_baits_velikost)
krb_leave_font = pygame.font.SysFont("Aharoni", krb_leave_velikost)
statistika_font = pygame.font.SysFont("Aharoni", statistika_velikost)
exit_bar_font = pygame.font.SysFont("Aharoni", exit_bar_velikost)
info_barman_font = pygame.font.SysFont("Aharoni", info_barman_velikost)
drink_cena_font = pygame.font.Font("CHAOS16.otf", drink_cena_velikost)
exit_shop_s_jidlem_font = pygame.font.SysFont("Aharoni", exit_shop_s_jidlem_velikost)
jidlo_cena_font = pygame.font.Font("CHAOS16.otf", jidlo_cena_velikost)
jidlo_jmeno_font = pygame.font.SysFont("Aharoni", jidlo_jmeno_velikost)
jidlo_popis_font = pygame.font.SysFont("Aharoni", jidlo_popis_velikost)
napis_hry_font = pygame.font.Font("hra_napis.otf", 140)
za_napis_hry_font = pygame.font.Font("hra_napis.otf", 139)


hlaska_font = pygame.font.SysFont("Aharoni", hlaska_velikost)
shop_hlaska = random.choice(seznam_vet)
hlaska_text = hlaska_font.render(shop_hlaska, True, cerna)

hlaska_barman_font = pygame.font.SysFont("Aharoni", hlaska_barman_velikost)
barman_hlaska = random.choice(seznam_vet_barman)
hlaska_barman_text = hlaska_barman_font.render(barman_hlaska, True, cerna)

prechod_lock_venek_a_rozcestnik = False
prechod_lock_venek_a_jezero = False
prechod_lock_dum_a_venek = False
prechod_lock_dum_a_krb = False
prechod_lock_garaz_a_rozcestnik = False


# CYKLICKE VYKRESLOVANI FRAMU HRY

zizen = 100
hlad = 100
deprese = 0

hlad_flag_60 = False
hlad_flag_40 = False
hlad_flag_30 = False
hlad_flag_20 = False
hlad_flag_0 = False

zizen_flag_60 = False
zizen_flag_40 = False
zizen_flag_30 = False
zizen_flag_20 = False
zizen_flag_0 = False

hlad_ikona = pygame.image.load("hlad.png")
zizen_ikona = pygame.image.load("zizen.png")
deprese_ikona = pygame.image.load("deprese.png")

za_zapnuti_statistik = pygame.draw.rect(okno, cerna, (359, 564, 82, 32))
zapnuti_statistik = pygame.draw.rect(okno, hneda, (360, 565, 80, 30))
zapnuti_statistik_ikona = pygame.image.load("zapnuti.png")
zapnuti = False

za_vypnuti_statistik = pygame.draw.rect(okno, cerna, (359, 4, 82, 32))
vypnuti_statistik = pygame.draw.rect(okno, hneda, (360, 5, 80, 30))
vypnuti_statistik_ikona = pygame.image.load("vypnuti.png")

zapnuti_statistik_rybareni = pygame.draw.rect(okno, hneda, (5, 565, 80, 30))


#BAR SHOP
bar_polozky_velikost_x = 120
bar_polozky_velikost_y = 158

za_voda_buy = pygame.draw.rect(okno, cerna, (67, 379, bar_polozky_velikost_x + 2, bar_polozky_velikost_y + 2))
voda_buy = pygame.draw.rect(okno, hneda, (68, 380, bar_polozky_velikost_x, bar_polozky_velikost_y))

za_dzus_buy = pygame.draw.rect(okno, cerna, (245, 379, bar_polozky_velikost_x + 2, bar_polozky_velikost_y + 2))
dzus_buy = pygame.draw.rect(okno, hneda, (246, 380, bar_polozky_velikost_x, bar_polozky_velikost_y))

za_cola_buy = pygame.draw.rect(okno, cerna, (423, 379, bar_polozky_velikost_x + 2, bar_polozky_velikost_y + 2))
cola_buy = pygame.draw.rect(okno, hneda, (424, 380, bar_polozky_velikost_x, bar_polozky_velikost_y))

za_pivo_buy = pygame.draw.rect(okno, cerna, (601, 379, bar_polozky_velikost_x + 2, bar_polozky_velikost_y + 2))
pivo_buy = pygame.draw.rect(okno, hneda, (602, 380, bar_polozky_velikost_x, bar_polozky_velikost_y))

voda_cena = 15
dzus_cena = 30
cola_cena = 50
pivo_cena = 75

zizen_voda = 20
hlad_voda = 0

zizen_dzus = 40
hlad_dzus = 0

zizen_cola = 40
hlad_cola = 10

zizen_pivo = 100
hlad_pivo = 20

voda = pygame.image.load("voda.png")
dzus = pygame.image.load("dzus.png")
cola = pygame.image.load("cola.png")
pivo = pygame.image.load("pivo.png")

hra = False 
ikona_prut_menu = pygame.image.load("ikona_prut_menu.png")

play_tlacitko = pygame.image.load("play_tlacitko.png")
play_tlacitko_rect = play_tlacitko.get_rect(center=(400, 280))

play_tlacitko_vetsi = pygame.image.load("play_tlacitko_vetsi.png")
play_tlacitko_vetsi_rect = play_tlacitko.get_rect(center=(395, 275))

quit_tlacitko = pygame.image.load("quit_tlacitko.png")
quit_tlacitko_rect = quit_tlacitko.get_rect(center=(30, 570))

quit_tlacitko_vetsi = pygame.image.load("quit_tlacitko_vetsi.png")
quit_tlacitko_vetsi_rect = quit_tlacitko_vetsi.get_rect(center=(30, 570))

#Animace
MN = [pygame.image.load(f"{i}.png") for i in range(1, 51)]

while not hra:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if udalost.type == pygame.MOUSEBUTTONDOWN and udalost.button == 1:
            mys_pozice = pygame.mouse.get_pos()
            
            if play_tlacitko_rect.collidepoint(mys_pozice):
                hra = True
            
            if quit_tlacitko_rect.collidepoint(mys_pozice):
                pygame.quit()
                sys.exit()
    kurzor_hand = False
    mys_pozice = pygame.mouse.get_pos()
    
    pocitadlo += 1

                
    if not hra and play_tlacitko_rect.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif not hra and quit_tlacitko_rect.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    if not hra:
        pocet_snimku = 50
        faktor_zpozdeni = 2
        
        index = int(pocitadlo / faktor_zpozdeni) % pocet_snimku  # ← Pozor: / místo //
        okno.blit(MN[index], (0, 0))        
        
        
        
        
        
        
        if not play_tlacitko_rect.collidepoint(mys_pozice):
            okno.blit(play_tlacitko, play_tlacitko_rect)
        else:
            okno.blit(play_tlacitko_vetsi, play_tlacitko_vetsi_rect)
        
        if not quit_tlacitko_rect.collidepoint(mys_pozice):
            okno.blit(quit_tlacitko, quit_tlacitko_rect)
        else:
            okno.blit(quit_tlacitko_vetsi, quit_tlacitko_vetsi_rect)
            
        summer_text = napis_hry_font.render("SUMMER", True, cerna)
        okno.blit(summer_text, ( 210, 1))
        za_summer_text = za_napis_hry_font.render("SUMMER", True, bila)
        okno.blit(za_summer_text, ( 210, 5))
        fish_text = napis_hry_font.render("F   SH", True, cerna)
        okno.blit(fish_text, (280, 90))
        za_fish_text = za_napis_hry_font.render("F   SH", True, bila)
        okno.blit(za_fish_text, (280, 95))
        okno.blit(ikona_prut_menu, (270, 60))
        
    clock.tick(60)
    pygame.display.flip()
    










while hra is True:
    print(hrac_pozice_x)
# OVLADANI HRY HRACEM
    mouse_click = False
    
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if udalost.type == pygame.MOUSEBUTTONDOWN and udalost.button == 1:
            mouse_click = True
    
    hrac_obrazovka_x = hrac_pozice_x - kamera_x
    
    stisknuto = pygame.key.get_pressed()
    mys_pozice = pygame.mouse.get_pos()

    
    

    if pozadi != krb:
        # Postupné snižování hladu a žízně
        hlad = max(0, hlad - 0.002)
        zizen = max(0, zizen - 0.002)

    if hlad < 60 and not hlad_flag_60:
            deprese += 5
            hlad_flag_60 = True
    if hlad < 40 and not hlad_flag_40:
        deprese += 5
        hlad_flag_40 = True
    if hlad < 30 and not hlad_flag_30:
        deprese += 10
        hlad_flag_30 = True
    if hlad < 20 and not hlad_flag_20:
        deprese += 15
        hlad_flag_20 = True
    if hlad == 0 and not hlad_flag_0:
        deprese += 25
        hlad_flag_0 = True
    
    if zizen < 60 and not zizen_flag_60:
        deprese += 5
        zizen_flag_60 = True
    if zizen < 40 and not zizen_flag_40:
        deprese += 5
        zizen_flag_40 = True
    if zizen < 30 and not zizen_flag_30:
        deprese += 10
        zizen_flag_30 = True
    if zizen < 20 and not zizen_flag_20:
        deprese += 15
        zizen_flag_20 = True
    if zizen == 0 and not zizen_flag_0:
        deprese += 25
        zizen_flag_0 = True
    
    if hlad >= 60:
        hlad_flag_60 = False
    if hlad >= 40:
        hlad_flag_40 = False
    if hlad >= 30:
        hlad_flag_30 = False
    if hlad >= 20:
        hlad_flag_20 = False
    if hlad > 0:
        hlad_flag_0 = False
    
    if zizen >= 60:
        zizen_flag_60 = False
    if zizen >= 40:
        zizen_flag_40 = False
    if zizen >= 30:
        zizen_flag_30 = False
    if zizen >= 20:
        zizen_flag_20 = False
    if zizen > 0:
        zizen_flag_0 = False
    
    hlad = min(100, max(0, hlad))
    zizen = min(100, max(0, zizen))
    deprese = min(100, max(0, deprese))
    
    if zizen > 70:
        hrac_aktualni_rychlost = hrac_rychlost
    elif zizen > 50:
        hrac_aktualni_rychlost = hrac_rychlost * 0.75
    elif zizen > 30:
        hrac_aktualni_rychlost = hrac_rychlost * 0.625
    elif zizen > 15:
        hrac_aktualni_rychlost = hrac_rychlost * 0.5
    else:
        hrac_aktualni_rychlost = hrac_rychlost * 0.25
            
    if pozadi == rybareni and zapnuti_statistik_rybareni.collidepoint(mys_pozice) and mouse_click and not zapnuti and not inventar and pozadi != bar and pozadi != barman and pozadi != shop and not shop_mode == "sell" and not shop_mode == "buy" and not prut and not minihra and pozadi != pozadi_shop_jidlo:
        zapnuti = True

    elif not zapnuti and zapnuti_statistik.collidepoint(mys_pozice) and mouse_click and not inventar and pozadi != bar and pozadi != barman and pozadi != shop and not shop_mode == "sell" and not shop_mode == "buy" and pozadi != rybareni and not prut and not minihra and pozadi != pozadi_shop_jidlo:
        zapnuti = True
        
    if zapnuti and vypnuti_statistik.collidepoint(mys_pozice) and mouse_click and not inventar and pozadi != bar and pozadi != barman and pozadi != shop and not shop_mode == "sell" and not shop_mode == "buy" and pozadi != pozadi_shop_jidlo:
        zapnuti = False

    
    # UPRAVA HRY MEZI FRAMY
    
    pocitadlo += 1
    aktualni_sprite = TEXTURApostava
    pocet_snimku = 2
    faktor_zpozdeni = 8
    
    #animace pepy pri chuzi
    
    
    if stisknuto[pygame.K_d]:
        if pocitadlo % (pocet_snimku * faktor_zpozdeni) < faktor_zpozdeni:
            aktualni_sprite = TEXTURApepa1

        else:
            aktualni_sprite = TEXTURApepa2
        hrac_pozice_x += hrac_aktualni_rychlost

    elif stisknuto[pygame.K_a]:
        if pocitadlo % (pocet_snimku * faktor_zpozdeni) < faktor_zpozdeni:
            aktualni_sprite = TEXTURApepa_1

        else:
            aktualni_sprite = TEXTURApepa_2
        hrac_pozice_x -= hrac_aktualni_rychlost
        
        
    # ROZCESTNIK
    if pozadi == rozcestnik:
        if hrac_pozice_x < 250:
            hrac_pozice_x = 250
        if hrac_pozice_x > pozadi_sirka - hrac_velikostX - 118 :
            hrac_pozice_x = pozadi_sirka - hrac_velikostX - 118
            
        if hrac_obrazovka_x > prava_zona:
            kamera_x += hrac_aktualni_rychlost
        if hrac_obrazovka_x < leva_zona:
            kamera_x -= hrac_aktualni_rychlost
            
        if kamera_x < 0:
            kamera_x = 0
        if kamera_x > pozadi_sirka - okno_sirka:
            kamera_x = pozadi_sirka - okno_sirka
        
        stojim_u_cesty_rozcestnik = hrac_pozice_x > 1360 and hrac_pozice_x < 1500
        
        info_rozcestnik_obrazovka_x = info_cesta_rozcestnik - kamera_x
        
        if stojim_u_cesty_rozcestnik and stisknuto[pygame.K_e] and not inventar and not prechod_lock_venek_a_rozcestnik:
            pozadi = venek
            prechod_lock_venek_a_rozcestnik = True
            hrac_pozice_x = 340
            kamera_x = 0
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
            hrac_rychlost = 4
            
        if not stojim_u_cesty_rozcestnik:
            prechod_lock_venek_a_rozcestnik = False
        
        stojim_u_baru = hrac_pozice_x > 890 and hrac_pozice_x < 1130
        
        if stojim_u_baru and stisknuto[pygame.K_e] and not inventar:
            pozadi = bar
            hrac_pozice_x = 0
            kamera_x = 0
            hrac_rychlost = 0
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
        
        stojim_u_auta = hrac_pozice_x > 249 and hrac_pozice_x < 320
        
        if stojim_u_auta and stisknuto[pygame.K_e] and not inventar:
            pass
        
        stojim_u_cesty_mezi_bar_a_auto = hrac_pozice_x > 515 and hrac_pozice_x < 770
        
        if stojim_u_cesty_mezi_bar_a_auto and stisknuto[pygame.K_e] and not inventar and not prechod_lock_garaz_a_rozcestnik:
            pozadi = garaz
            prechod_lock_garaz_a_rozcestnik = True
            hrac_pozice_x = 160
            kamera_x = 0
            hrac_rychlost = 4
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
        
        if not stojim_u_cesty_mezi_bar_a_auto:
            prechod_lock_garaz_a_rozcestnik = False
        
        info_garaz_exit_obrazovka_x = 20 - kamera_x
        info_garaz_shop_jidlo_obrazovka_x = 490 - kamera_x
        
    if pozadi == garaz:
        hrac_rychlost = 4
        pozadi_sirka = pozadi.get_width()
        pozadi_vyska = pozadi.get_height()
        
        if hrac_pozice_x < 60:
            hrac_pozice_x = 60
        if hrac_pozice_x > pozadi_sirka - hrac_velikostX - 170:
            hrac_pozice_x = pozadi_sirka - hrac_velikostX - 170
                
            
        if hrac_obrazovka_x > prava_zona:
            kamera_x += hrac_aktualni_rychlost
        if hrac_obrazovka_x < leva_zona:
            kamera_x -= hrac_aktualni_rychlost
                
        if kamera_x < 0:
            kamera_x = 0
        if kamera_x > pozadi_sirka - okno_sirka:
            kamera_x = pozadi_sirka - okno_sirka
        
        stojim_u_cesty_ven_z_garazi = hrac_pozice_x > 20 and hrac_pozice_x < 140
        
        if stojim_u_cesty_ven_z_garazi and stisknuto[pygame.K_e] and not inventar and not prechod_lock_garaz_a_rozcestnik:
            
            pozadi = rozcestnik
            prechod_lock_garaz_a_rozcestnik = True
            hrac_pozice_x = 500
            hrac_rychlost = 4
            kamera_x = 100
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
        
        if not stojim_u_cesty_ven_z_garazi:
            prechod_lock_garaz_a_rozcestnik = False

        
        stojim_u_shopu_jidlo = hrac_pozice_x > 280 and hrac_pozice_x < 635
        
        
        if stojim_u_shopu_jidlo and stisknuto[pygame.K_e] and not inventar and pozadi == garaz:
            pozice_pred_jidlo_shopem = (hrac_pozice_x, hrac_pozice_y, kamera_x)
            stojim_u_shopu_jidlo = hrac_pozice_x > 280 and hrac_pozice_x < 635
            pozadi = pozadi_shop_jidlo
            hrac_pozice_x = 0
            hrac_rychlost = 0
            kamera_x = 0
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
            za_jidlo_shop_leave = pygame.draw.rect(okno, cerna, (9, 539, 102, 52))
            jidlo_shop_leave = pygame.draw.rect(okno, hneda, (10, 540, 100, 50))
            jidlo_polozky_velikost_y = 300
            jidlo_polozky_velikost_x = 150
            
            hranolky_cena = 20
            salat_cena = 35
            hamburger_cena = 60
            rybi_prsty_cena = 110
            
            hranolky_hunger = 20
            hranolky_zizen = 0
            
            salat_hunger = 20
            salat_zizen = 20
            
            hamburger_hunger = 55
            hamburger_zizen = 5
            
            rybi_prsty_hunger = 90
            rybi_prsty_zizen = 20
            
            hranolky_ikona = pygame.image.load("hranolky.png")
            salat_ikona = pygame.image.load("salat.png")
            hamburger_ikona = pygame.image.load("hamburger.png")
            rybi_prsty_ikona = pygame.image.load("rybi_prsty.png")
            
            za_hranolky_buy = pygame.draw.rect(okno, cerna, (39, 149, jidlo_polozky_velikost_x + 2, jidlo_polozky_velikost_y + 2))
            hranolky_buy = pygame.draw.rect(okno, hneda, (40, 150, jidlo_polozky_velikost_x, jidlo_polozky_velikost_y))
            
            za_salat_buy = pygame.draw.rect(okno, cerna, (229, 149, jidlo_polozky_velikost_x + 2, jidlo_polozky_velikost_y + 2))
            salat_buy = pygame.draw.rect(okno, hneda, (230, 150, jidlo_polozky_velikost_x, jidlo_polozky_velikost_y))
            
            za_hamburger_buy = pygame.draw.rect(okno, cerna, (419, 149, jidlo_polozky_velikost_x + 2, jidlo_polozky_velikost_y + 2))
            hamburger_buy = pygame.draw.rect(okno, hneda, (420, 150, jidlo_polozky_velikost_x, jidlo_polozky_velikost_y))
            
            za_rybi_prsty_buy = pygame.draw.rect(okno, cerna, (609, 149, jidlo_polozky_velikost_x + 2, jidlo_polozky_velikost_y + 2))
            rybi_prsty_buy = pygame.draw.rect(okno, hneda, (610, 150, jidlo_polozky_velikost_x, jidlo_polozky_velikost_y))
        
            
    if pozadi == pozadi_shop_jidlo:
        hrac_rychlost = 0
        pozadi_sirka = pozadi.get_width()
        pozadi_vyska = pozadi.get_height()
        
        if jidlo_shop_leave.collidepoint(mys_pozice) and mouse_click and not inventar:
            hrac_pozice_x, hrac_pozice_y, kamera_x = pozice_pred_jidlo_shopem
            stojim_u_shopu_jidlo = hrac_pozice_x > 280 and hrac_pozice_x < 635
            pozadi = garaz
            hrac_rychlost = 4
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
        
        if hranolky_buy.collidepoint(mys_pozice) and mouse_click and not inventar:
            if coins >= hranolky_cena:
                hlad += hranolky_hunger
                zizen += hranolky_zizen
                coins -= hranolky_cena
        
        if salat_buy.collidepoint(mys_pozice) and mouse_click and not inventar:
            if coins >= salat_cena:
                hlad += salat_hunger
                zizen += salat_zizen
                coins -= salat_cena
        
        if hamburger_buy.collidepoint(mys_pozice) and mouse_click and not inventar:
            if coins >= hamburger_cena:
                hlad += hamburger_hunger
                zizen += hamburger_zizen
                coins -= hamburger_cena
        
        if rybi_prsty_buy.collidepoint(mys_pozice) and mouse_click and not inventar:
            if coins >= rybi_prsty_cena:
                hlad += rybi_prsty_hunger
                zizen += rybi_prsty_zizen
                coins -= rybi_prsty_cena
        
            
        
    #BAR
        
    if pozadi == bar:
        info_rozcestnik_obrazovka_x = info_cesta_rozcestnik - kamera_x
        pozadi = bar
        hrac_pozice_x = 0
        kamera_x = 0
        hrac_rychlost = 0
        pozadi_sirka = pozadi.get_width()
        pozadi_vyska = pozadi.get_height()
        
        if bar_exit.collidepoint(mys_pozice) and mouse_click and not inventar:
            pozadi = rozcestnik
            hrac_pozice_x = 1150
            kamera_x = 752
            hrac_rychlost = 4
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
        
        if zidle_bar_rect.collidepoint(mys_pozice) and mouse_click and not inventar:
            barman_hlaska = random.choice(seznam_vet_barman)
            hlaska_barman_text = hlaska_barman_font.render(barman_hlaska, True, cerna)
            pozadi = barman
            hrac_pozice_x = 0
            kamera_x = 0
            hrac_rychlost = 0
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
        
        if slot_bar_rect.collidepoint(mys_pozice) and mouse_click and not inventar:
            pozadi = slotmachine
            hrac_pozice_x = 0
            kamera_x = 0
            hrac_rychlost = 0
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
    
    if pozadi == barman:
        if barman_exit.collidepoint(mys_pozice) and mouse_click and not inventar:
            pozadi = bar
            hrac_pozice_x = 0
            kamera_x = 0
            hrac_rychlost = 0
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
        
        if voda_buy.collidepoint(mys_pozice) and mouse_click and not inventar:
            if coins >= voda_cena:
                zizen += zizen_voda
                hlad += hlad_voda
                coins -= voda_cena
        
        if dzus_buy.collidepoint(mys_pozice) and mouse_click and not inventar:
            if coins >= dzus_cena:
                zizen += zizen_dzus
                hlad += hlad_dzus
                coins -= dzus_cena
        
        if cola_buy.collidepoint(mys_pozice) and mouse_click and not inventar:
            if coins >= cola_cena:
                zizen += zizen_cola
                hlad += hlad_cola
                coins -= cola_cena
        
        if pivo_buy.collidepoint(mys_pozice) and mouse_click and not inventar:
            if coins >= pivo_cena:
                zizen += zizen_pivo
                hlad += hlad_pivo
                coins -= pivo_cena
            
        

    
        
    #VENEK
    
    if pozadi == venek:
        if hrac_pozice_x < 60:
            hrac_pozice_x = 60
        if hrac_pozice_x > pozadi_sirka - hrac_velikostX - 170:
            hrac_pozice_x = pozadi_sirka - hrac_velikostX - 170
                
            
        if hrac_obrazovka_x > prava_zona:
            kamera_x += hrac_aktualni_rychlost
        if hrac_obrazovka_x < leva_zona:
            kamera_x -= hrac_aktualni_rychlost
                
        if kamera_x < 0:
            kamera_x = 0
        if kamera_x > pozadi_sirka - okno_sirka:
            kamera_x = pozadi_sirka - okno_sirka 

        info_shop_obrazovka_x = info_shop - kamera_x

        stojim_u_cesty_venek = hrac_pozice_x > 1 and hrac_pozice_x < 80
        
        if stojim_u_cesty_venek and stisknuto[pygame.K_e] and not inventar and not prechod_lock_venek_a_rozcestnik:
            pozadi = rozcestnik
            prechod_lock_venek_a_rozcestnik = True
            hrac_rychlost = 4
            hrac_pozice_x = 1300
            kamera_x = 848
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
        stojim_u_jezera = hrac_pozice_x > 1320 and hrac_pozice_x < 1450
        
        if not stojim_u_cesty_venek:
            prechod_lock_venek_a_rozcestnik = False 
        
        #Vstup na jezero
        
        if stojim_u_jezera and stisknuto[pygame.K_e] and not inventar and not prechod_lock_venek_a_jezero:
            pozadi = jezero
            prechod_lock_venek_a_jezero = True
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
            hrac_pozice_x = 370
            hrac_pozice_y = 320
            hrac_velikostX= 110
            hrac_velikostY = 170
            hrac_rychlost = 4
        
        if not stojim_u_jezera:
            prechod_lock_venek_a_jezero = False
            
        info_jezero_obrazovka_x = info_jezero - kamera_x

        stojim_u_shopu = hrac_pozice_x > 750 and hrac_pozice_x < 1020
        
        #Vstup do shopu
        
        if stojim_u_shopu and stisknuto[pygame.K_e] and not inventar:
            pozice_pred_shopem = (hrac_pozice_x, hrac_pozice_y, kamera_x)
            pozadi = shop
            hrac_rychlost = 0
            
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
            
            shop_mode = None
            
            shop_hlaska = random.choice(seznam_vet)
            hlaska_text = hlaska_font.render(shop_hlaska, True, cerna)
        
        stojim_u_domu = hrac_pozice_x > 90 and hrac_pozice_x < 340
        info_dum_obrazovka_x = info_dum - kamera_x
        
        if stojim_u_domu and stisknuto[pygame.K_e] and not inventar and not prechod_lock_dum_a_venek:
            pozadi = dum
            prechod_lock_dum_a_venek = True
            hrac_rychlost = 4
            hrac_pozice_x = 400
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
            kamera_x = 0
        
        if not stojim_u_domu:
            prechod_lock_dum_a_venek = False
        
        stojim_u_boudy = hrac_pozice_x > 380 and hrac_pozice_x < 560
        info_bouda_obrazovka_x = 1080 - kamera_x
        

        
    #DUM
    info_vnitrek_domu_obrazovka_x = info_vnitrek_domu - kamera_x
    stojim_u_dveri = hrac_pozice_x > 560 and hrac_pozice_x < 800
    stojim_u_postele = hrac_pozice_x > 400 and hrac_pozice_x < 540
    stojim_u_krbu = hrac_pozice_x > 110 and hrac_pozice_x < 230
    za_krb_leave = pygame.draw.rect(okno, cerna, (679, 479, 102, 52))
    krb_leave = pygame.draw.rect(okno, hneda, (680, 480, 100, 50))
    
    if pozadi == dum:
        
        if hrac_pozice_x < 200:
            hrac_pozice_x = 200
        if hrac_pozice_x > 700 - hrac_velikostX:
            hrac_pozice_x = 700 - hrac_velikostX
        
        if stojim_u_dveri and stisknuto[pygame.K_e] and not inventar and not prechod_lock_dum_a_venek:
            pozadi = venek
            prechod_lock_dum_a_venek = True
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()

            hrac_pozice_x = 360
            hrac_pozice_y = 315

            hrac_velikostX = 110
            hrac_velikostY = 170
            hrac_rychlost = 4

            kamera_x = 0
        
        if not stojim_u_dveri:
            prechod_lock_dum_a_venek = False
        
        if stojim_u_postele and stisknuto[pygame.K_e] and not inventar and pozadi == dum:
            pass
        
        if stojim_u_krbu and stisknuto[pygame.K_e] and not inventar and not prechod_lock_dum_a_krb:
            pozadi = krb
            prechod_lock_dum_a_krb = True
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
            
            hrac_rychlost = 0
        
        if not stojim_u_krbu:
            prechod_lock_dum_a_krb = False
    
    if pozadi == krb:
        if deprese > 0:
            deprese -= 0.02

            
    if pozadi == krb and krb_leave.collidepoint(mys_pozice) and mouse_click and not inventar:
        pozadi = dum
        hrac_rychlost = 4
        hrac_pozice_x = 240
        pozadi_sirka = pozadi.get_width()
        pozadi_vyska = pozadi.get_height()
        kamera_x = 0
        
        
    #JEZERO
    if pozadi == jezero:
    
        kamera_x = 0
        
        aktualni_sprite = TEXTURApepa_lod
        
        if stisknuto[pygame.K_d]:
            aktualni_sprite = TEXTURApepa_2_lod

        elif stisknuto[pygame.K_a]:
            aktualni_sprite = TEXTURApepa_1_lod
            
        if hrac_pozice_x < 330:
            hrac_pozice_x = 330
        if hrac_pozice_x > 422:
            hrac_pozice_x = 422
                
        if kamera_x < 0:
            kamera_x = 0
        if kamera_x > pozadi_sirka - okno_sirka:
            kamera_x = pozadi_sirka - okno_sirka 
        
        stojim_u_leva_lod = hrac_pozice_x > 329 and hrac_pozice_x < 350
        
        #Vystup z lode na jezere zpatky ven
        
        if stojim_u_leva_lod and stisknuto[pygame.K_e] and not inventar and not prechod_lock_venek_a_jezero:
            pozadi = venek
            prechod_lock_venek_a_jezero = True
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()

            hrac_pozice_x = 1312
            hrac_pozice_y = 315

            hrac_velikostX = 110
            hrac_velikostY = 170
            hrac_rychlost = 4

            kamera_x = 848
        
        if not stojim_u_leva_lod:
            prechod_lock_venek_a_jezero = False

        stojim_u_prava_lod = hrac_pozice_x > 395 and hrac_pozice_x < 423
        
        #Vstup z lode na jezere do rybareni
        
        if stojim_u_prava_lod and stisknuto[pygame.K_e] and pozadi != rybareni and not inventar:
            pozadi = rybareni
            zpet_tlacitko = True
            hrac_rychlost = 0
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
            
    
    #Tlacitko exit k opusteni rybareni zpet na jezero
    
    if zpet_tlacitko and pozadi == rybareni and zpet_tlacitko_rect.collidepoint(mys_pozice) and mouse_click and not inventar:
        pozadi = jezero
        zpet_tlacitko = False
        hrac_rychlost = 4
        hrac_pozice_x = 422
        kamera_x = 0
        aktualni_sprite = TEXTURApepa_lod

    #SPACE k zapnuti naprahu
    
    if pozadi == rybareni and stisknuto[pygame.K_SPACE] and not (prut or minihra) and not inventar and (baits_mode is None or baits_mode["pocet"] == 0):
        None
   
    elif pozadi == rybareni and stisknuto[pygame.K_SPACE] and not (prut or minihra) and not inventar:
          
        if sum(obsah_inventare.values()) < obsah_inventare_max:
            pozadi = rybareni_dole
            hrac_rychlost = 0
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
            prut = True
            zpet_tlacitko = False
            
            ulovek = vyber_predmet(predmety, baits_mode)
            ulovek["cekani"] += baits_mode["cekani"]
            ulovek["zmacknuti"] += baits_mode["zmacknuti"]
            ulovek["cekani"] += penalizace_cekani_z_hladu()
            ulovek["zmacknuti"] += penalizace_kliknuti_z_deprese()
            cas_nahozeni = pygame.time.get_ticks()
        else:
            plny_inventar_upozorneni = True
            plny_inventar_cas = pygame.time.get_ticks()
    
    #Doba cekani nez hrac muze chytat ulovek
    
    if prut and pygame.time.get_ticks() - cas_nahozeni > ulovek["cekani"]:
        prut = False
        minihra = True
        sekvence = ""
        poradi = 0
        
        #Pridani pismena do sekvence a opatreni proti opakujicimu pismenu
        delka_sekvence = max(ulovek["zmacknuti"], 1)
        for pismeno in range(delka_sekvence):
            pismneko_ktere_zkousime_davat_do_sekvence = chr(random.randint(97, 97 + 25))
            while sekvence != "" and sekvence[-1] == pismneko_ktere_zkousime_davat_do_sekvence:
                pismneko_ktere_zkousime_davat_do_sekvence = chr(random.randint(97, 97 + 25))
            sekvence += pismneko_ktere_zkousime_davat_do_sekvence
        pismeno_text = pismeno_font.render(f"{sekvence[poradi]}", True, cerna)
        okraj_random_x = random.randint(20, 780 - pismeno_velikost)
        okraj_random_y = random.randint(20, 580 - pismeno_velikost)
        zacatek_limitu = pygame.time.get_ticks()
        

    #System minihry, scitani poradi, ziskani ulovku
    
    if minihra:
        pozadi = rybareni_pozor
        hrac_rychlost = 0
        pozadi_sirka = pozadi.get_width()
        pozadi_vyska = pozadi.get_height()
        
        if pygame.time.get_ticks() - zacatek_limitu > ulovek["limit_cekani"]:
            minihra = False
            zpet_tlacitko = True
            pozadi = rybareni
            hrac_rychlost = 0
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
            baits_mode["pocet"] -= 1
    
        elif stisknuto[ord(sekvence[poradi])]:
            poradi += 1
            if poradi < ulovek["zmacknuti"]:
                pismeno_text = pismeno_font.render(f"{sekvence[poradi]}", True, cerna)
                okraj_random_x = random.randint(20, 780 - pismeno_velikost)
                okraj_random_y = random.randint(20, 580 - pismeno_velikost)
                
                zacatek_limitu = pygame.time.get_ticks()
            else:
                inventar_order.append(ulovek)
                obsah_inventare[ulovek["jmeno"]] += 1
                baits_mode["pocet"] -= 1
                
                posledni_ulovek = ulovek
                posledni_ulovek_cas = pygame.time.get_ticks()
                
                minihra = False
                zpet_tlacitko = True
                pozadi = rybareni
                hrac_rychlost = 0
                pozadi_sirka = pozadi.get_width()
                pozadi_vyska = pozadi.get_height()
                
        elif any(stisknuto) and not (poradi > 0 and stisknuto[ord(sekvence[poradi - 1])]):
            minihra = False
            zpet_tlacitko = True
            pozadi = rybareni
            hrac_rychlost = 0
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
            baits_mode["pocet"] -= 1
        

                   
    #Funkcnost shopu, klik na buy, sell a moznost opusteni shopu
            
    if pozadi == shop:
        if shop_mode is None: 
            if buy.collidepoint(mys_pozice) and mouse_click:
                shop_mode = "buy"
        
            elif sell.collidepoint(mys_pozice) and mouse_click:
                shop_mode = "sell"
        
            elif leave.collidepoint(mys_pozice) and mouse_click:
                pozadi = venek
                hrac_pozice_x, hrac_pozice_y, kamera_x = pozice_pred_shopem
                hrac_velikostX = 110
                hrac_velikostY = 170
                hrac_rychlost = 4
                shop_mode = None
                shop_hlaska = None
                pozadi_sirka = pozadi.get_width()
                pozadi_vyska = pozadi.get_height()
                
                
    if shop_mode == "sell" and pozadi == pozadi_shop and mouse_click:
        for rect, jmeno in sell_items:
            if rect.collidepoint(mys_pozice):
                zisk = prodej_predmet(jmeno)
                if zisk:
                    coins += zisk
                break
    
    if shop_mode == "buy" and pozadi == pozadi_shop:
        if kyblik_buy.collidepoint(mys_pozice) and mouse_click:
            if kyblik_lvl < max_upgrade_kybliku and coins >= kyblik_cena:
                obsah_inventare_max += 6
                coins -= kyblik_cena
                
                kyblik_lvl += 1
                kyblik_cena *= 2
                
                
        if zmacknuti_buy.collidepoint(mys_pozice) and mouse_click:
            if zmacknuti_lvl < max_upgrade_zmacknuti and coins >= zmacknuti_cena:
                for predmet in predmety:
                    if predmet["zmacknuti"] > 1:
                        predmet["zmacknuti"] -= 1
                        
                coins -= zmacknuti_cena
                zmacknuti_lvl += 1
                zmacknuti_cena *= 2
                

                
        if cekani_buy.collidepoint(mys_pozice) and mouse_click:
            if cekani_lvl < max_upgrade_cekani and coins >= cekani_cena:
                for predmet in predmety:
                    if predmet["cekani"] > 200:
                        predmet["cekani"] -= 200

                momentalni_cekani += 2
                        
                coins -= cekani_cena
                cekani_lvl += 1
                cekani_cena *= 2
        
        if bread_bait.collidepoint(mys_pozice) and mouse_click:
            if coins >= bread_bait_cena:
                if soucet_vsech_baits() < obsah_baits_max:
                    baits["bread"]["pocet"] += 1
                    coins -= bread_bait_cena
        
        if worm_bait.collidepoint(mys_pozice) and mouse_click:
            if coins >= worm_bait_cena:
                if soucet_vsech_baits() < obsah_baits_max:
                    baits["worm"]["pocet"] += 1
                    coins -= worm_bait_cena
                
        if corn_bait.collidepoint(mys_pozice) and mouse_click:
            if coins >= corn_bait_cena:
                if soucet_vsech_baits() < obsah_baits_max:
                    baits["corn"]["pocet"] += 1
                    coins -= corn_bait_cena
            
        if fish_head_bait.collidepoint(mys_pozice) and mouse_click:
            if coins >= fish_head_bait_cena:
                if soucet_vsech_baits() < obsah_baits_max:
                    baits["fish_head"]["pocet"] += 1 
                    coins -= fish_head_bait_cena
        
        if baits_upgrade.collidepoint(mys_pozice) and mouse_click:
            if coins >= baits_upgrade_cena:
                if baits_lvl < max_upgrade_baits:
                    baits_lvl += 1
                    coins -= baits_upgrade_cena
                    baits_upgrade_cena *= 2
                    obsah_baits_max += 4

            
        #Prechod z buy nebo sell na none (uvitaci stranka shopu)
        
        if shop_mode == "buy":
            if leave_buy.collidepoint(mys_pozice) and mouse_click:
                shop_mode = None
                pozadi = shop
        
        elif shop_mode == "sell":
            if leave_sell.collidepoint(mys_pozice) and mouse_click:
                shop_mode = None
                pozadi = shop

    
    #Omezeni otevirani inv v shopu a v buy and sell a v slotmachine
    
    if pozadi != shop and pozadi != pozadi_shop and pozadi != slotmachine:
        if ikona_inv_rect.collidepoint(mys_pozice) and mouse_click:
            inventar = True
            hrac_rychlost = 0
        if inventar:
            if tlacitko.collidepoint(mys_pozice) and mouse_click:
                inventar = False
                hrac_rychlost = 4
    if prut:
        if ikona_inv_rect.collidepoint(mys_pozice) and mouse_click:
            inventar = False
            hrac_rychlost = 0
    
    if minihra:
        if ikona_inv_rect.collidepoint(mys_pozice) and mouse_click:
            inventar = False
            hrac_rychlost = 0
    
    
    if inventar and baits_mode is None:
        if bread_tlacitko_inventory.collidepoint(mys_pozice) and mouse_click:
            baits_mode = baits["bread"]

        elif worm_tlacitko_inventory.collidepoint(mys_pozice) and mouse_click:
            baits_mode = baits["worm"]

        elif corn_tlacitko_inventory.collidepoint(mys_pozice) and mouse_click:
            baits_mode = baits["corn"]
        
        elif fish_head_tlacitko_inventory.collidepoint(mys_pozice) and mouse_click:
            baits_mode = baits["fish_head"]
    
    if inventar and baits_mode is not None:
        if bait_leave_tlacitko_inventory.collidepoint(mys_pozice) and mouse_click:
            baits_mode = None



    #Kurzor na hand nebo arrow podle urciteho pozadi ci podminky
    
    kurzor_hand = False 

                
    if pozadi == pozadi_shop and leave_buy.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    
    elif pozadi == pozadi_shop_jidlo and jidlo_shop_leave.collidepoint(mys_pozice) and not inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    
    elif pozadi == pozadi_shop_jidlo and hranolky_buy.collidepoint(mys_pozice) and not inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    
    elif pozadi == pozadi_shop_jidlo and hamburger_buy.collidepoint(mys_pozice) and not inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    
    elif pozadi == pozadi_shop_jidlo and salat_buy.collidepoint(mys_pozice) and not inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    elif pozadi == pozadi_shop_jidlo and rybi_prsty_buy.collidepoint(mys_pozice) and not inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    
    elif not zapnuti and zapnuti_statistik.collidepoint(mys_pozice) and pozadi != rybareni and not inventar and pozadi != bar and pozadi != barman and pozadi != shop and not shop_mode == "sell" and not shop_mode == "buy" and not prut and not minihra and pozadi != pozadi_shop_jidlo:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    
    elif not zapnuti and zapnuti_statistik_rybareni.collidepoint(mys_pozice) and not inventar and pozadi == rybareni:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    elif zapnuti and vypnuti_statistik.collidepoint(mys_pozice) and not inventar and pozadi != bar and pozadi != barman and pozadi != shop and not shop_mode == "sell" and not shop_mode == "buy" and not prut and not minihra and pozadi != pozadi_shop_jidlo:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
         
    elif pozadi == bar and bar_exit.collidepoint(mys_pozice) and not inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == barman and barman_exit.collidepoint(mys_pozice) and not inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == bar and zidle_bar_rect.collidepoint(mys_pozice) and not inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    elif pozadi == bar and slot_bar_rect.collidepoint(mys_pozice) and not inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    
    elif pozadi == barman and voda_buy.collidepoint(mys_pozice) and not inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == barman and dzus_buy.collidepoint(mys_pozice) and not inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == barman and cola_buy.collidepoint(mys_pozice) and not inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    elif pozadi == barman and pivo_buy.collidepoint(mys_pozice) and not inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    
    elif pozadi == shop and (buy.collidepoint(mys_pozice) or sell.collidepoint(mys_pozice) or leave.collidepoint(mys_pozice)):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == pozadi_shop and leave_sell.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif ikona_inv_rect.collidepoint(mys_pozice)and not inventar and not pozadi == shop and not pozadi == pozadi_shop and not minihra and not prut and pozadi != slotmachine:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif tlacitko.collidepoint(mys_pozice) and inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif zpet_tlacitko_rect.collidepoint(mys_pozice) and not prut and not minihra and pozadi == rybareni and not inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == pozadi_shop and shop_mode == "sell" and plechovka_sell.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == pozadi_shop and shop_mode == "sell" and bota_sell.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == pozadi_shop and shop_mode == "sell" and kapr_sell.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == pozadi_shop and shop_mode == "sell" and stika_sell.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == pozadi_shop and shop_mode == "sell" and sumec_sell.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == pozadi_shop and shop_mode == "sell" and tajnaRyba_sell.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == pozadi_shop and shop_mode == "buy" and kyblik_buy.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == pozadi_shop and shop_mode == "buy" and zmacknuti_buy.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == pozadi_shop and shop_mode == "buy" and cekani_buy.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == pozadi_shop and shop_mode == "buy" and bread_bait.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == pozadi_shop and shop_mode == "buy" and worm_bait.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == pozadi_shop and shop_mode == "buy" and corn_bait.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == pozadi_shop and shop_mode == "buy" and fish_head_bait.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif pozadi == pozadi_shop and shop_mode == "buy" and baits_upgrade.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    elif baits_mode is None and inventar:
        if bread_tlacitko_inventory.collidepoint(mys_pozice) and inventar:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif worm_tlacitko_inventory.collidepoint(mys_pozice) and inventar:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif corn_tlacitko_inventory.collidepoint(mys_pozice) and inventar:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif fish_head_tlacitko_inventory.collidepoint(mys_pozice) and inventar:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:         
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    elif baits_mode is not None and inventar:
        if bait_leave_tlacitko_inventory.collidepoint(mys_pozice) and inventar:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:         
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    elif pozadi == krb and krb_leave.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:         
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    # VYKRESLENI PRVKU HRY
    
    if pozadi != shop:
        okno.blit(pozadi, (-kamera_x, 0))
    else:
        okno.blit(pozadi, (0, 0))
    
    
    if not zapnuti and not inventar and pozadi != bar and pozadi != barman and pozadi != shop and not shop_mode == "sell" and not shop_mode == "buy" and pozadi and not minihra and not prut and pozadi != pozadi_shop_jidlo:
        if pozadi == rybareni:
            pygame.draw.rect(okno, cerna, (4, 564, 82, 32))
            pygame.draw.rect(okno, hneda, (5, 565, 80, 30))
            okno.blit(zapnuti_statistik_ikona, (5, 565, 80, 30))
        else:
            pygame.draw.rect(okno, cerna, za_zapnuti_statistik)
            pygame.draw.rect(okno, hneda, zapnuti_statistik)
            okno.blit(zapnuti_statistik_ikona, (360, 565, 80, 30))

    if pozadi == venek:
        okno.blit(bouda, (info_bouda_obrazovka_x, 290))
    
    if zapnuti and not inventar and pozadi != bar and pozadi != barman and pozadi != shop and not shop_mode == "sell" and not shop_mode == "buy" and not prut and not minihra and pozadi != pozadi_shop_jidlo:
        pygame.draw.rect(okno, cerna, za_vypnuti_statistik)
        pygame.draw.rect(okno, hneda, vypnuti_statistik)
        okno.blit(vypnuti_statistik_ikona, (360, 5, 80, 30))

    if zapnuti and pozadi != shop and not inventar and not minihra and not prut and pozadi != bar and pozadi != barman and pozadi != slotmachine and pozadi != pozadi_shop_jidlo:
        pygame.draw.rect(okno, cerna, (4 , 544, 102 , 52))
        pygame.draw.rect(okno, Shneda, (5 , 545, 100 , 50))
        hlad_info = statistika_font.render(f"{int(hlad)}/100", True, cerna)
        hlad_text = statistika_font.render("Hunger:", True, cerna)
        okno.blit(hlad_ikona, (5 , 542, 100 , 50))
        okno.blit(hlad_info, (53 , 565, 100 , 50))
        okno.blit(hlad_text, (51 , 545, 100 , 50))
        
        pygame.draw.rect(okno, cerna, (109 , 544, 102 , 52))
        pygame.draw.rect(okno, modra, (110 , 545, 100 , 50))
        zizen_info = statistika_font.render(f"{int(zizen)}/100", True, cerna)
        zizen_text = statistika_font.render("Thirst:", True, cerna)
        okno.blit(zizen_ikona, (110 , 545, 100 , 50))
        okno.blit(zizen_info, (158, 565, 100, 50))
        okno.blit(zizen_text, (158, 545, 100, 50))
    
        pygame.draw.rect(okno, cerna, (694 , 544, 102 , 52))
        pygame.draw.rect(okno, fialova, (695 , 545, 100 , 50))
        deprese_info = statistika_font.render(f"{int(deprese)}/100", True, cerna)
        deprese_text = statistika_font.render("Misery:", True, cerna)
        okno.blit(deprese_ikona, (695 , 545, 100 , 50))
        okno.blit(deprese_info, (695 + 48, 565, 100, 50))
        okno.blit(deprese_text, (695 + 48, 545, 100, 50))
        
        pygame.draw.rect(okno, cerna, (259, 544, 282, 52))
        pygame.draw.rect(okno, hneda, (260, 545, 280, 50))
        okno.blit(hlad_text, (265 , 545, 100 , 50))
        okno.blit(zizen_text, (370, 545, 100, 50))
        okno.blit(deprese_text, (460, 545, 100, 50))
        hlad_dopad_text = statistika_font.render("Waiting time:", True , cerna)
        hlad_dopad_cislo_text = statistika_font.render(f"+{penalizace_cekani_z_hladu()/1000}s", True, cerna)
        okno.blit(hlad_dopad_text, (265 , 560))
        okno.blit(hlad_dopad_cislo_text, (265 , 575))
        zizen_dopad_text = statistika_font.render("Movement:", True, cerna)
        zizen_dopad_rychlost_text = statistika_font.render(f"{rychlost_na_text()}", True, cerna)
        okno.blit(zizen_dopad_text, (370, 560))
        okno.blit(zizen_dopad_rychlost_text, (370, 575))
        deprese_dopad_text = statistika_font.render("More clicks:", True, cerna)
        deprese_dopad_cislo_text = statistika_font.render(f"+{penalizace_kliknuti_z_deprese()}", True, cerna)
        okno.blit(deprese_dopad_text, (460, 560))
        okno.blit(deprese_dopad_cislo_text, (460, 575))
        
    if pozadi == bar:
        pygame.draw.rect(okno, cerna, za_bar_exit)
        pygame.draw.rect(okno, hneda, bar_exit)
        exit_bar_text = exit_bar_font.render("EXIT", True, cerna)
        okno.blit(exit_bar_text, (36, 543))
        
        okno.blit(zidle_bar, zidle_bar_rect)
        okno.blit(slot_bar, slot_bar_rect)
    
    if pozadi == barman:
        pygame.draw.rect(okno, cerna, za_barman_exit)
        pygame.draw.rect(okno, hneda, barman_exit)
        exit_barman_text = exit_bar_font.render("EXIT", True, cerna)
        okno.blit(exit_barman_text, (26, 558))
        okno.blit(hlaska_barman_text, (390, 160))
        
        pygame.draw.rect(okno, cerna, za_voda_buy)
        pygame.draw.rect(okno, hneda, voda_buy)
        okno.blit(voda, (82, 380))
        voda_text = info_barman_font.render("water", True, cerna)
        okno.blit(voda_text, (100, 431))
        voda_cena_text = drink_cena_font.render(f"{voda_cena}", True, zluta)
        okno.blit(voda_cena_text, (102, 502))
        okno.blit(coin_ikona, (132, 502))
        statistika_zizne_voda_text = statistika_font.render(f"Thirst: +{zizen_voda}", True, cerna)
        okno.blit(statistika_zizne_voda_text, (77, 458))
        statistika_hladu_voda_text = statistika_font.render(f"Hunger: +{hlad_voda}", True, cerna)
        okno.blit(statistika_hladu_voda_text, (77, 478))
        
        pygame.draw.rect(okno, cerna, za_dzus_buy)
        pygame.draw.rect(okno, hneda, dzus_buy)
        okno.blit(dzus, (260, 380))
        dzus_text = info_barman_font.render("juice", True, cerna)
        okno.blit(dzus_text, (284, 431))
        dzus_cena_text = drink_cena_font.render(f"{dzus_cena}", True, zluta)
        okno.blit(dzus_cena_text, (280, 502))
        okno.blit(coin_ikona, (310, 502))
        statistika_zizne_dzus_text = statistika_font.render(f"Thirst: +{zizen_dzus}", True, cerna)
        okno.blit(statistika_zizne_dzus_text, (255, 458))
        statistika_hladu_dzus_text = statistika_font.render(f"Hunger: +{hlad_dzus}", True, cerna)
        okno.blit(statistika_hladu_dzus_text,  (255, 478))

        pygame.draw.rect(okno, cerna, za_cola_buy)
        pygame.draw.rect(okno, hneda, cola_buy)
        okno.blit(cola, (438, 380))
        cola_text = info_barman_font.render("cola", True, cerna)
        okno.blit(cola_text, (464, 431))
        cola_cena_text = drink_cena_font.render(f"{cola_cena}", True, zluta)
        okno.blit(cola_cena_text, (460, 502))
        okno.blit(coin_ikona, (490, 502))
        statistika_zizne_cola_text = statistika_font.render(f"Thirst: +{zizen_cola}", True, cerna)
        okno.blit(statistika_zizne_cola_text, (434, 458))
        statistika_hladu_cola_text = statistika_font.render(f"Hunger: +{hlad_cola}", True, cerna)
        okno.blit(statistika_hladu_cola_text, (434, 478))
        
        pygame.draw.rect(okno, cerna, za_pivo_buy)
        pygame.draw.rect(okno, hneda, pivo_buy)
        okno.blit(pivo, (616, 382))
        pivo_text = info_barman_font.render("beer 0%", True, cerna)
        okno.blit(pivo_text, (630, 431))
        pivo_cena_text = drink_cena_font.render(f"{pivo_cena}", True, zluta)
        okno.blit(pivo_cena_text, (640, 502))
        okno.blit(coin_ikona, (670, 502))
        statistika_zizne_piva_text = statistika_font.render(f"Thirst: +{zizen_pivo}", True, cerna)
        okno.blit(statistika_zizne_piva_text, (610, 458))
        statistika_hladu_pivo_text = statistika_font.render(f"Hunger: +{hlad_pivo}", True, cerna)
        okno.blit(statistika_hladu_pivo_text, (610, 478))
        
        pygame.draw.rect(okno, cerna, (649 , 544, 102 , 52))
        pygame.draw.rect(okno, Shneda, (650 , 545, 100 , 50))
        hlad_info = statistika_font.render(f"{int(hlad)}/100", True, cerna)
        hlad_text = statistika_font.render("Hunger:", True, cerna)
        okno.blit(hlad_ikona, (650 , 542, 100 , 50))
        okno.blit(hlad_info, (698 , 565, 100 , 50))
        okno.blit(hlad_text, (696 , 545, 100 , 50))
        
        pygame.draw.rect(okno, cerna, (539 , 544, 102 , 52))
        pygame.draw.rect(okno, modra, (540 , 545, 100 , 50))
        zizen_info = statistika_font.render(f"{int(zizen)}/100", True, cerna)
        zizen_text = statistika_font.render("Thirst:", True, cerna)
        okno.blit(zizen_ikona, (540 , 545, 100 , 50))
        okno.blit(zizen_info, (588, 565, 100, 50))
        okno.blit(zizen_text, (586, 545, 100, 50))
        
    if pozadi == rozcestnik and stojim_u_auta:
        pygame.draw.rect(okno, cerna, (info_rozcestnik_obrazovka_x - 1401, 339, 52, 52))
        pygame.draw.rect(okno, bila, (info_rozcestnik_obrazovka_x - 1400, 340, 50, 50))
        okno.blit(E_text, (info_rozcestnik_obrazovka_x - 1400 + (50/2 - E_text.get_size()[0] / 2), 352))
        
    if pozadi == garaz and stojim_u_cesty_ven_z_garazi and not prechod_lock_garaz_a_rozcestnik:
        pygame.draw.rect(okno, cerna, (info_garaz_exit_obrazovka_x - 1, 339, 52, 52))
        pygame.draw.rect(okno, bila, (info_garaz_exit_obrazovka_x, 340, 50, 50))
        okno.blit(E_text, (info_garaz_exit_obrazovka_x + (50/2 - E_text.get_size()[0] / 2), 352))
    
    if pozadi == garaz and stojim_u_shopu_jidlo:
        e_shop_jidlo_x = 490 - kamera_x  
        pygame.draw.rect(okno, cerna, (e_shop_jidlo_x - 1, 339, 52, 52))
        pygame.draw.rect(okno, bila, (e_shop_jidlo_x, 340, 50, 50))
        okno.blit(E_text, (e_shop_jidlo_x + (50/2 - E_text.get_size()[0] / 2), 352))
    
    if pozadi == pozadi_shop_jidlo and not inventar:

        pygame.draw.rect(okno, cerna, za_jidlo_shop_leave)
        pygame.draw.rect(okno, hneda, jidlo_shop_leave)
        exit_shop_s_jidlem_text = exit_shop_s_jidlem_font.render("EXIT", True, cerna)
        okno.blit(exit_shop_s_jidlem_text,( 27, 553))
        
        pygame.draw.rect(okno, cerna, za_hranolky_buy)
        pygame.draw.rect(okno, hneda, hranolky_buy)
        hranolky_cena_text = jidlo_cena_font.render(f"{hranolky_cena}", True, zluta)
        okno.blit(hranolky_cena_text, (90, 410))
        okno.blit(coin_ikona, (120, 410))
        hranolky_jmeno_text = jidlo_jmeno_font.render("Fries", True, cerna)
        okno.blit(hranolky_jmeno_text, (90, 160))
        hranolky_popis_hlad_text = jidlo_popis_font.render(f"Hunger: +{hranolky_hunger}", True, cerna)
        hranolky_popis_zizen_text = jidlo_popis_font.render(f"Thirst: +{hranolky_zizen}", True, cerna)
        okno.blit(hranolky_popis_hlad_text, (50, 340))
        okno.blit(hranolky_popis_zizen_text, (50, 365))
        okno.blit(hranolky_ikona, (hranolky_buy))
            
        pygame.draw.rect(okno, cerna, za_salat_buy)                                       
        pygame.draw.rect(okno, hneda, salat_buy)
        salat_cena_text = jidlo_cena_font.render(f"{salat_cena}", True, zluta)
        okno.blit(salat_cena_text, (280, 410))
        okno.blit(coin_ikona, (310, 410))
        salat_jmeno_text = jidlo_jmeno_font.render("Salad", True, cerna)
        okno.blit(salat_jmeno_text, (275, 160))
        salat_popis_hlad_text = jidlo_popis_font.render(f"Hunger: +{salat_hunger}", True, cerna)
        salat_popis_zizen_text = jidlo_popis_font.render(f"Thirst: +{salat_zizen}", True, cerna)
        okno.blit(salat_popis_hlad_text, (240, 340))
        okno.blit(salat_popis_zizen_text, (240, 365))
        okno.blit(salat_ikona, (salat_buy))

        
        pygame.draw.rect(okno, cerna, za_hamburger_buy)
        pygame.draw.rect(okno, hneda, hamburger_buy)
        hamburger_cena_text = jidlo_cena_font.render(f"{hamburger_cena}", True, zluta)
        okno.blit(hamburger_cena_text, (470, 410))
        okno.blit(coin_ikona, (500, 410))
        hamburger_jmeno_text = jidlo_jmeno_font.render("Hamburger", True, cerna)
        okno.blit(hamburger_jmeno_text, (440, 160))
        hamburger_popis_hlad_text = jidlo_popis_font.render(f"Hunger: +{hamburger_hunger}", True, cerna)
        hamburger_popis_zizen_text = jidlo_popis_font.render(f"Thirst: +{hamburger_zizen}", True, cerna)
        okno.blit(hamburger_popis_hlad_text, (430, 340))
        okno.blit(hamburger_popis_zizen_text, (430, 365))
        okno.blit(hamburger_ikona, (hamburger_buy))

        
        pygame.draw.rect(okno, cerna, za_rybi_prsty_buy)
        pygame.draw.rect(okno, hneda, rybi_prsty_buy)
        rybi_prsty_cena_text = jidlo_cena_font.render(f"{rybi_prsty_cena}", True, zluta)
        okno.blit(rybi_prsty_cena_text, (655, 410))
        okno.blit(coin_ikona, (690, 410))
        rybi_prsty_jmeno_text = jidlo_jmeno_font.render("Fish sticks", True, cerna)
        okno.blit(rybi_prsty_jmeno_text, (633, 160))
        rybi_prsty_popis_hlad_text = jidlo_popis_font.render(f"Hunger: +{rybi_prsty_hunger}", True, cerna)
        rybi_prsty_popis_zizen_text = jidlo_popis_font.render(f"Thirst: +{rybi_prsty_zizen}", True, cerna)
        okno.blit(rybi_prsty_popis_hlad_text, (620, 340))
        okno.blit(rybi_prsty_popis_zizen_text, (620, 365))
        okno.blit(rybi_prsty_ikona, (rybi_prsty_buy))



        
        
        pygame.draw.rect(okno, cerna, (649 , 544, 102 , 52))
        pygame.draw.rect(okno, Shneda, (650 , 545, 100 , 50))
        hlad_info = statistika_font.render(f"{int(hlad)}/100", True, cerna)
        hlad_text = statistika_font.render("Hunger:", True, cerna)
        okno.blit(hlad_ikona, (650 , 542, 100 , 50))
        okno.blit(hlad_info, (698 , 565, 100 , 50))
        okno.blit(hlad_text, (696 , 545, 100 , 50))
        
        pygame.draw.rect(okno, cerna, (539 , 544, 102 , 52))
        pygame.draw.rect(okno, modra, (540 , 545, 100 , 50))
        zizen_info = statistika_font.render(f"{int(zizen)}/100", True, cerna)
        zizen_text = statistika_font.render("Thirst:", True, cerna)
        okno.blit(zizen_ikona, (540 , 545, 100 , 50))
        okno.blit(zizen_info, (588, 565, 100, 50))
        okno.blit(zizen_text, (586, 545, 100, 50))
        

        
    if pozadi == rozcestnik and stojim_u_cesty_mezi_bar_a_auto and not prechod_lock_garaz_a_rozcestnik:
        pygame.draw.rect(okno, cerna, (info_rozcestnik_obrazovka_x - 899, 339, 52, 52))
        pygame.draw.rect(okno, bila, (info_rozcestnik_obrazovka_x - 898, 340, 50, 50))
        okno.blit(E_text, (info_rozcestnik_obrazovka_x - 898 + (50/2 - E_text.get_size()[0] / 2), 352))
        
    if pozadi == rozcestnik and stojim_u_cesty_rozcestnik and not prechod_lock_venek_a_rozcestnik:
        pygame.draw.rect(okno, cerna, (info_rozcestnik_obrazovka_x - 1, 339, 52, 52))
        pygame.draw.rect(okno, bila, (info_rozcestnik_obrazovka_x, 340, 50, 50))
        okno.blit(E_text, (info_rozcestnik_obrazovka_x + (50/2 - E_text.get_size()[0] / 2), 352))
    
    if pozadi == rozcestnik and stojim_u_baru:
        pygame.draw.rect(okno, cerna, (info_rozcestnik_obrazovka_x - 539, 339, 52, 52))
        pygame.draw.rect(okno, bila, (info_rozcestnik_obrazovka_x - 538, 340, 50, 50))
        okno.blit(E_text, (info_rozcestnik_obrazovka_x - 538 + (50/2 - E_text.get_size()[0] / 2), 352))
    
    if pozadi == venek and stojim_u_jezera and not prechod_lock_venek_a_jezero:
        pygame.draw.rect(okno, cerna, za_e_u_jezera)
        pygame.draw.rect(okno, (bila), (info_jezero_obrazovka_x, 340, 50, 50))
        okno.blit(E_text, (info_jezero_obrazovka_x + (50/2 - E_text.get_size()[0] / 2), 352))

    if pozadi == venek and stojim_u_shopu:
        info_shop_obrazovka_x = info_shop - kamera_x
        
        pygame.draw.rect(okno, cerna, (info_shop_obrazovka_x -1, 359, 52, 52))
        pygame.draw.rect(okno, (bila), (info_shop_obrazovka_x, 360, 50, 50))
        okno.blit(E_text, (info_shop_obrazovka_x + (50/2 - E_text.get_size()[0] / 2), 372))
    
    if pozadi == jezero and stojim_u_leva_lod and not prechod_lock_venek_a_jezero:
        pygame.draw.rect(okno, cerna, (21, 339, 52, 52)) 
        pygame.draw.rect(okno, (bila), (22, 340, 50, 50))
        okno.blit(E_text, (info_jezero_obrazovka_x + (50/2 - E_text.get_size()[0] / 2) - 700, 352))
    
    if pozadi == jezero and stojim_u_prava_lod:
        okno.blit(ikona_prut, (722, 290))
        pygame.draw.rect(okno, cerna, za_space_u_jezera)
        pygame.draw.rect(okno, bila, (722, 340, 50, 50))
        okno.blit(E_text, (info_jezero_obrazovka_x + (50/2 - E_text.get_size()[0] / 2), 352))
    
    if pozadi == venek and stojim_u_domu and not prechod_lock_dum_a_venek:
        pygame.draw.rect(okno, cerna, (info_dum_obrazovka_x - 1, 339, 52, 52))
        pygame.draw.rect(okno, bila, (info_dum_obrazovka_x, 340, 50, 50))
        okno.blit(E_text, (info_jezero_obrazovka_x + (50/2 - E_text.get_size()[0] / 2) - 1380, 352))
        
    if pozadi == dum and stojim_u_dveri and not prechod_lock_dum_a_venek:
        pygame.draw.rect(okno, cerna, (729, 339, 52, 52))
        pygame.draw.rect(okno, bila, (730, 340, 50, 50))
        okno.blit(E_text, (info_vnitrek_domu_obrazovka_x + (50/2 - E_text.get_size()[0] / 2) - 20, 352))
        
    if pozadi == dum and stojim_u_postele:
        pygame.draw.rect(okno, cerna,(info_vnitrek_domu_obrazovka_x - 225, 249,52,52))
        pygame.draw.rect(okno, bila, (info_vnitrek_domu_obrazovka_x - 224, 250,50,50))
        okno.blit(E_text, (info_vnitrek_domu_obrazovka_x + (50/2 - E_text.get_size()[0] / 2) - 224, 263))
    
    if pozadi == dum and stojim_u_krbu and not prechod_lock_dum_a_krb:
        pygame.draw.rect(okno, cerna,(info_vnitrek_domu_obrazovka_x - 625, 359,52,52))
        pygame.draw.rect(okno, bila, (info_vnitrek_domu_obrazovka_x - 624, 360,50,50))
        okno.blit(E_text, (info_vnitrek_domu_obrazovka_x + (50/2 - E_text.get_size()[0] / 2) - 624, 372))
    
    if pozadi == krb:
        pygame.draw.rect(okno, cerna, za_krb_leave)
        pygame.draw.rect(okno, hneda, krb_leave)
        krb_leave_text = krb_leave_font.render("EXIT", True, cerna)
        okno.blit(krb_leave_text, (697, 493))
    
    if pozadi == venek and stojim_u_cesty_venek and not prechod_lock_venek_a_rozcestnik:
        pygame.draw.rect(okno, cerna, (info_jezero_obrazovka_x - 1565, 339, 52, 52))
        pygame.draw.rect(okno, bila, (info_jezero_obrazovka_x - 1564, 340, 50, 50))
        okno.blit(E_text, (info_jezero_obrazovka_x - 1564 + (50/2 - E_text.get_size()[0] / 2), 352))
    
    hrac_obrazovka_x = hrac_pozice_x - kamera_x
    if pozadi != shop and pozadi != rybareni and pozadi != rybareni_dole and pozadi != rybareni_pozor and pozadi != krb and pozadi != bar and pozadi != barman and pozadi != slotmachine and pozadi != pozadi_shop_jidlo:
        okno.blit(aktualni_sprite, (hrac_obrazovka_x, hrac_pozice_y))
    

        
    if pozadi == shop and shop_mode is None:
        pygame.draw.rect(okno, cerna, za_koupit)
        pygame.draw.rect(okno, hneda, buy)
        pygame.draw.rect(okno, cerna, za_prodat)
        pygame.draw.rect(okno, hneda, sell)
        pygame.draw.rect(okno, cerna, za_opustit)
        pygame.draw.rect(okno, hneda, leave)
        okno.blit(buy_text, (180, 425))
        okno.blit(sell_text, (525, 425))
        okno.blit(leave_text, (687, 548))
        okno.blit(hlaska_text, (458, 262))
    
    if shop_mode == "buy":
        pozadi = pozadi_shop
        okno.blit(pozadi_shop, (0,0))
        hrac_rychlost = 0
        pygame.draw.rect(okno, cerna, za_opustit_buy)
        pygame.draw.rect(okno, hneda, leave_buy)
        okno.blit(leave_buy_text, (57, 548))
        upgrades_shop_text = upgrades_shop_font.render("UPGRADES", True, cerna)
        okno.blit(upgrades_shop_text, (282, 25))
        
        pygame.draw.rect(okno, cerna, za_kyblik_buy)
        pygame.draw.rect(okno, hneda, kyblik_buy)
        okno.blit(kyblik_buy_ikona, (kyblik_buy_pozice_x, kyblik_buy_pozice_y))
        pocet_upgradu_pro_kyblik = pocet_upgradu_font.render(f"{kyblik_lvl}/{max_upgrade_kybliku}", True, cerna)
        if kyblik_lvl < max_upgrade_kybliku:
            cena_buy_upgradu_kyblik = coins_cena_buy_font.render(f"{kyblik_cena}", True, zluta)
            okno.blit(cena_buy_upgradu_kyblik, (kyblik_buy_pozice_x + 70, kyblik_buy_pozice_y + upgrady_velikost_y -50))
            okno.blit(coin_ikona, (kyblik_buy_pozice_x + 40, kyblik_buy_pozice_y + upgrady_velikost_y -50))
        else:
            Max_kyblik = pocet_upgradu_font.render("MAX", True, cervena)
            okno.blit(Max_kyblik, (kyblik_buy_pozice_x + 60, kyblik_buy_pozice_y + upgrady_velikost_y -40))

        okno.blit(pocet_upgradu_pro_kyblik,(kyblik_buy_pozice_x + 135, kyblik_buy_pozice_y + upgrady_velikost_y - 20))
        
        
        pygame.draw.rect(okno, cerna, za_zmacknuti_buy)
        pygame.draw.rect(okno, hneda, zmacknuti_buy)
        okno.blit(zmacknuti_buy_ikona, (zmacknuti_buy_pozice_x, zmacknuti_buy_pozice_y))
        pocet_upgradu_pro_zmacknuti = pocet_upgradu_font.render(f"{zmacknuti_lvl}/{max_upgrade_zmacknuti}", True, cerna)
        if zmacknuti_lvl < max_upgrade_zmacknuti:
            cena_buy_upgradu_zmacknuti = coins_cena_buy_font.render(f"{zmacknuti_cena}", True, zluta)
            okno.blit(cena_buy_upgradu_zmacknuti, (zmacknuti_buy_pozice_x + 70, zmacknuti_buy_pozice_y + upgrady_velikost_y -50))
            okno.blit(coin_ikona, (zmacknuti_buy_pozice_x + 40, zmacknuti_buy_pozice_y + upgrady_velikost_y -50))
        else:
            Max_zmacknuti = pocet_upgradu_font.render("MAX", True, cervena)
            okno.blit(Max_zmacknuti, (zmacknuti_buy_pozice_x + 60, zmacknuti_buy_pozice_y + upgrady_velikost_y - 40))
                
        okno.blit(pocet_upgradu_pro_zmacknuti,(zmacknuti_buy_pozice_x + 135, zmacknuti_buy_pozice_y + upgrady_velikost_y - 20))
        
        
        pygame.draw.rect(okno, cerna, za_cekani_buy)
        pygame.draw.rect(okno, hneda, cekani_buy)
        okno.blit(cekani_buy_ikona, (cekani_buy_pozice_x, cekani_buy_pozice_y))
        pocet_upgradu_pro_cekani = pocet_upgradu_font.render(f"{cekani_lvl}/{max_upgrade_cekani}", True, cerna)
        if cekani_lvl < max_upgrade_cekani:
            cena_buy_upgradu_cekani = coins_cena_buy_font.render(f"{cekani_cena}", True, zluta)
            okno.blit(cena_buy_upgradu_cekani, (cekani_buy_pozice_x + 70, cekani_buy_pozice_y + upgrady_velikost_y -50))
            okno.blit(coin_ikona, (cekani_buy_pozice_x + 40, cekani_buy_pozice_y + upgrady_velikost_y - 50))
        else:
            Max_cekani = pocet_upgradu_font.render("MAX", True, cervena)
            okno.blit(Max_cekani, (cekani_buy_pozice_x + 60, cekani_buy_pozice_y + upgrady_velikost_y - 40))
 
        okno.blit(pocet_upgradu_pro_cekani,(cekani_buy_pozice_x + 135, cekani_buy_pozice_y + upgrady_velikost_y - 20))
        
        baits_shop_text = baits_shop_font.render("BAITS",  True, cerna)
        okno.blit(baits_shop_text, (335, 245))
        pygame.draw.rect(okno, cerna, za_baits_pozadi)
        pygame.draw.rect(okno, hneda, baits_pozadi)
        
        
        pygame.draw.rect(okno, cerna, za_bread_bait)
        pygame.draw.rect(okno, hneda, bread_bait)
        cena_buy_bait_bread = buy_baits_cena_font.render(f"{bread_bait_cena}", True, zluta)
        okno.blit(cena_buy_bait_bread, (bread_bait_pozice_x + 50, bread_bait_pozice_y + 170))
        okno.blit(coin_ikona, ( bread_bait_pozice_x + 15, bread_bait_pozice_y +170))
        vykresli_popis_baitu(
            baits["bread"],
            bread_bait_pozice_x + 5,
            bread_bait_pozice_y + 50
        )
        okno.blit(bread_bait_ikona, (bread_bait_pozice_x + 10, bread_bait_pozice_y + 20))
        
        pygame.draw.rect(okno, cerna, za_worm_bait)
        pygame.draw.rect(okno, hneda, worm_bait)
        cena_buy_bait_worm = buy_baits_cena_font.render(f"{worm_bait_cena}", True, zluta)
        okno.blit(cena_buy_bait_worm, (worm_bait_pozice_x + 50, worm_bait_pozice_y + 170))
        okno.blit(coin_ikona, (worm_bait_pozice_x + 15, worm_bait_pozice_y + 170))
        vykresli_popis_baitu(
            baits["worm"],
            worm_bait_pozice_x + 5,
            worm_bait_pozice_y + 50
        )
        okno.blit(worm_bait_ikona, (worm_bait_pozice_x + 10, worm_bait_pozice_y + 20))
        
        pygame.draw.rect(okno, cerna, za_corn_bait)
        pygame.draw.rect(okno, hneda, corn_bait)
        cena_buy_bait_corn = buy_baits_cena_font.render(f"{corn_bait_cena}", True, zluta)
        okno.blit(cena_buy_bait_corn, (corn_bait_pozice_x + 50, corn_bait_pozice_y + 170))
        okno.blit(coin_ikona, (corn_bait_pozice_x + 15, corn_bait_pozice_y + 170))
        vykresli_popis_baitu(
            baits["corn"],
            corn_bait_pozice_x + 5,
            corn_bait_pozice_y + 50
        )
        okno.blit(corn_bait_ikona, (corn_bait_pozice_x + 10, corn_bait_pozice_y + 20))
        
        pygame.draw.rect(okno, cerna, za_fish_head_bait)
        pygame.draw.rect(okno, hneda, fish_head_bait)
        cena_buy_bait_fish_head = buy_baits_cena_font.render(f"{fish_head_bait_cena}", True, zluta)
        okno.blit(cena_buy_bait_fish_head, (fish_head_bait_pozice_x + 50, fish_head_bait_pozice_y + 170))
        okno.blit(coin_ikona, (fish_head_bait_pozice_x + 15, fish_head_bait_pozice_y + 170))
        vykresli_popis_baitu(
            baits["fish_head"],
            fish_head_bait_pozice_x + 5,
            fish_head_bait_pozice_y + 50
        )
        okno.blit(fish_head_bait_ikona, (fish_head_bait_pozice_x + 10, fish_head_bait_pozice_y + 20))
        
        pygame.draw.rect(okno, cerna, za_baits_upgrade)
        pygame.draw.rect(okno, hneda, baits_upgrade)
        okno.blit(baits_upgrade_ikona, (baits_upgrade_pozice_x + 12, baits_upgrade_pozice_y + 20))
        baits_upgrade_cena_text = buy_baits_cena_font.render(f"{baits_upgrade_cena}", True, zluta)
        max_baits_v_shopu = info_o_baits_font.render(f"Current: x{obsah_baits_max}", True, cerna)
        okno.blit(max_baits_v_shopu, (baits_upgrade_pozice_x + 23, baits_pozadi_pozice_y + 140))
        if baits_lvl < max_upgrade_baits:
            okno.blit(baits_upgrade_cena_text, (baits_upgrade_pozice_x + 50, baits_upgrade_pozice_y +170))
            okno.blit(coin_ikona, (baits_upgrade_pozice_x + 15, baits_upgrade_pozice_y + 170))
        else:
            Max_cekani = pocet_upgradu_font.render("MAX", True, cervena)
            okno.blit(Max_cekani, (baits_upgrade_pozice_x + 37, baits_upgrade_pozice_y + 170))
            
        pocet_upgradu_pro_baits = pocet_upgradu_font.render(f"{baits_lvl}/{max_upgrade_baits}", True, cerna)
        okno.blit(pocet_upgradu_pro_baits, (baits_upgrade_pozice_x + 90, baits_upgrade_pozice_y))
            
            
        for jmeno, x, y in bait_ui:
            pocet = baits[jmeno]["pocet"]
            text = info_o_baits_font.render(f"x{pocet}", True, cerna)
            okno.blit(text, (x + 5, y + 5))
          
    if pozadi == pozadi_shop and shop_mode == "buy":
        if leave_buy.collidepoint(mys_pozice) and mouse_click:
            pozadi = shop
            shop_mode = None
            pygame.draw.rect(okno, cerna, za_koupit)
            pygame.draw.rect(okno, hneda, buy)
            pygame.draw.rect(okno, cerna, za_prodat)
            pygame.draw.rect(okno, hneda, sell)
            pygame.draw.rect(okno, cerna, za_opustit)
            pygame.draw.rect(okno, hneda, leave)
            okno.blit(buy_text, (180, 425))
            okno.blit(sell_text, (525, 425))
            okno.blit(leave_text, (687, 548))
            okno.blit(hlaska_text, (458, 262))
    
    
    if shop_mode == "sell":
        pozadi = pozadi_shop
        okno.blit(pozadi_shop, (0,0))
        hrac_rychlost = 0
        pygame.draw.rect(okno, cerna, za_opustit_sell)
        pygame.draw.rect(okno, hneda, leave_sell)
        okno.blit(leave_sell_text, (57, 548))
        
        pygame.draw.rect(okno, cerna, za_plechovka_sell)
        pygame.draw.rect(okno, hneda, plechovka_sell)
        pocet_plechovek = obsah_inventare["Plechovka"]
        cislo_u_plechovky_text = cislo_u_polozky_font.render(str(pocet_plechovek), True, cerna)
        okno.blit(cislo_u_plechovky_text, (sell_plechovka_pozice_x + polozky_velikost_x - 25, sell_plechovka_pozice_y + polozky_velikost_y - 25))
        okno.blit(plechovka, (sell_plechovka_pozice_x, sell_plechovka_pozice_y + 5))
        rarita_text_common_plechovka = rarita_font.render("COMMON", True, Sseda)
        okno.blit(rarita_text_common_plechovka, (sell_plechovka_pozice_x + 8, sell_plechovka_pozice_y + 102))
        popis_plechovky_text = popis_polozky_font.render("TIN", True, cerna)
        okno.blit(popis_plechovky_text, (sell_plechovka_pozice_x + polozky_velikost_x - popis_polozky_velikost - 42, sell_plechovka_pozice_y + 10))
        predmet_plechovka = najdi_predmet_podle_jmena(predmety, "Plechovka")
        hodnota_plechovky_text = hodnota_polozky_font.render(str(predmet_plechovka["cena"]), True, zluta)
        okno.blit(hodnota_plechovky_text, (sell_plechovka_pozice_x + polozky_velikost_x / 2 + 42, sell_plechovka_pozice_y + 45))
        okno.blit(coin_ikona, (sell_plechovka_pozice_x + polozky_velikost_x / 2 + 72, sell_plechovka_pozice_y + 45))
        
        pygame.draw.rect(okno, cerna, za_bota_sell)
        pygame.draw.rect(okno, hneda, bota_sell)
        pocet_bot = obsah_inventare["Bota"]
        cislo_u_boty_text = cislo_u_polozky_font.render(str(pocet_bot), True, cerna)
        okno.blit(cislo_u_boty_text, (sell_bota_pozice_x + polozky_velikost_x - 25, sell_bota_pozice_y + polozky_velikost_y - 25))
        okno.blit(bota, (sell_bota_pozice_x + 8, sell_bota_pozice_y ))
        rarita_text_uncommon_bota = rarita_font.render("UNCOMMON", True, zelena)
        okno.blit(rarita_text_uncommon_bota, (sell_bota_pozice_x + 8, sell_bota_pozice_y + 102))
        popis_boty_text = popis_polozky_font.render("BOOT", True, cerna)
        okno.blit(popis_boty_text, (sell_bota_pozice_x + polozky_velikost_x - popis_polozky_velikost - 42, sell_bota_pozice_y + 10))
        predmet_bota = najdi_predmet_podle_jmena(predmety, "Bota")
        hodnota_boty_text = hodnota_polozky_font.render(str(predmet_bota["cena"]), True, zluta)
        okno.blit(hodnota_boty_text, (sell_bota_pozice_x + polozky_velikost_x / 2 + 42, sell_bota_pozice_y + 45))
        okno.blit(coin_ikona, (sell_bota_pozice_x + polozky_velikost_x / 2 + 72, sell_bota_pozice_y + 45))

        pygame.draw.rect(okno, cerna, za_kapr_sell)
        pygame.draw.rect(okno, hneda, kapr_sell)
        pocet_kapru = obsah_inventare["Kapr"]
        cislo_u_kapra_text = cislo_u_polozky_font.render(str(pocet_kapru), True, cerna)
        okno.blit(cislo_u_kapra_text, (sell_kapr_pozice_x + polozky_velikost_x - 25, sell_kapr_pozice_y + polozky_velikost_y - 25))
        okno.blit(kapr, (sell_kapr_pozice_x + 5 , sell_kapr_pozice_y ))
        rarita_text_rare_kapr = rarita_font.render("RARE", True, modra)
        okno.blit(rarita_text_rare_kapr, (sell_kapr_pozice_x + 8, sell_kapr_pozice_y + 102))
        popis_kapra_text = popis_polozky_font.render("CARP", True, cerna)
        okno.blit(popis_kapra_text, (sell_kapr_pozice_x + polozky_velikost_x - popis_polozky_velikost - 42, sell_kapr_pozice_y + 10))
        predmet_kapr = najdi_predmet_podle_jmena(predmety, "Kapr")
        hodnota_kapra_text = hodnota_polozky_font.render(str(predmet_kapr["cena"]), True, zluta)
        okno.blit(hodnota_kapra_text, (sell_kapr_pozice_x + polozky_velikost_x / 2 + 30, sell_kapr_pozice_y + 45))
        okno.blit(coin_ikona, (sell_kapr_pozice_x + polozky_velikost_x / 2 + 72, sell_kapr_pozice_y + 45))

        pygame.draw.rect(okno, cerna, za_stika_sell)
        pygame.draw.rect(okno, hneda, stika_sell)
        pocet_stik = obsah_inventare["Štika"]
        cislo_u_stiky_text = cislo_u_polozky_font.render(str(pocet_stik), True, cerna)
        okno.blit(cislo_u_stiky_text, (sell_stika_pozice_x + polozky_velikost_x - 25, sell_stika_pozice_y + polozky_velikost_y -25))
        okno.blit(stika, (sell_stika_pozice_x + 5 , sell_stika_pozice_y))
        rarita_text_epic_stika = rarita_font.render("EPIC", True, fialova)
        okno.blit(rarita_text_epic_stika, (sell_stika_pozice_x + 8, sell_stika_pozice_y + 102))   
        popis_stiky_text = popis_polozky_font.render("PIKE", True, cerna)
        okno.blit(popis_stiky_text, (sell_stika_pozice_x + polozky_velikost_x - popis_polozky_velikost - 42, sell_stika_pozice_y + 10))
        predmet_stika = najdi_predmet_podle_jmena(predmety, "Štika")
        hodnota_stiky_text = hodnota_polozky_font.render(str(predmet_stika["cena"]), True, zluta)
        okno.blit(hodnota_stiky_text, (sell_stika_pozice_x + polozky_velikost_x / 2 + 30, sell_stika_pozice_y + 45))
        okno.blit(coin_ikona, (sell_stika_pozice_x + polozky_velikost_x / 2 + 75, sell_stika_pozice_y + 45))
        
        pygame.draw.rect(okno, cerna, za_sumec_sell)
        pygame.draw.rect(okno, hneda, sumec_sell)
        pocet_sumcu = obsah_inventare["Sumec"]
        cislo_u_sumce_text = cislo_u_polozky_font.render(str(pocet_sumcu), True, cerna)
        okno.blit(cislo_u_sumce_text, (sell_sumec_pozice_x + polozky_velikost_x -25, sell_sumec_pozice_y + polozky_velikost_y - 25))
        okno.blit(sumec, (sell_sumec_pozice_x + 5 , sell_sumec_pozice_y ))
        rarita_text_epic_sumec = rarita_font.render("EPIC", True, fialova)
        okno.blit(rarita_text_epic_sumec, (sell_sumec_pozice_x + 8, sell_sumec_pozice_y + 102))
        popis_sumce_text = popis_polozky_font.render("CATFISH", True, cerna)
        okno.blit(popis_sumce_text, (sell_sumec_pozice_x + polozky_velikost_x - popis_polozky_velikost - 60, sell_sumec_pozice_y + 10))
        predmet_sumec = najdi_predmet_podle_jmena(predmety, "Sumec")
        hodnota_sumce_text = hodnota_polozky_font.render(str(predmet_sumec["cena"]), True, zluta)
        okno.blit(hodnota_sumce_text, (sell_sumec_pozice_x + polozky_velikost_x / 2 + 30, sell_sumec_pozice_y + 45))
        okno.blit(coin_ikona, (sell_sumec_pozice_x + polozky_velikost_x / 2 + 75, sell_sumec_pozice_y + 45))
        
        pygame.draw.rect(okno, cerna, za_tajnaRyba_sell)
        pygame.draw.rect(okno, hneda, tajnaRyba_sell)
        pocet_raku = obsah_inventare["Rak"]
        cislo_u_raka_text = cislo_u_polozky_font.render(str(pocet_raku), True, cerna)
        okno.blit(cislo_u_raka_text, (sell_tajnaRyba_pozice_x + polozky_velikost_x - 25, sell_tajnaRyba_pozice_y + polozky_velikost_y - 25))
        okno.blit(tajnaRyba, (sell_tajnaRyba_pozice_x + 5 , sell_tajnaRyba_pozice_y ))
        rarita_text_legendary_rak = rarita_font.render("LEGENDARY", True, zluta)
        okno.blit(rarita_text_legendary_rak, (sell_tajnaRyba_pozice_x + 8, sell_tajnaRyba_pozice_y + 102))
        popis_tajnaRyba_text = popis_polozky_font.render("???", True, cerna)
        okno.blit(popis_tajnaRyba_text, (sell_tajnaRyba_pozice_x + polozky_velikost_x - popis_polozky_velikost - 42, sell_tajnaRyba_pozice_y + 10))
        predmet_tajnaRyba = najdi_predmet_podle_jmena(predmety, "Rak")
        hodnota_tajnaRyba_text = hodnota_polozky_font.render(str(predmet_tajnaRyba["cena"]), True, zluta)
        okno.blit(hodnota_tajnaRyba_text, (sell_tajnaRyba_pozice_x + polozky_velikost_x / 2 + 25, sell_tajnaRyba_pozice_y + 45))
        okno.blit(coin_ikona, (sell_tajnaRyba_pozice_x + polozky_velikost_x / 2 + 75, sell_tajnaRyba_pozice_y + 45))
        
    
    if pozadi == pozadi_shop and shop_mode == "sell":
        if leave_sell.collidepoint(mys_pozice) and mouse_click:
            pozadi = shop
            shop_mode = None
            pygame.draw.rect(okno, cerna, za_koupit)
            pygame.draw.rect(okno, hneda, buy)
            pygame.draw.rect(okno, cerna, za_prodat)
            pygame.draw.rect(okno, hneda, sell)
            pygame.draw.rect(okno, cerna, za_opustit)
            pygame.draw.rect(okno, hneda, leave)
            okno.blit(buy_text, (180, 425))
            okno.blit(sell_text, (525, 425))
            okno.blit(leave_text, (687, 548))
            okno.blit(hlaska_text, (458, 262))

    
    coins_text = coins_font.render(f":{coins}", True, zluta)
    okno.blit(coins_text, (55, 20))
    okno.blit(coin_ikona, (20, 20))
    
    if not inventar and pozadi != shop and pozadi != pozadi_shop and not prut and not minihra and pozadi != slotmachine:
        okno.blit(ikona_inv, (700, 20))
        
    if inventar:
        if kyblik_lvl == 0:   
            okno.blit(inv, (0, 0,))
        if kyblik_lvl == 1:
            okno.blit(inv2, (0, 0))
        if kyblik_lvl == 2:
            okno.blit(inv3, (0,0))
        if kyblik_lvl == 3:
            okno.blit(inv4, (0,0))
        pygame.draw.rect(okno, seda, (412 - inventory_tlacitko_velikost, 516, inventory_tlacitko_velikost + 2, inventory_tlacitko_velikost + 2)) # za tlacitko
        pygame.draw.rect(okno, Sseda, (413 - inventory_tlacitko_velikost, 517, inventory_tlacitko_velikost, inventory_tlacitko_velikost)) # tlacitko
        coins_text = coins_font.render(f":{coins}", True, zluta)
        okno.blit(coins_text, (530, 545))
        okno.blit(coin_ikona, (500, 545))
        inventory_upgrades_text = upgrades_inventory_font.render("Upgrades:", True, cerna)
        okno.blit(inventory_upgrades_text, (51 + 10, 422 + 10))
        
        inventory_info_kyblik_cislo = inventory_info_font.render(f"{obsah_inventare_max}", True, cerna)
        inventory_info_kyblik_text = inventory_info_font.render("Maximum inventory slot:", True, cerna)
        okno.blit(inventory_info_kyblik_text, (51 + 10, 442 + 10))
        okno.blit(inventory_info_kyblik_cislo, (51 +  200, 442 + 10 ))
        
        inventory_info_zmacknuti_cislo = inventory_info_font.render(f"{zmacknuti_lvl}", True, cerna)
        inventory_info_kyblik_text = inventory_info_font.render("Fewer presses:", True, cerna)
        okno.blit(inventory_info_kyblik_text, (51+ 10, 452 + 20))
        okno.blit(inventory_info_zmacknuti_cislo, (51 + 200, 452 + 20))

        inventory_info_cekani_cislo = inventory_info_font.render(f"- {momentalni_cekani / 10} s", True, cerna)
        inventory_info_cekani_text = inventory_info_font.render("Shorter waiting time:", True, cerna)
        okno.blit(inventory_info_cekani_text, (51 + 10, 472 + 20))
        okno.blit(inventory_info_cekani_cislo, (51 + 193, 472 + 20))
        
        pocet_upgradu_pro_baits = inventory_info_font.render(f"{obsah_baits_max}", True, cerna)
        pocet_upgradu_pro_baits_text = inventory_info_font.render("Max baits amount:", True, cerna)
        okno.blit(pocet_upgradu_pro_baits, (51 + 200, 492 + 20))
        okno.blit(pocet_upgradu_pro_baits_text, (51 + 10, 492 + 20))
        
        
        if baits_mode == None:
            okno.blit(bread_inventory_ikona, (510, 440))
            okno.blit(worm_inventory_ikona, (570, 440))
            okno.blit(corn_inventory_ikona, (630, 440))
            okno.blit(fish_head_inventory_ikona, (690, 440))
            for jmeno, x, y in bait_ui_inv:
                pocet = baits[jmeno]["pocet"]
                text = info_o_baits_font.render(f"x{pocet}", True, cerna)
                okno.blit(text, (x + 5, y + 5))
            pygame.draw.rect(okno, cerna, za_bread_tlacitko_inventory)
            pygame.draw.rect(okno, zelena, bread_tlacitko_inventory)
            
            pygame.draw.rect(okno, cerna, za_worm_tlacitko_inventory)
            pygame.draw.rect(okno, zelena, worm_tlacitko_inventory)

            pygame.draw.rect(okno, cerna, za_corn_tlacitko_inventory)
            pygame.draw.rect(okno, zelena, corn_tlacitko_inventory)
            
            pygame.draw.rect(okno, cerna, za_fish_head_tlacitko_inventory)
            pygame.draw.rect(okno, zelena, fish_head_tlacitko_inventory)
        
        if inventar and baits_mode is not None:
            vykresli_popis_baitu(
                baits_mode,
                580,   # X – uprav si podle UI
                400    # Y – klidně níž/výš
            )
        
        if baits_mode == baits["bread"]:
            okno.blit(bread_inventory_ikona, (510, 440))
            pocet = baits["bread"]["pocet"]
            text = info_o_baits_font.render(f"x{pocet}", True, cerna)
            okno.blit(text, (510, 425))
            pygame.draw.rect(okno, cerna, za_bait_leave_tlacitko_inventory)
            pygame.draw.rect(okno, cervena, (bait_leave_tlacitko_inventory))
                
        if baits_mode == baits["worm"]:
            okno.blit(worm_inventory_ikona, (510, 440))
            pocet = baits["worm"]["pocet"]
            text = info_o_baits_font.render(f"x{pocet}", True, cerna)
            okno.blit(text, (510, 425))
            pygame.draw.rect(okno, cerna, za_bait_leave_tlacitko_inventory)
            pygame.draw.rect(okno, cervena, bait_leave_tlacitko_inventory)
            
        if baits_mode == baits["corn"]:
            okno.blit(corn_inventory_ikona, (510, 440))
            pocet = baits["corn"]["pocet"]
            text = info_o_baits_font.render(f"x{pocet}", True, cerna)
            okno.blit(text, (510, 425))
            pygame.draw.rect(okno, cerna, za_bait_leave_tlacitko_inventory)
            pygame.draw.rect(okno, cervena, bait_leave_tlacitko_inventory)
        
        if baits_mode == baits["fish_head"]:
            okno.blit(fish_head_inventory_ikona, (510, 440))
            pocet = baits["fish_head"]["pocet"]
            text = info_o_baits_font.render(f"x{pocet}", True, cerna)
            okno.blit(text, (510, 425))
            pygame.draw.rect(okno, cerna, za_bait_leave_tlacitko_inventory)
            pygame.draw.rect(okno, cervena, bait_leave_tlacitko_inventory)




    if not inventar and pozadi == rybareni:
        hrac_rychlost = 0
    if inventar and pozadi == rybareni:
        hrac_rychlost = 0
    
    if zpet_tlacitko and not inventar:
        pygame.draw.rect(okno, cerna, (4, 479, 102, 52))
        zpet_tlacitko_rect = pygame.draw.rect(okno, bila, (5, 480, 100, 50))
        okno.blit(zpet_tlacitko_text, (21, 492))
        


    
    if minihra:
        center = (okraj_random_x, okraj_random_y)
        radius = 22

        pygame.draw.circle(okno, cerna, center, radius + 3)
        pygame.draw.circle(okno, bila, center, radius)

        text_rect = pismeno_text.get_rect(center=center)
        okno.blit(pismeno_text, text_rect)
    
    if pozadi == rybareni and not prut and not minihra and not inventar and (baits_mode is None or baits_mode["pocet"] == 0) and stisknuto[pygame.K_SPACE]:
        no_baits_text = plny_inv_font.render("NO BAITS!", True, cervena)
        no_baits_upozorneni_rect = no_baits_text.get_rect(center=(okno_sirka // 2, 340))
        okno.blit(no_baits_text, no_baits_upozorneni_rect)
    
    if plny_inventar_upozorneni and pozadi == rybareni and not inventar:
        plny_inventar_upozorneni_rect = plny_inv_text.get_rect(center=(okno_sirka // 2, 280))
        okno.blit(plny_inv_text, plny_inventar_upozorneni_rect)
        if pygame.time.get_ticks() - plny_inventar_cas > plny_inventar_doba:
            plny_inventar_upozorneni = False
    
    
    if pozadi == rybareni and not prut and not minihra and not inventar:
        if posledni_ulovek and pygame.time.get_ticks() - posledni_ulovek_cas < posledni_ulovek_doba:
                x = 640
                y = 440
                okno.blit(posledni_ulovek["obrazek"], (x, y))
                okno.blit(plus_ikona, (x - 40, y + 25))
 
        else:
            posledni_ulovek = None
        pocet_snimku = 10
        faktor_zpozdeni = 10
        
        space_to_fish_text_rect = space_to_fish_text.get_rect(center=(okno_sirka // 2, 80))
        
        if pocitadlo % (pocet_snimku * faktor_zpozdeni) < 5 * faktor_zpozdeni:
            okno.blit(space_to_fish_text, space_to_fish_text_rect)

        elif pocitadlo % (pocet_snimku * faktor_zpozdeni) < 6 * faktor_zpozdeni:
            okno.blit(space_to_fish_text, (1000, 1000))
    
    if inventar:
        vylovene_predmety = []
        for p in inventar_order:
                if len(vylovene_predmety) < odemcene_sloty:
                    vylovene_predmety.append(p["obrazek"])

    if inventar:
        for i, obrazek in enumerate(sloty):
            if i < len(vylovene_predmety):
                obrazek = vylovene_predmety[i]
                okno.blit(obrazek, sloty[i].topleft)
    
    
    
    clock.tick(60)
    pygame.display.flip()
    
    