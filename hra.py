import pygame
import sys
pygame.init()

rozliseni_okna = (800, 600)
pozice_x = 350
pozice_y = 250
velikostX = 100
velikostY = 100
manualni_posun = 2

okno = pygame.display.set_mode(rozliseni_okna)
clock = pygame.time.Clock()

while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    okno.fill((87, 87, 87))
    pygame.draw.rect(okno, (0, 0, 0), (pozice_x, pozice_y, velikostX, velikostY))
    
    stisknuto = pygame.key.get_pressed()
    
    if stisknuto[pygame.K_w]:
        pozice_y -= manualni_posun
    if stisknuto[pygame.K_d]:
        pozice_x += manualni_posun
    if stisknuto[pygame.K_s]:
        pozice_y += manualni_posun
    if stisknuto[pygame.K_a]:
        pozice_x -= manualni_posun
    
    if pozice_x < 0:
        pozice_x = 0
    if pozice_x > 800 - velikostX:
        pozice_x = 800 - velikostX
    if pozice_y < 0:
        pozice_y = 0
    if pozice_y > 600 - velikostY:
        pozice_y = 600 - velikostY
    
    clock.tick(60)
    pygame.display.update()
    
    