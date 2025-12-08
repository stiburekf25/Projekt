import pygame
import sys
pygame.init()

okno_sirka = 800
okno_vyska = 600

skacu = False


rozliseni_okna = (okno_sirka, okno_vyska)

hrac_pozice_x = 100
hrac_pozice_y = 320
hrac_velikostX= 100
hrac_velikostY = 150
hrac_rychlost = 4

kamera_x = 0

leva_zona = 500
prava_zona = 500

okno = pygame.display.set_mode(rozliseni_okna)
clock = pygame.time.Clock()

pozadi = pygame.image.load("level_1.png")
pozadi_sirka = pozadi.get_width()
pozadi_vyska = pozadi.get_height()

postava = pygame.image.load("pepa.png")
TEXTURApostava = pygame.transform.scale(postava, (hrac_velikostX, hrac_velikostY))

while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    
    
    
    
    stisknuto = pygame.key.get_pressed()
    

    if stisknuto[pygame.K_d]:
        hrac_pozice_x += hrac_rychlost

    if stisknuto[pygame.K_a]:
        hrac_pozice_x -= hrac_rychlost
        
    #if stisknuto[pygame.K_SPACE]:
        #skacu = True
        #if skacu:
            
            
    
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

    okno.blit(pozadi, (-kamera_x, 0))
    okno.blit(TEXTURApostava, (hrac_obrazovka_x, hrac_pozice_y))

    clock.tick(60)
    pygame.display.update()
    
    