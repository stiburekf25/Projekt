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

#predmety
coins = 100
obsah_inventare = {
    "plechovka":0, "bota":0, "kapr":0}

#Rybareni
prut = False
minihra = False
predmety = [
    {
        "jmeno": "plechovka",
        "sance": 50,
        "cekani": 1,
        "zmacknuti": 5
    },
    {
        "jmeno": "bota",
        "sance": 90,
        "cekani": 1.3,
        "zmacknuti": 7
    },
    {
        "jmeno": "kapr",
        "sance": 100,
        "cekani": 2,
        "zmacknuti": 12
    }
]
        


#shop
buy_velikost = 60
sell_velikost = 60
leave_velikost =  40
leave_buy_velikost = 40
leave_sell_velikost = 40
shop_hlaska = None
hlaska_velikost = 25

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
coins_text = coins_font.render(f"golds:{coins}", True, zluta)
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



hlaska_font = pygame.font.SysFont("Aharoni", hlaska_velikost)
shop_hlaska = random.choice(seznam_vet)
hlaska_text = hlaska_font.render(shop_hlaska, True, cerna)

# CYKLICKE VYKRESLOVANI FRAMU HRY

while True:

    # OVLADANI HRY HRACEM
    
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    hrac_obrazovka_x = hrac_pozice_x - kamera_x
    
    stisknuto = pygame.key.get_pressed()
    mys_pozice = pygame.mouse.get_pos()
    klik = pygame.mouse.get_pressed()

    
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
    
        aktualni_sprite = TEXTURApepa_lod
        
        if stisknuto[pygame.K_d]:
            aktualni_sprite = TEXTURApepa_2_lod

        elif stisknuto[pygame.K_a]:
            aktualni_sprite = TEXTURApepa_1_lod
            
        if hrac_pozice_x < 330:
            hrac_pozice_x = 330
        if hrac_pozice_x > 422:
            hrac_pozice_x = 422
    
            
        if hrac_obrazovka_x > prava_zona:
            kamera_x += hrac_rychlost
        if hrac_obrazovka_x < leva_zona:
            kamera_x -= hrac_rychlost
                
        if kamera_x < 0:
            kamera_x = 0
        if kamera_x > pozadi_sirka - okno_sirka:
            kamera_x = pozadi_sirka - okno_sirka 
        
        stojim_u_leva_lod = hrac_pozice_x > 329 and hrac_pozice_x < 350
        
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
        
        if stojim_u_prava_lod and stisknuto[pygame.K_e]:
            pozadi = rybareni
            hrac_rychlost = 0
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
        
    if pozadi == rybareni and stisknuto[pygame.K_SPACE] and not (prut or minihra):
        prut = True
        ulovek = vyber_predmet(predmety)
        cas_nahozeni = pygame.time.get_ticks()
        print(ulovek)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    if prut and pygame.time.get_ticks() - cas_nahozeni > ulovek["cekani"]:
        prut = False
        minihra = True
        sekvence = ""
        poradi = 0
        
        for pismeno in range(ulovek["zmacknuti"]):
            pismneko_ktere_zkousime_davat_do_sekvence = chr(random.randint(97, 97 + 25))
            while sekvence != "" and sekvence[-1] == pismneko_ktere_zkousime_davat_do_sekvence:
                pismneko_ktere_zkousime_davat_do_sekvence = chr(random.randint(97, 97 + 25))
            sekvence += pismneko_ktere_zkousime_davat_do_sekvence
        print(sekvence)

    if minihra:
        print(sekvence[poradi])
        if stisknuto[ord(sekvence[poradi])]:
            poradi += 1
        if poradi == ulovek["zmacknuti"]:
            obsah_inventare[ulovek["jmeno"]] += 1
            minihra = False
            print(obsah_inventare)
            
        

        
            
            
            
                
            

                
            

    if pozadi == shop:
        if shop_mode is None: 
            if buy.collidepoint(mys_pozice) and klik[0]:
                shop_mode = "buy"
        
            elif sell.collidepoint(mys_pozice) and klik[0]:
                shop_mode = "sell"
        
            elif leave.collidepoint(mys_pozice) and klik[0]:
                pozadi = venek
                hrac_pozice_x, hrac_pozice_y, kamera_x = pozice_pred_shopem
                hrac_velikostX = 110
                hrac_velikostY = 170
                hrac_rychlost = 4
                shop_mode = None
                shop_hlaska = None
                pozadi_sirka = pozadi.get_width()
                pozadi_vyska = pozadi.get_height()

        
        elif shop_mode == "buy":
            if leave_buy.collidepoint(mys_pozice) and klik[0]:
                shop_mode = None
                pozadi = shop
        
        elif shop_mode == "sell":
            if leave_sell.collidepoint(mys_pozice) and klik[0]:
                shop_mode = None
                pozadi = shop
                
    if pozadi != shop and pozadi != pozadi_shop:
        if ikona_inv_rect.collidepoint(mys_pozice) and klik[0]:
            inventar = True
            hrac_rychlost = 0
        if inventar:
            if tlacitko.collidepoint(mys_pozice) and klik[0]:
                inventar = False
                hrac_rychlost = 4
                
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

    if pozadi == jezero and stojim_u_leva_lod:
        pygame.draw.rect(okno, cerna, (21, 339, 52, 52)) 
        pygame.draw.rect(okno, (bila), (22, 340, 50, 50))
        okno.blit(E_text, (info_jezero_obrazovka_x + (50/2 - E_text.get_size()[0] / 2) - 700, 352))
    
    if pozadi == jezero and stojim_u_prava_lod:
        okno.blit(ikona_prut, (722, 290))
        pygame.draw.rect(okno, cerna, za_space_u_jezera)
        pygame.draw.rect(okno, bila, (722, 340, 50, 50))
        okno.blit(E_text, (info_jezero_obrazovka_x + (50/2 - E_text.get_size()[0] / 2), 352))


    if pozadi != shop and pozadi != rybareni:
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
        if leave_buy.collidepoint(mys_pozice) and klik[0]:
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
    
    if pozadi == pozadi_shop and shop_mode == "sell":
        if leave_sell.collidepoint(mys_pozice) and klik[0]:
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
        

    #print(shop_mode)
    #print(kamera_x, hrac_pozice_x)
    #print(inventar)
    
    clock.tick(60)
    pygame.display.update()
    