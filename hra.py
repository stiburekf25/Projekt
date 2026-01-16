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

#BARVICKY
zluta = (205, 235, 98)
cerna = (0, 0, 0)
bila = (255, 255, 255)
seda = (94, 94, 94)
hneda = (148, 96, 56)
Sseda = (158, 158, 158)


#inventar
inventar = False
obsah_inventare = 0
obsah_inventare_max = 7
plny_inventar_upozorneni = False
plny_inventar_cas = 0
plny_inventar_doba = 2000

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
    },
    {
        "jmeno": "Bota",
        "sance": 65,
        "cekani": 5000,
        "zmacknuti": 7,
        "limit_cekani": 2500,
        "cena": 30,
    },
    {
        "jmeno": "Kapr",
        "sance": 80,
        "cekani": 6000,
        "zmacknuti": 12,
        "limit_cekani": 2000,
        "cena": 80,
    },
    {
        "jmeno": "Štika",
        "sance": 90,
        "cekani": 7000,
        "zmacknuti": 15,
        "limit_cekani": 1300,
        "cena": 130,
    },
    {
        "jmeno": "Sumec",
        "sance": 97,
        "cekani": 11000,
        "zmacknuti": 18,
        "limit_cekani": 1000,
        "cena": 180,
    },
    {
        "jmeno": "Rak",
        "sance": 100,
        "cekani": 9000,
        "zmacknuti": 25,
        "limit_cekani": 800,
        "cena": 500,
    },
]
        


