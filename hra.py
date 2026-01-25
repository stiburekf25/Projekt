import pygame
import sys
import random
pygame.init()

# PRIPRAVA HRY

def vyber_predmet(predmety):
    los = random.randint(1, 100)
    for p in predmety:
        if p["sance"] >= los:
            return p
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

hrac_pozice_x = 400
hrac_pozice_y = 315
hrac_rychlost = 4
hrac_velikostX= 110
hrac_velikostY = 170

info_jezero = 1570
info_shop = 920

kamera_x = 0

soubor = open("shop.txt", "r", encoding="utf-8")

seznam_vet = []

for radek in soubor:
    seznam_vet.append(radek[:-1])

soubor.close()

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
        "cena": 20,
        "obrazek": pygame.image.load("plechovka.png"),
    },
    {
        "jmeno": "Bota",
        "sance": 65,
        "cekani": 5000,
        "zmacknuti": 7,
        "limit_cekani": 2500,
        "cena": 40,
        "obrazek": pygame.image.load("bota.png"),
    },
    {
        "jmeno": "Kapr",
        "sance": 80,
        "cekani": 6000,
        "zmacknuti": 12,
        "limit_cekani": 2000,
        "cena": 80,
        "obrazek": pygame.image.load("kapr.png"),
    },
    {
        "jmeno": "Štika",
        "sance": 90,
        "cekani": 7000,
        "zmacknuti": 15,
        "limit_cekani": 1300,
        "cena": 130,
        "obrazek": pygame.image.load("stika.png"),
    },
    {
        "jmeno": "Sumec",
        "sance": 97,
        "cekani": 11000,
        "zmacknuti": 18,
        "limit_cekani": 1000,
        "cena": 250,
        "obrazek": pygame.image.load("sumec.png"),
    },
    {
        "jmeno": "Rak",
        "sance": 100,
        "cekani": 9000,
        "zmacknuti": 23,
        "limit_cekani": 1100,
        "cena": 600,
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
info_o_baits_velikost = 20
inventory_baits_tlacitko_velikost = 30


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

        surface = info_o_baits_font.render(
            f"{text}: {hodnota}", True, cerna
        )

        okno.blit(surface, (x, y + 40 +i * 20))


baits = {
    "bread": {
        "pocet":0,
        "lepsi_sance":-5, #horsi
        "kratsi_cekani":0.5, #horsi
        "mene_zmacknuti": 0,     #normal  
    },
    "worm": {
        "pocet":0,
        "lepsi_sance":+5, #lepsi
        "kratsi_cekani":-0.2, # lepsi
        "mene_zmacknuti": 0, #normal   
    },
    "corn": {
        "pocet":0,
        "lepsi_sance":+5,
        "kratsi_cekani": 0.5, # horsi
        "mene_zmacknuti": - 1,  # lepsi
        
    },
    "fish_head": {
        "pocet":0,
        "lepsi_sance": +10, # lepsi
        "kratsi_cekani": - 1, # lepsi
        "mene_zmacknuti": - 2, # lepsi
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
    ("lepsi_sance", "Luck"),
    ("kratsi_cekani", "Wait time"),
    ("mene_zmacknuti", "presses"),
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
venek = pygame.image.load("venek.png")
jezero = pygame.image.load("level_2.png")
shop = pygame.image.load("shop.png")
pozadi_shop = pygame.image.load("pozadi_shop.png")
rybareni = pygame.image.load("rybareni.png")
ikona_prut = pygame.image.load("ikona_prut.png")
rybareni_dole = pygame.image.load("rybareni_dole.png")
rybareni_pozor = pygame.image.load("rybareni_pozor.png")

pozadi = venek
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
#TEXTURAinv = pygame.transform.scale(inv, (500, 300))
ikona_inv = pygame.image.load("ikona_inv.png") # x 70 y 80
ikona_inv_rect = ikona_inv.get_rect(topleft=(700, 20))
tlacitko = pygame.draw.rect(okno, Sseda, (413 - inventory_tlacitko_velikost, 517 ,inventory_tlacitko_velikost, inventory_tlacitko_velikost))
za_tlacitko = pygame.draw.rect(okno, seda, (412 - inventory_tlacitko_velikost, 516, inventory_tlacitko_velikost, inventory_tlacitko_velikost))


        #okno.blit(worm_inventory_ikona, (570, 440))
        #okno.blit(corn_inventory_ikona, (630, 440))
        #okno.blit(fish_head_inventory_ikona, (690, 440))
                                      

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

hlaska_font = pygame.font.SysFont("Aharoni", hlaska_velikost)
shop_hlaska = random.choice(seznam_vet)
hlaska_text = hlaska_font.render(shop_hlaska, True, cerna)

# CYKLICKE VYKRESLOVANI FRAMU HRY

while True:

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
    #klik = pygame.mouse.get_pressed()

    
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
        hrac_pozice_x += hrac_rychlost

    elif stisknuto[pygame.K_a]:
        if pocitadlo % (pocet_snimku * faktor_zpozdeni) < faktor_zpozdeni:
            aktualni_sprite = TEXTURApepa_1

        else:
            aktualni_sprite = TEXTURApepa_2
        hrac_pozice_x -= hrac_rychlost
    
    #VENEK
    
    if pozadi == venek:
        if hrac_pozice_x < 190:
            hrac_pozice_x = 190
        if hrac_pozice_x > pozadi_sirka - hrac_velikostX - 170:
            hrac_pozice_x = pozadi_sirka - hrac_velikostX - 170
                
            
        if hrac_obrazovka_x > prava_zona:
            kamera_x += hrac_rychlost
        if hrac_obrazovka_x < leva_zona:
            kamera_x -= hrac_rychlost
                
        if kamera_x < 0:
            kamera_x = 0
        if kamera_x > pozadi_sirka - okno_sirka:
            kamera_x = pozadi_sirka - okno_sirka 

        info_shop_obrazovka_x = info_shop - kamera_x

        
        stojim_u_jezera = hrac_pozice_x > 1320 and hrac_pozice_x < 1450
        
        #Vstup na jezero
        
        if stojim_u_jezera and stisknuto[pygame.K_e] and not inventar:
            pozadi = jezero
            
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
            hrac_pozice_x = 370
            hrac_pozice_y = 320
            hrac_velikostX= 110
            hrac_velikostY = 170
            hrac_rychlost = 4
            
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
        
        if stojim_u_leva_lod and stisknuto[pygame.K_e] and not inventar:
            pozadi = venek
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()

            hrac_pozice_x = 1312
            hrac_pozice_y = 315

            hrac_velikostX = 110
            hrac_velikostY = 170
            hrac_rychlost = 4

            kamera_x = 848

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
   
    if pozadi == rybareni and stisknuto[pygame.K_SPACE] and not (prut or minihra) and not inventar:
        if sum(obsah_inventare.values()) < obsah_inventare_max:
            pozadi = rybareni_dole
            hrac_rychlost = 0
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
            prut = True
            zpet_tlacitko = False
            ulovek = vyber_predmet(predmety)
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
        
        for pismeno in range(ulovek["zmacknuti"]):
            pismneko_ktere_zkousime_davat_do_sekvence = chr(random.randint(97, 97 + 25))
            while sekvence != "" and sekvence[-1] == pismneko_ktere_zkousime_davat_do_sekvence:
                pismneko_ktere_zkousime_davat_do_sekvence = chr(random.randint(97, 97 + 25))
            sekvence += pismneko_ktere_zkousime_davat_do_sekvence
        #print(sekvence)
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
            print(obsah_inventare)
                   
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

    
    #Omezeni otevirani inv v shopu a v buy and sell
    
    if pozadi != shop and pozadi != pozadi_shop:
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
            baits_mode = "bait_bread"

        elif worm_tlacitko_inventory.collidepoint(mys_pozice) and mouse_click:
            baits_mode = "bait_worm"

        elif corn_tlacitko_inventory.collidepoint(mys_pozice) and mouse_click:
            baits_mode = "bait_corn"
        
        elif fish_head_tlacitko_inventory.collidepoint(mys_pozice) and mouse_click:
            baits_mode = "bait_fish_head"
    
    if inventar and baits_mode is not None:
        if bait_leave_tlacitko_inventory.collidepoint(mys_pozice) and mouse_click:
            baits_mode = None



    #Kurzor na hand nebo arrow podle urciteho pozadi ci podminky
    
    kurzor_hand = False 

                
    if pozadi == pozadi_shop and leave_buy.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif pozadi == shop and (buy.collidepoint(mys_pozice) or sell.collidepoint(mys_pozice) or leave.collidepoint(mys_pozice)):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif pozadi == pozadi_shop and leave_sell.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif ikona_inv_rect.collidepoint(mys_pozice)and not inventar and not pozadi == shop and not pozadi == pozadi_shop and not minihra and not prut:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif tlacitko.collidepoint(mys_pozice) and inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif zpet_tlacitko_rect.collidepoint(mys_pozice) and not prut and not minihra and not pozadi == jezero and not pozadi == shop and not pozadi == venek and not shop_mode == "buy" and not shop_mode == "sell" and not inventar:
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
    else:         
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    # VYKRESLENI PRVKU HRY
    

    if pozadi != shop:
        okno.blit(pozadi, (-kamera_x, 0))
    else:
        okno.blit(pozadi, (0, 0))
    
    if pozadi == venek and stojim_u_jezera:
        pygame.draw.rect(okno, cerna, za_e_u_jezera)
        pygame.draw.rect(okno, (bila), (info_jezero_obrazovka_x, 340, 50, 50))
        okno.blit(E_text, (info_jezero_obrazovka_x + (50/2 - E_text.get_size()[0] / 2), 352))

    if pozadi == venek and stojim_u_shopu:
        info_shop_obrazovka_x = info_shop - kamera_x
        
        pygame.draw.rect(okno, cerna, (info_shop_obrazovka_x -1, 359, 52, 52))
        pygame.draw.rect(okno, (bila), (info_shop_obrazovka_x, 360, 50, 50))
        okno.blit(E_text, (info_shop_obrazovka_x + (50/2 - E_text.get_size()[0] / 2), 372))
    
    stojim_u_leva_lod = hrac_pozice_x > 329 and hrac_pozice_x < 350

    if pozadi == jezero and stojim_u_leva_lod:
        pygame.draw.rect(okno, cerna, (21, 339, 52, 52)) 
        pygame.draw.rect(okno, (bila), (22, 340, 50, 50))
        okno.blit(E_text, (info_jezero_obrazovka_x + (50/2 - E_text.get_size()[0] / 2) - 700, 352))
    
    stojim_u_prava_lod = hrac_pozice_x > 395 and hrac_pozice_x < 423

    if pozadi == jezero and stojim_u_prava_lod:
        okno.blit(ikona_prut, (722, 290))
        pygame.draw.rect(okno, cerna, za_space_u_jezera)
        pygame.draw.rect(okno, bila, (722, 340, 50, 50))
        okno.blit(E_text, (info_jezero_obrazovka_x + (50/2 - E_text.get_size()[0] / 2), 352))


    if pozadi != shop and pozadi != rybareni and pozadi != rybareni_dole and pozadi != rybareni_pozor:
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
        okno.blit(hodnota_kapra_text, (sell_kapr_pozice_x + polozky_velikost_x / 2 + 42, sell_kapr_pozice_y + 45))
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
        okno.blit(hodnota_tajnaRyba_text, (sell_tajnaRyba_pozice_x + polozky_velikost_x / 2 + 30, sell_tajnaRyba_pozice_y + 45))
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
    
    if not inventar and pozadi != shop and pozadi != pozadi_shop and not prut and not minihra:
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
        
        if baits_mode == "bait_bread":
            okno.blit(bread_inventory_ikona, (510, 440))
            pocet = baits["bread"]["pocet"]
            text = info_o_baits_font.render(f"x{pocet}", True, cerna)
            okno.blit(text, (510, 425))
            pygame.draw.rect(okno, cerna, za_bait_leave_tlacitko_inventory)
            pygame.draw.rect(okno, cervena, (bait_leave_tlacitko_inventory))
                
        if baits_mode == "bait_worm":
            okno.blit(worm_inventory_ikona, (510, 440))
            pocet = baits["worm"]["pocet"]
            text = info_o_baits_font.render(f"x{pocet}", True, cerna)
            okno.blit(text, (510, 425))
            pygame.draw.rect(okno, cerna, za_bait_leave_tlacitko_inventory)
            pygame.draw.rect(okno, cervena, bait_leave_tlacitko_inventory)
            
        if baits_mode == "bait_corn":
            okno.blit(corn_inventory_ikona, (510, 440))
            pocet = baits["corn"]["pocet"]
            text = info_o_baits_font.render(f"x{pocet}", True, cerna)
            okno.blit(text, (510, 425))
            pygame.draw.rect(okno, cerna, za_bait_leave_tlacitko_inventory)
            pygame.draw.rect(okno, cervena, bait_leave_tlacitko_inventory)
        
        if baits_mode == "bait_fish_head":
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
        pygame.draw.rect(okno, cerna, (349, 529, 102, 52))
        zpet_tlacitko_rect = pygame.draw.rect(okno, bila, (350, 530, 100, 50))
        okno.blit(zpet_tlacitko_text, (367, 543))
    
    
    if minihra:
        center = (okraj_random_x, okraj_random_y)
        radius = 22

        pygame.draw.circle(okno, cerna, center, radius + 3)
        pygame.draw.circle(okno, bila, center, radius)

        text_rect = pismeno_text.get_rect(center=center)
        okno.blit(pismeno_text, text_rect)
    
    if plny_inventar_upozorneni and pozadi == rybareni and not inventar:
        plny_inventar_upozorneni_rect = plny_inv_text.get_rect(center=(okno_sirka // 2, 280))
        okno.blit(plny_inv_text, plny_inventar_upozorneni_rect)
        if pygame.time.get_ticks() - plny_inventar_cas > plny_inventar_doba:
            plny_inventar_upozorneni = False
    
    
    if pozadi == rybareni and not prut and not minihra and not inventar:
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
    
    print(baits_mode)
    clock.tick(60)
    pygame.display.update()
    
