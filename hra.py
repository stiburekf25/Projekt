import pygame
import sys
pygame.init()

# PRIPRAVA HRY

okno_sirka = 800
okno_vyska = 600

rozliseni_okna = (okno_sirka, okno_vyska)

hrac_pozice_x = 100
hrac_pozice_y = 320
hrac_velikostX= 100
hrac_velikostY = 150
hrac_rychlost = 4

kamera_x = 0

info_jezero = 1570


leva_zona = 300
prava_zona = 400

okno = pygame.display.set_mode(rozliseni_okna)
clock = pygame.time.Clock()

venek = pygame.image.load("level_1.png")
jezero = pygame.image.load("level_2.png")

pozadi = venek
pozadi_sirka = pozadi.get_width()
pozadi_vyska = pozadi.get_height()

postava = pygame.image.load("pepa.png")
TEXTURApostava = pygame.transform.scale(postava, (hrac_velikostX, hrac_velikostY))

E_font = pygame.font.SysFont("Aharoni", 40)
E_text = E_font.render("E", True, (0, 0, 0))

# CYKLICKE VYKRESLOVANI FRAMU HRY

while True:

    # OVLADANI HRY HRACEM
    
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    stisknuto = pygame.key.get_pressed()
    
    # UPRAVA HRY MEZI FRAMY

    if stisknuto[pygame.K_d]:
        hrac_pozice_x += hrac_rychlost

    if stisknuto[pygame.K_a]:
        hrac_pozice_x -= hrac_rychlost
        
    if hrac_pozice_x < 0:
        hrac_pozice_x = 0
    if hrac_pozice_x > pozadi_sirka - hrac_velikostX:
        hrac_pozice_x = pozadi_sirka - hrac_velikostX
        
    hrac_obrazovka_x = hrac_pozice_x - kamera_x
    
    if hrac_obrazovka_x > prava_zona:
        kamera_x += hrac_rychlost
    if hrac_obrazovka_x < leva_zona:
        kamera_x -= hrac_rychlost
        
    if kamera_x < 0:
        kamera_x = 0
    if kamera_x > pozadi_sirka - okno_sirka:
        kamera_x = pozadi_sirka - okno_sirka


    if pozadi == venek:

        info_jezero_obrazovka_x = info_jezero - kamera_x
        
        stojim_u_jezera = hrac_pozice_x > 1350 and hrac_pozice_x < 1450
            
        if stojim_u_jezera and stisknuto[pygame.K_e]:
            pozadi = jezero
            
            pozadi_sirka = pozadi.get_width()
            pozadi_vyska = pozadi.get_height()
            hrac_pozice_x = 50
            hrac_pozice_y = 320
            hrac_velikostX= 100
            hrac_velikostY = 150
            hrac_rychlost = 4
    
    # VYKRESLENI PRVKU HRY
    
    okno.blit(pozadi, (-kamera_x, 0))
    okno.blit(TEXTURApostava, (hrac_obrazovka_x, hrac_pozice_y))

    
    if pozadi == venek and stojim_u_jezera:
        pygame.draw.rect(okno, (255, 255, 255), (info_jezero_obrazovka_x, 340, 50, 50))
        okno.blit(E_text, (info_jezero_obrazovka_x + (50/2 - E_text.get_size()[0] / 2), 352))

    print(kamera_x, hrac_pozice_x)
    
    clock.tick(60)
    pygame.display.update()
    
    