#velikosti
buy_velikost = 60
sell_velikost = 60
leave_velikost =  40
leave_buy_velikost = 40
leave_sell_velikost = 40
shop_hlaska = None
hlaska_velikost = 25
zpet_tlacitko_velikost = 40
space_to_fish_velikost = 40
pismeno_velikost = 40
plny_inventory_velikost = 60
cislo_u_polozky_velikost = 20


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
TEXTURAinv = pygame.transform.scale(inv, (500, 300))
ikona_inv = pygame.image.load("ikona_inv.png") # x 70 y 80
ikona_inv_rect = ikona_inv.get_rect(topleft=(700, 20))
tlacitko = pygame.draw.rect(okno, Sseda, (392, 240, 30, 30))
za_tlacitko = pygame.draw.rect(okno, seda, (391, 239, 32, 32))



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
space_to_fish_font = pygame.font.SysFont("Aharoni", space_to_fish_velikost)
space_to_fish_text = space_to_fish_font.render("Press space to cast", True, cerna)
pismeno_font = pygame.font.SysFont("Aharoni", pismeno_velikost)
plny_inv_font = pygame.font.SysFont("Aharoni", plny_inventory_velikost)
plny_inv_text = plny_inv_font.render("FULL INVENTORY", True, cerna)
cislo_u_plechovky_font = pygame.font.SysFont("Aharoni", cislo_u_polozky_velikost)


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
        
        if stojim_u_jezera and stisknuto[pygame.K_e]:
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
        
        if stojim_u_shopu and stisknuto[pygame.K_e]:
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
        
        if stojim_u_leva_lod and stisknuto[pygame.K_e]:
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
        
        if stojim_u_prava_lod and stisknuto[pygame.K_e] and pozadi != rybareni:
            pozadi = rybareni
            zpet_tlacitko = True
            hrac_rychlost = 0
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
    
    #Tlacitko exit k opusteni rybareni zpet na jezero
    
    if zpet_tlacitko and pozadi == rybareni and zpet_tlacitko_rect.collidepoint(mys_pozice) and mouse_click:
        pozadi = jezero
        zpet_tlacitko = False
        hrac_rychlost = 4
        hrac_pozice_x = 422
        kamera_x = 0
        aktualni_sprite = TEXTURApepa_lod

    #SPACE k zapnuti naprahu
   
    if pozadi == rybareni and stisknuto[pygame.K_SPACE] and not (prut or minihra):
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
            print(obsah_inventare)
    
        elif stisknuto[ord(sekvence[poradi])]:
            poradi += 1
            if poradi < ulovek["zmacknuti"]:
                pismeno_text = pismeno_font.render(f"{sekvence[poradi]}", True, cerna)
                okraj_random_x = random.randint(20, 780 - pismeno_velikost)
                okraj_random_y = random.randint(20, 580 - pismeno_velikost)
                
                zacatek_limitu = pygame.time.get_ticks()
            else:
                obsah_inventare[ulovek["jmeno"]] += 1
                minihra = False
                zpet_tlacitko = True
                pozadi = rybareni
                hrac_rychlost = 0
                pozadi_sirka = pozadi.get_width()
                pozadi_vyska = pozadi.get_height()
                print(obsah_inventare)
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
                
                
    if shop_mode == "sell" and pozadi == pozadi_shop:
        if plechovka_sell.collidepoint(mys_pozice) and mouse_click:
                jmeno = "Plechovka"
                
                if obsah_inventare["Plechovka"] <= 0:
                    print("nemas plechovku lol", obsah_inventare)
                    
                else:
                    predmet = najdi_predmet_podle_jmena(predmety, jmeno)
                    
                    obsah_inventare[jmeno] -= 1
                    coins += predmet["cena"]
        
        if bota_sell.collidepoint(mys_pozice) and mouse_click:
            jmeno = "Bota"
            
            if obsah_inventare["Bota"] <= 0:
                print("nemas botu lol", obsah_inventare)
                
            else:
                predmet = najdi_predmet_podle_jmena(predmety, jmeno)
                
                obsah_inventare[jmeno] -= 1
                coins += predmet["cena"]
        
        if kapr_sell.collidepoint(mys_pozice) and mouse_click:
            jmeno = "Kapr"
            
            if obsah_inventare["Kapr"] <= 0:
                print("nemas kapra lol", obsah_inventare)
            
            else:
                predmet = najdi_predmet_podle_jmena(predmety, jmeno)
                
                obsah_inventare[jmeno] -= 1
                coins += predmet["cena"]
        
        if stika_sell.collidepoint(mys_pozice) and mouse_click:
            jmeno = "Stika"
            
            if obsah_inventare["Štika"] <= 0:
                print("nemas stiku lol", obsah_inventare)
                
            else:
                predmet = najdi_predmet_podle_jmena(predmety, jmeno)
                
                obsah_inventare[jmeno] -= 1
                coins += predmet["cena"]
        
        if sumec_sell.collidepoint(mys_pozice) and mouse_click:
            jmeno = "Sumec"
            
            if obsah_inventare["Sumec"] <= 0:
                print("nemas sumce lol", obsah_inventare)
                
            else:
                predmet = najdi_predmet_podle_jmena(predmety, jmeno)
                
                obsah_inventare[jmeno] -= 1
                coins += predmet["cena"]

        if tajnaRyba_sell.collidepoint(mys_pozice) and mouse_click:
            jmeno = "Rak"
            
            if obsah_inventare["Rak"] <= 0:
                print("nemas tajnou rybu lol", obsah_inventare)
                
            else:
                predmet = najdi_predmet_podle_jmena(predmety, jmeno)
                
                obsah_inventare[jmeno] -= 1
                coins += predmet["cena"]

            
        #Prechod z buy nebo sell na none (uvitaci stranka shopu)
        
        elif shop_mode == "buy":
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
    
    #Kurzor na hand nebo arrow podle urciteho pozadi ci podminky
    
    kurzor_hand = False 
        
    if pozadi == pozadi_shop and leave_buy.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif pozadi == shop and (buy.collidepoint(mys_pozice) or sell.collidepoint(mys_pozice) or leave.collidepoint(mys_pozice)):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif pozadi == pozadi_shop and leave_sell.collidepoint(mys_pozice):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif ikona_inv_rect.collidepoint(mys_pozice)and not inventar and not pozadi == shop and not pozadi == pozadi_shop:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif tlacitko.collidepoint(mys_pozice) and inventar:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif zpet_tlacitko_rect.collidepoint(mys_pozice) and not prut and not minihra and not pozadi == jezero and not pozadi == shop and not pozadi == venek and not shop_mode == "buy" and not shop_mode == "sell":
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
        
        pygame.draw.rect(okno, cerna, za_plechovka_sell)
        pygame.draw.rect(okno, hneda, plechovka_sell)
        pocet_plechovek = obsah_inventare["Plechovka"]
        cislo_u_plechovky_text = cislo_u_plechovky_font.render(str(pocet_plechovek), True, cerna)
        
        okno.blit(cislo_u_plechovky_text, (sell_plechovka_pozice_x + polozky_velikost_x - 25, sell_plechovka_pozice_y + polozky_velikost_y -25))

        
        pygame.draw.rect(okno, cerna, za_bota_sell)
        pygame.draw.rect(okno, hneda, bota_sell)
        
        pygame.draw.rect(okno, cerna, za_kapr_sell)
        pygame.draw.rect(okno, hneda, kapr_sell)
        
        pygame.draw.rect(okno, cerna, za_stika_sell)
        pygame.draw.rect(okno, hneda, stika_sell)
        
        pygame.draw.rect(okno, cerna, za_sumec_sell)
        pygame.draw.rect(okno, hneda, sumec_sell)
        
        pygame.draw.rect(okno, cerna, za_tajnaRyba_sell)
        pygame.draw.rect(okno, hneda, tajnaRyba_sell)
        
        okno.blit(leave_sell_text, (57, 548))
    
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

    
    coins_text = coins_font.render(f"golds:{coins}", True, zluta)
    okno.blit(coins_text, (30, 20))
    
    if not inventar and pozadi != shop and pozadi != pozadi_shop:
        okno.blit(ikona_inv, (700, 20))
        
    if inventar:
        okno.blit(TEXTURAinv, ( 350 - (500 - hrac_velikostX) / 2, 10,))
        pygame.draw.rect(okno, seda, (391, 239, 32, 32)) # za tlacitko
        pygame.draw.rect(okno, Sseda, (392, 240, 30, 30)) # tlacitko
    
    if not inventar and pozadi == rybareni:
        hrac_rychlost = 0
    if inventar and pozadi == rybareni:
        hrac_rychlost = 0
    
    if zpet_tlacitko:
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
    
    if plny_inventar_upozorneni:
        plny_inventar_upozorneni_rect = plny_inv_text.get_rect(center=(okno_sirka // 2, 50))
        okno.blit(plny_inv_text, plny_inventar_upozorneni_rect)
        if pygame.time.get_ticks() - plny_inventar_cas > plny_inventar_doba:
            plny_inventar_upozorneni = False

    
    #print(shop_mode)
    #print(kamera_x, hrac_pozice_x)
    #print(inventar)
    #print(sekvence[poradi])
    #print(mouse_click)
        
    clock.tick(60)
    pygame.display.update()
    