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

leva_zona = 300
prava_zona = 400

pocitadlo = 0




okno = pygame.display.set_mode(rozliseni_okna)
clock = pygame.time.Clock()

venek = pygame.image.load("venek.png")
jezero = pygame.image.load("level_2.png")

pozadi = venek
pozadi_sirka = pozadi.get_width()
pozadi_vyska = pozadi.get_height()

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







E_font = pygame.font.SysFont("Aharoni", 40)
E_text = E_font.render("E", True, (0, 0, 0))

# CYKLICKE VYKRESLOVANI FRAMU HRY

while True:

    # OVLADANI HRY HRACEM
    
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    hrac_obrazovka_x = hrac_pozice_x - kamera_x
    
    stisknuto = pygame.key.get_pressed()
    
    # UPRAVA HRY MEZI FRAMY
    
    pocitadlo += 1
    aktualni_sprite = TEXTURApostava
    pocet_snimku = 2
    faktor_zpozdeni = 8
    
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


        info_jezero_obrazovka_x = info_jezero - kamera_x
        
        stojim_u_jezera = hrac_pozice_x > 1320 and hrac_pozice_x < 1450
            
        if stojim_u_jezera and stisknuto[pygame.K_e]:
            pozadi = jezero
            
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
            hrac_pozice_x = 50
            hrac_pozice_y = 320
            hrac_velikostX= 110
            hrac_velikostY = 170
            hrac_rychlost = 4
    
    #JEZERO
    if pozadi == jezero:
        if hrac_pozice_x < 0:
            hrac_pozice_x = 0
        if hrac_pozice_x > pozadi_sirka - hrac_velikostX:
            hrac_pozice_x = pozadi_sirka - hrac_velikostX
    
            
        if hrac_obrazovka_x > prava_zona:
            kamera_x += hrac_rychlost
        if hrac_obrazovka_x < leva_zona:
            kamera_x -= hrac_rychlost
                
        if kamera_x < 0:
            kamera_x = 0
        if kamera_x > pozadi_sirka - okno_sirka:
            kamera_x = pozadi_sirka - okno_sirka 
    
    # VYKRESLENI PRVKU HRY
    
    okno.blit(pozadi, (-kamera_x, 0))
    okno.blit(aktualni_sprite, (hrac_obrazovka_x, hrac_pozice_y))

    
    if pozadi == venek and stojim_u_jezera:
        pygame.draw.rect(okno, (255, 255, 255), (info_jezero_obrazovka_x, 340, 50, 50))
        okno.blit(E_text, (info_jezero_obrazovka_x + (50/2 - E_text.get_size()[0] / 2), 352))

    print(kamera_x, hrac_pozice_x)
    
    clock.tick(60)
    pygame.display.update()
    
