import pygame
import solve_pddl
from pathlib import Path

data_folder = Path("/home/familie/symk/domains/")
ziel_pddl_pfad = ["ziel_pfad"] * 5
ziel_pddl_pfad[0] = data_folder /"Ziel0.pddl"
ziel_pddl_pfad[1] = data_folder /"Ziel1.pddl"
ziel_pddl_pfad[2] = data_folder /"Ziel2.pddl"
ziel_pddl_pfad[3] = data_folder /"Ziel3.pddl"
ziel_pddl_pfad[4] = data_folder /"Ziel4.pddl"


pygame.init()

black = (0,0,0)
white = (255,255,255)
red   = (255,0,0)
green = (0,255,0)
blue  = (0,0,255)
orange = ((255,100,10))
purple = ((240,0,255))


def pygame_quit():
  for ereignis in pygame.event.get():
    if ereignis.type == pygame.QUIT or \
       (ereignis.type == pygame.KEYDOWN and ereignis.key == pygame.K_ESCAPE):
      return True

def draw_lab_wait():
    # PDDL-Textdatei auslesen
    file = open(ziel_pddl_pfad[1], 'r')

    # Spielfeld zeichnen
    # Fenstergröße (Pixel)
    screen = pygame.display.set_mode((800, 500))
    # Rechteck Abmessungen
    width = height = 70
    # X-Y Koordinate
    x = 0
    y = 0
    n = 0

    screen.fill(white)

    for textzeile in file:
        if(n == 7):
          x = x + width
          y = 0
          n = 0
        if (textzeile.find('open') != -1):
         pygame.draw.rect(screen, black, (x,y,width,height), 1)
         y = y + height
         n = n + 1
        elif (textzeile.find('locked') != -1):
         pygame.draw.rect(screen, black, (x,y,width,height), 0)
         y = y + height
         n = n + 1
    file.close()

    #Initialzustand auslesen und einzeichnen
    x = y = 0
    file = open(ziel_pddl_pfad[1], 'r')
    for textzeile in file:
        if((textzeile.find('at-robot') != -1) & (textzeile.find('goal') == -1)):
            x = int(textzeile[24]) * width
            y = int(textzeile[26]) * height
            pygame.draw.ellipse(screen, red, (x,y,width,height), 0)
    file.close()

    #Zielzustand 1 auslesen und einzeichnen
    x = y = 0
    file = open(ziel_pddl_pfad[1], 'r')
    for textzeile in file:
        if(textzeile.find('goal') != -1):
            x = int(textzeile[29]) * width
            y = int(textzeile[31]) * height
            pygame.draw.ellipse(screen, green, (x,y,width,height), 5)
    file.close()

    #Zielzustand 2 auslesen und einzeichnen
    x = y = 0
    file = open(ziel_pddl_pfad[2], 'r')
    for textzeile in file:
        if(textzeile.find('goal') != -1):
            x = int(textzeile[29]) * width
            y = int(textzeile[31]) * height
            pygame.draw.ellipse(screen, purple, (x,y,width,height), 5)
    file.close()

    #Zielzustand 3 auslesen und einzeichnen
    x = y = 0
    file = open(ziel_pddl_pfad[3], 'r')
    for textzeile in file:
        if(textzeile.find('goal') != -1):
            x = int(textzeile[29]) * width + int(width/2)
            y = int(textzeile[31]) * height + int(height/2)
            pygame.draw.circle(screen, blue, (x,y), 20, 0)
    file.close()

    #Zielzustand 4 auslesen und einzeichnen
    x = y = 0
    file = open(ziel_pddl_pfad[4], 'r')
    for textzeile in file:
        if(textzeile.find('goal') != -1):
            x = int(textzeile[29]) * width + int(width/2)
            y = int(textzeile[31]) * height + int(height/2)
            pygame.draw.circle(screen, orange, (x,y), 20, 0)
    file.close()

    #Spiegelt die Ausgabe so dass das Koordinatensystem unten links mit 0,0 beginnt
    display_surface = pygame.display.get_surface()
    display_surface.blit(pygame.transform.flip(display_surface, False, True), dest=(0, 0))

    #Text in Grafik schreiben
    pygame.font.init()
    myfont = pygame.font.SysFont(None, 25)
    textsurface = myfont.render('Spielstein', False, red)
    screen.blit(textsurface,(500,35))
    textsurface = myfont.render('Agent1 Ziele:', False, black)
    screen.blit(textsurface,(500,70))
    textsurface = myfont.render('Ziel1', False, green)
    screen.blit(textsurface, (625, 70))
    textsurface = myfont.render('Ziel2', False, purple)
    screen.blit(textsurface, (700, 70))
    textsurface = myfont.render('Agent2 Ziele:', False, black)
    screen.blit(textsurface,(500,105))
    textsurface = myfont.render('Ziel3', False, blue)
    screen.blit(textsurface, (625, 105))
    textsurface = myfont.render('Ziel4', False, orange)
    screen.blit(textsurface, (700, 105))
    textsurface = myfont.render('Wahrscheinlichkeit Ziele Agent1', False, black)
    screen.blit(textsurface,(500,200))
    textsurface = myfont.render('Ziel1:', False, black)
    screen.blit(textsurface,(500,250))
    textsurface = myfont.render('Ziel2:', False, black)
    screen.blit(textsurface,(650,250))
    textsurface = myfont.render('Wahrscheinlichkeit Ziele Agent2', False, black)
    screen.blit(textsurface,(500,350))
    textsurface = myfont.render('Ziel3:', False, black)
    screen.blit(textsurface,(500,400))
    textsurface = myfont.render('Ziel4:', False, black)
    screen.blit(textsurface,(650,400))


    #Wahrscheinlichkeiten aktualisieren
    P_Ziel1 = str(solve_pddl.p_Z1_old)
    P_Ziel2 = str(solve_pddl.p_Z2_old)
    P_Ziel3 = str(solve_pddl.p_Z3_old)
    P_Ziel4 = str(solve_pddl.p_Z4_old)
    #Agent1
    textsurface = myfont.render(P_Ziel1[:4], False, black)
    screen.blit(textsurface,(550,250))
    textsurface = myfont.render(P_Ziel2[:4], False, black)
    screen.blit(textsurface,(700,250))
    #Agent2
    textsurface = myfont.render(P_Ziel3[:4], False, black)
    screen.blit(textsurface,(550,400))
    textsurface = myfont.render(P_Ziel4[:4], False, black)
    screen.blit(textsurface,(700,400))
    pygame.display.update()
    while not pygame_quit():
        wait = 0

