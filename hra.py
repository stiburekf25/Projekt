import pygame
import sys
pygame.init()

# PRIPRAVA HRY

okno_sirka = 800
okno_vyska = 600

hrac_pozice_x = 400
hrac_pozice_y = 315
hrac_rychlost = 4
hrac_velikostX= 110
hrac_velikostY = 170

rozliseni_okna = (okno_sirka, okno_vyska)

kamera_x = 0

info_jezero = 1570
info_shop = 920

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


#inventar
inventar = False
buy = pygame.draw.rect(okno, (seda), (120, 335, 200, 100))
sell = pygame.draw.rect(okno, (seda), (480, 335, 200, 100))
leave = pygame.draw.rect(okno, (seda), (670, 520, 100, 50))
shop_mode = None # nic / buy / sell

#predmety
coins = 0
plechovka = 0
bota = 0
kapr = 0






# obrazky levelu
venek = pygame.image.load("venek.png")
jezero = pygame.image.load("level_2.png")
shop = pygame.image.load("shop.png")

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

#obrazek inv
inv = pygame.image.load("inventar.png")
TEXTURAinv = pygame.transform.scale(inv, (500, 300))


#priprava textu
E_font = pygame.font.SysFont("Aharoni", 40)
E_text = E_font.render("E", True, (cerna))

coins_font = pygame.font.SysFont("Aharoni", 30)
coins_text = coins_font.render(("golds:"f"{coins}"), True, (seda))

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
    
    #inventar zapinani a vypinani
    if stisknuto[pygame.K_SPACE]:
        inventar = True
        hrac_rychlost = 0
    
    if stisknuto[pygame.K_ESCAPE]:
        inventar = False 
        hrac_rychlost = 4

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


        info_jezero_obrazovka_x = info_jezero - kamera_x
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
        
        stojim_u_shopu = hrac_pozice_x > 750 and hrac_pozice_x < 1020
        
        
        if stojim_u_shopu and stisknuto[pygame.K_e]:
            pozadi = shop
            hrac_rychlost = 0
            
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
        

            
        
    #JEZERO
    if pozadi == jezero:
        aktualni_sprite = TEXTURApepa_lod
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

            kamera_x = 0

    # VYKRESLENI PRVKU HRY
    
    if pozadi != shop:
        okno.blit(pozadi, (-kamera_x, 0))
    else:
        okno.blit(pozadi, (0, 0))
    
    
    okno.blit(coins_text, (20, 30))


    
    if pozadi == venek and stojim_u_jezera:
        pygame.draw.rect(okno, (bila), (info_jezero_obrazovka_x, 340, 50, 50))
        okno.blit(E_text, (info_jezero_obrazovka_x + (50/2 - E_text.get_size()[0] / 2), 352))
    if pozadi == venek and stojim_u_shopu:
        pygame.draw.rect(okno, (bila), (info_shop_obrazovka_x, 360, 50, 50))
        okno.blit(E_text, (info_shop_obrazovka_x + (50/2 - E_text.get_size()[0] / 2), 372))
    if pozadi == jezero and stojim_u_leva_lod:
        pygame.draw.rect(okno, (bila), (22, 340, 50, 50))
        okno.blit(E_text, (info_jezero_obrazovka_x + (50/2 - E_text.get_size()[0] / 2) - 700, 352))


    if pozadi != shop:
        okno.blit(aktualni_sprite, (hrac_obrazovka_x, hrac_pozice_y))
    
        if inventar:
            okno.blit(TEXTURAinv, ( 350 - (500 - hrac_velikostX) / 2, 10,))
    
    if pozadi == shop:
        pygame.draw.rect(okno, seda, buy)
        pygame.draw.rect(okno, seda, sell)
        pygame.draw.rect(okno, seda, leave)

    
    if pozadi == shop and (buy.collidepoint(mys_pozice) or sell.collidepoint(mys_pozice) or leave.collidepoint(mys_pozice)):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    if pozadi == shop and shop_mode is None: 
        if buy.collidepoint(mys_pozice) and klik[0]:
            shop_mode = "buy"
        
        if sell.collidepoint(mys_pozice) and klik[0]:
            shop_mode = "sell"
        
        if leave.collidepoint(mys_pozice) and klik[0]:
            pozadi = venek
            shop_mode = None
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()

            hrac_pozice_x = 888
            hrac_pozice_y = 315

            hrac_velikostX = 110
            hrac_velikostY = 170
            hrac_rychlost = 4

            kamera_x = 0


    if pozadi == shop and shop_mode is None:
        pygame.draw.rect(okno, seda, buy)
        pygame.draw.rect(okno, seda, sell)
        pygame.draw.rect(okno, seda, leave)


    if pozadi == shop and shop_mode == "buy":
        # tady později itemy
        pass

    if pozadi == shop and shop_mode == "sell":
        # tady ryby
        pass
    
    if pozadi == shop and stisknuto[pygame.K_ESCAPE]:
        shop_mode = None
    

    print(shop_mode)
    #print(kamera_x, hrac_pozice_x)
    
    clock.tick(60)
    pygame.display.update()
    