def draw_lab():
    # PDDL-Textdatei auslesen
    file = open(ziel_pddl_pfad[1], 'r')

    # Spielfeld zeichnen
    # Fenstergröße (Pixel)
    screen = pygame.display.set_mode((800, 500))
    # Rechteck Abmessungen
    width = height = 70
    # X-Y Koordinate
    x = 0
    y = 0
    n = 0

    screen.fill(white)

    for textzeile in file:
        if(n == 7):
          x = x + width
          y = 0
          n = 0
        if (textzeile.find('open') != -1):
         pygame.draw.rect(screen, black, (x,y,width,height), 1)
         y = y + height
         n = n + 1
        elif (textzeile.find('locked') != -1):
         pygame.draw.rect(screen, black, (x,y,width,height), 0)
         y = y + height
         n = n + 1
    file.close()

    #Initialzustand auslesen und einzeichnen
    x = y = 0
    file = open(ziel_pddl_pfad[1], 'r')
    for textzeile in file:
        if((textzeile.find('at-robot') != -1) & (textzeile.find('goal') == -1)):
            x = int(textzeile[24]) * width
            y = int(textzeile[26]) * height
            pygame.draw.ellipse(screen, red, (x,y,width,height), 0)
    file.close()

    #Zielzustand 1 auslesen und einzeichnen
    x = y = 0
    file = open(ziel_pddl_pfad[1], 'r')
    for textzeile in file:
        if(textzeile.find('goal') != -1):
            x = int(textzeile[29]) * width
            y = int(textzeile[31]) * height
            pygame.draw.ellipse(screen, green, (x,y,width,height), 5)
    file.close()

    #Zielzustand 2 auslesen und einzeichnen
    x = y = 0
    file = open(ziel_pddl_pfad[2], 'r')
    for textzeile in file:
        if(textzeile.find('goal') != -1):
            x = int(textzeile[29]) * width
            y = int(textzeile[31]) * height
            pygame.draw.ellipse(screen, purple, (x,y,width,height), 5)
    file.close()

    #Zielzustand 3 auslesen und einzeichnen
    x = y = 0
    file = open(ziel_pddl_pfad[3], 'r')
    for textzeile in file:
        if(textzeile.find('goal') != -1):
            x = int(textzeile[29]) * width + int(width/2)
            y = int(textzeile[31]) * height + int(height/2)
            pygame.draw.circle(screen, blue, (x,y), 20, 0)
    file.close()

    #Zielzustand 4 auslesen und einzeichnen
    x = y = 0
    file = open(ziel_pddl_pfad[4], 'r')
    for textzeile in file:
        if(textzeile.find('goal') != -1):
            x = int(textzeile[29]) * width + int(width/2)
            y = int(textzeile[31]) * height + int(height/2)
            pygame.draw.circle(screen, orange, (x,y), 20, 0)
    file.close()

    #Spiegelt die Ausgabe so dass das Koordinatensystem unten links mit 0,0 beginnt
    display_surface = pygame.display.get_surface()
    display_surface.blit(pygame.transform.flip(display_surface, False, True), dest=(0, 0))

    #Text in Grafik schreiben
    pygame.font.init()
    myfont = pygame.font.SysFont(None, 25)
    textsurface = myfont.render('Spielstein', False, red)
    screen.blit(textsurface,(500,35))
    textsurface = myfont.render('Agent1 Ziele:', False, black)
    screen.blit(textsurface,(500,70))
    textsurface = myfont.render('Ziel1', False, green)
    screen.blit(textsurface, (625, 70))
    textsurface = myfont.render('Ziel2', False, purple)
    screen.blit(textsurface, (700, 70))
    textsurface = myfont.render('Agent2 Ziele:', False, black)
    screen.blit(textsurface,(500,105))
    textsurface = myfont.render('Ziel3', False, blue)
    screen.blit(textsurface, (625, 105))
    textsurface = myfont.render('Ziel4', False, orange)
    screen.blit(textsurface, (700, 105))
    textsurface = myfont.render('Wahrscheinlichkeit Ziele Agent1', False, black)
    screen.blit(textsurface,(500,200))
    textsurface = myfont.render('Ziel1:', False, black)
    screen.blit(textsurface,(500,250))
    textsurface = myfont.render('Ziel2:', False, black)
    screen.blit(textsurface,(650,250))
    textsurface = myfont.render('Wahrscheinlichkeit Ziele Agent2', False, black)
    screen.blit(textsurface,(500,350))
    textsurface = myfont.render('Ziel3:', False, black)
    screen.blit(textsurface,(500,400))
    textsurface = myfont.render('Ziel4:', False, black)
    screen.blit(textsurface,(650,400))


    #Wahrscheinlichkeiten aktualisieren
    P_Ziel1 = str(solve_pddl.p_Z1_old)
    P_Ziel2 = str(solve_pddl.p_Z2_old)
    P_Ziel3 = str(solve_pddl.p_Z3_old)
    P_Ziel4 = str(solve_pddl.p_Z4_old)
    #Agent1
    textsurface = myfont.render(P_Ziel1[:4], False, black)
    screen.blit(textsurface,(550,250))
    textsurface = myfont.render(P_Ziel2[:4], False, black)
    screen.blit(textsurface,(700,250))
    #Agent2
    textsurface = myfont.render(P_Ziel3[:4], False, black)
    screen.blit(textsurface,(550,400))
    textsurface = myfont.render(P_Ziel4[:4], False, black)
    screen.blit(textsurface,(700,400))
    pygame.display.update()



pygame.quit()