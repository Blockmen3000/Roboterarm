#https://www.mypapertown.de
#Version 1.3
import json
import numpy as np
from tkinter import *
from tkinter import filedialog as fd
from PIL import Image as im
from PIL import ImageTk
from functools import partial
import HEMalgorithmus as HEM
import Malprogramm as draw

try:
    import roboter as ROBO
except:
    print("kein Roboter verfügbar")
import turtle
from turtle import TurtleScreen, ScrolledCanvas, RawTurtle

class Benutzeroberfläche:
    def __init__(self,info=False):
        self.farben = ("#000000","#CCCCCC","#232327","#232327", "#737377", "#232327", "#CCCCCC")
        self.farben = ("#888888","black","#BBBBBB","#737377", "#434347", "#999999", "black")
        # [0] = Background
        # [1] = Text
        # [2] = Canvas
        # [3] = Tabbuttonfarbe
        # [4] = aktuelle Tabfarbe
        # [5] = Standard-ActiveBackground (nicht bei Klaibrieren, Zeichnen oder Toleranz anpassen, weil dort schon rot und grün zum Einsatz kommen)
        # [6] = Standard-ActiveForeground (Textfarbe beim Drücken)
        self.info=info
        
        self.algorithmus = HEM.EigenerAlgorithmus()
        self.malfenster = draw.Malprogramm()
        self.malfenster.lerne_GUI_kennen(self)
        try:
            self.roboter = ROBO.Roboter()
        except:
            pass
        
        self.fenster=Tk()
        self.fenster.title("Netflix")
        #self.fenster.geometry("1440x900+2000+50")
        

        fensterbreite = 1440
        fensterhöhe = 900
        x = (self.fenster.winfo_screenwidth() - fensterbreite) // 2
        y = (self.fenster.winfo_screenheight() - fensterhöhe) // 2
        self.fenster.geometry(f"{fensterbreite}x{fensterhöhe}+{x}+{y}")
        
        self.fenster.configure(background=self.farben[0])

        #Tableiste
        self.akt_Tab = 0
        tabbuttoninhalt = ("Jetzt Zeichnen", "Bild öffnen", "JSON-Datei öffnen", "Bild malen")
        self.tabbuttons = []
        for i in range(len(tabbuttoninhalt)):
            tabbutton = Button(self.fenster, text = tabbuttoninhalt[i], font=("TkDefaultFont", 12), relief=FLAT, activebackground=self.farben[5],activeforeground=self.farben[6], bg=self.farben[3], fg = self.farben[1], width=20, height=1, command=partial(self.tabwechseln, i))
            tabbutton.place(x = i*190, y = 0)
            self.tabbuttons.append(tabbutton)

        self.tabbuttons[self.akt_Tab].configure(bg=self.farben[4])

        self.objektliste = [] # Alle TKinter-Objekte werden hierdrin gespeichert um sie schnell beim Tabwechsel löschen zu können

        self.zeit_VAR = StringVar(self.fenster, "ca 0 min, 0 s")
        
        self.imMainloop()

    def imMainloop(self):

        if self.akt_Tab == 0:
            self.jetztzeichnen()

        if self.akt_Tab == 3:
            self.malfenster.oberfläche()
        if self.akt_Tab == 4:
            self.qrgui.oberfläche()

        self.fenster.mainloop()

    def tabwechseln(self, tab):
        if tab == self.akt_Tab:
            return #nur bei Tabwechsel wird was gemacht
        else:
            self.akt_Tab = tab
            if tab == 1:
                self.bildÖffnen(True)
                #zu "Jetzt Zeichnen" wechseln
                self.tabwechseln(0)

            elif tab == 2:
                self.malfenster.jsonÖffnen()
                #zum "Malprogramm" wechseln
                self.tabwechseln(3)
                
            else:
                #alte Objekte löschen
                for i in self.objektliste:
                    i.destroy()

                # Tabbuttonfarbe aktualisieren
                for i in self.tabbuttons:
                    i.configure(bg=self.farben[3])
                self.tabbuttons[self.akt_Tab].configure(bg=self.farben[4])

                #neue Objekte setzen
                self.imMainloop()

    def jetztzeichnen(self):
        #Canvas
        self.canvas = Canvas(self.fenster, width = 1280, height= 720, border=-2, bg = self.farben[2])
        self.canvas.place(x = 115, y = 50)
        self.objektliste.append(self.canvas)

        #Buttons
        self.toleranzAnpassen_BTN = Button(self.fenster, text = "Toleranz anpassen", activebackground="#FF2223", bg=self.farben[0],fg = self.farben[1], width=13, height=1, command=self.toleranzAnpassen)
        self.toleranzAnpassen_BTN.place(x = 1300, y = 790)
        self.objektliste.append(self.toleranzAnpassen_BTN)

        self.kalibrierung_BTN = Button(self.fenster, text = "Kalibrieren", activebackground="#FF2223", bg=self.farben[0],fg = self.farben[1], width=13, height=1, command=self.kalibrierungsfensterErstellen)
        self.kalibrierung_BTN.place(x = 1300, y = 15)
        self.objektliste.append(self.kalibrierung_BTN)

        self.MALEN_BTN = Button(self.fenster, text = "MALEN", activebackground="#55aa00", bg=self.farben[0],fg = self.farben[1], width=13, height=1, command=self.malen)
        self.MALEN_BTN.place(x = 1300, y = 850)
        self.objektliste.append(self.MALEN_BTN)


        labelinhalt = (("Kontrast-\ntoleranz:", "Dopplungs-\ntoleranz:"),("minimale\nStrichlänge:", "Lücken-\ntoleranz:"))
        scale_to = ((255,10),(50,10))
        setwerte = ((170,0),(10,3))

        self.labelliste=[]
        self.scaleliste=[] # [Kontrast, Dopplung, minStrich, Lücken]
        
        for i in range(0,2):
            for j in range(0,2):
                label = Label(self.fenster,text=labelinhalt[i][j],bg=self.farben[0],fg = self.farben[1],activebackground = self.farben[5],justify=LEFT)
                label.place(x = ((j*650)+115)-80, y = ((i*50)+790))

                scale = Scale(self.fenster, from_=0, to=scale_to[i][j], orient=HORIZONTAL, bg=self.farben[0],fg = self.farben[1], relief=FLAT, length=550-(j*50),activebackground = self.farben[5],highlightbackground=self.farben[2],troughcolor=self.farben[2], border = 0)
                scale.place(x = ((j*650)+115), y= ((i*50)+790))
                scale.set(setwerte[i][j])

                self.labelliste.append(label)
                self.scaleliste.append(scale)

        self.objektliste+=self.labelliste
        self.objektliste+=self.scaleliste

        #Checkbutton
        self.instantZeichnen_VAR = BooleanVar(self.fenster,False)
        
        self.instantZeichnen_CHB = Checkbutton(self.fenster, text = "sofort Zeichnen", bg = self.farben[0], activebackground = self.farben[0],activeforeground=self.farben[6],fg = self.farben[1],variable = self.instantZeichnen_VAR)
        self.instantZeichnen_CHB.place(x = 1300, y = 815)
        self.instantZeichnen_CHB.select()
        self.objektliste.append(self.instantZeichnen_CHB)

        #HIER BEEEEEEEEEEEEN DAS IST DAZUGEKOMMEN
        
        self.zeit_LBL = Label(self.fenster,textvariable = self.zeit_VAR ,bg=self.farben[0],fg = self.farben[1],activebackground = self.farben[5],justify=LEFT)
        self.zeit_LBL.place(x = 1300, y = 877)
        self.objektliste.append(self.zeit_LBL)
        
        if self.algorithmus.zeit != 0: # Bild exisitiert
            self.turtle()
            self.fenster.update()


    

    def malen(self, liste = None):
        self.roboter.reset(True)
        try:
            if liste == None:
                strichliste = self.algorithmus.strichliste
                bildbreite = len(self.algorithmus.edges[0])
                bildhöhe = len(self.algorithmus.edges)
            else:
                strichliste = liste
                bildbreite = self.malfenster.canvasbreite
                bildhöhe = self.malfenster.canvashöhe
        except NameError:
            print("abbruch")
            return
        
        
        self.roboter.bildZeichnen(strichliste, (bildbreite, bildhöhe))

    def kalibrierungsfensterErstellen(self):
        # kafe = Kaliebrierungs-Fenster
        self.roboter.reset(True)
        self.kafe = Toplevel()
        self.kafe.geometry("300x170")
        self.kafe.configure(background=self.farben[0])
        self.eckliste = ["untererBildrand", "OL", "OR", "UR", "UL"]
        self.akt_ecklisten_index = 0

        self.roboter.gehezuEcke(self.eckliste[self.akt_ecklisten_index]) # zur ersten Ecke gehen

        #Label
        self.anzeige_LBL = Label(self.kafe, text = "aktueller Schritt: "+self.eckliste[0], bg=self.farben[0])
        self.anzeige_LBL.place(x = 15, y = 10)
        
        self.kafevelo_LBL = Label(self.kafe, text = "Geschwindigkeit der Kalibrierung", bg=self.farben[0])
        self.kafevelo_LBL.place(x = 15, y = 60)

        #Buttons
        self.näher_BTN = Button(self.kafe, text = "höher", activebackground="#777777", bg=self.farben[0], width=13, height=1, command=self.kalibrierungs_NÄHER)
        self.näher_BTN.place(x = 15, y = 30)

        self.ferner_BTN = Button(self.kafe, text = "tiefer", activebackground="#777777", bg=self.farben[0], width=13, height=1, command=self.kalibrierungs_FERNER)
        self.ferner_BTN.place(x = 150, y = 30)

        self.nächster_BTN = Button(self.kafe, text = "nächster Kalibrierungsschritt", activebackground="#777777", bg=self.farben[0], width=32, height=1, command=self.kalibrierung_NÄCHSTE)
        self.nächster_BTN.place(x = 15, y = 130)

        #Scales
        self.kalibrierungsgeschwindigkeit_SCL = Scale(self.kafe, from_=1, to=20, orient=HORIZONTAL, bg=self.farben[0], relief=FLAT, length=250, border = 0)
        self.kalibrierungsgeschwindigkeit_SCL.place(x=15, y=80)
        self.kalibrierungsgeschwindigkeit_SCL.set(10)


    def kalibrierungs_NÄHER(self):
        if self.akt_ecklisten_index == 0:
            z = True
        else:
            z = False
        self.roboter.kalibrierung(self.kalibrierungsgeschwindigkeit_SCL.get(), z)

    def kalibrierungs_FERNER(self):
        if self.akt_ecklisten_index == 0:
            z = True
        else:
            z = False
        self.roboter.kalibrierung(-1 * self.kalibrierungsgeschwindigkeit_SCL.get(), z)

    def kalibrierung_NÄCHSTE(self):
        self.roboter.vierPunkteKalibrierung(self.eckliste[self.akt_ecklisten_index]) # aktuelle Position eintragen

        self.näher_BTN.config(text="näher")
        self.ferner_BTN.config(text="ferner")
        
        if self.akt_ecklisten_index == 4: # Nach allen 4 Ecken kafe schließen
            self.roboter.saveKalibrierungspunkte()
            self.roboter.stift_absetzen()
            self.kafe.destroy()
            self.roboter.reset(True)
            return
        else:
            self.akt_ecklisten_index += 1
        
        self.anzeige_LBL.configure(text = "aktuelle Ecke: "+self.eckliste[self.akt_ecklisten_index])
        self.roboter.gehezuEcke(self.eckliste[self.akt_ecklisten_index]) # zur nächsten Ecke gehen

    def bildÖffnen(self, tabwechsel = False): #bei Tabwechsel = True --> kein Turtle malen
        filepath = fd.askopenfilename(filetypes = [("Bild", "*.jpg;*.jpeg;*.png")])
        self.algorithmus.imgpath = filepath
        if self.algorithmus.konvertieren(self.info) == True:

            self.update_Zeit()
            if tabwechsel == False:
                self.turtle()
        else:
            print("Error beim Erkennen des Bildes")

    def update_Zeit(self):
        minuten = int(self.algorithmus.zeit // 60)
        sekunden = int(round(self.algorithmus.zeit % 60, -1))
        zeit = f"ca. {minuten} min, {sekunden} s"
        print(zeit)
        self.zeit_VAR.set(zeit)
        self.fenster.update()


    def toleranzAnpassen(self): #self.scaleliste = [Kontrast, Dopplung, minStrich, Lücken]
        self.algorithmus.wert = 255-self.scaleliste[0].get()
        self.algorithmus.min_strichlänge = self.scaleliste[2].get()
        self.algorithmus.doppungstoleranz = self.scaleliste[1].get()
        self.algorithmus.lückentoleranz = self.scaleliste[3].get()+1

        if self.algorithmus.konvertieren(self.info) == True:
            self.update_Zeit()
            self.turtle()

    def getVerhältnis(self, edges):
        bildbreite = len(edges[0])
        bildhöhe = len(edges)
        bildverhältnis1 = (bildbreite) / (bildhöhe)
        bildverhältnis2 = (bildhöhe) / (bildbreite)
        
        #Beide Möglichkeiten durchgehen, erst Bild an Canvasbreite anpassen, dann an Canvashöhe und gucken was besser ist
        canvasbreite = 1280
        canvashöhe = 720
        x = int(canvasbreite)
        y = int(canvasbreite * bildverhältnis2)
        if x > canvashöhe:
            y=0
        tupel1 = (x,y)
        
        x = int(canvashöhe * bildverhältnis1)
        y = int(canvashöhe)
        if y > canvasbreite:
            x=0
        tupel2 = (x,y)

        if (tupel1[0] * tupel1[1]) > (tupel2[0] * tupel2[1]): # besseres Format mithilfe vom Flächeninhalt herausfinden
            #print(canvasbreite/bildbreite)
            #print(canvashöhe/bildhöhe)
            self.verhältnis = canvasbreite/bildbreite
            return tupel1
        else:
            #print(canvasbreite/bildbreite)
            #print(canvashöhe/bildhöhe)
            self.verhältnis = canvashöhe/bildhöhe
            return tupel2


    def turtle(self):
        verhältnis = self.getVerhältnis(self.algorithmus.edges)
        #print(verhältnis)
        self.canvas.delete("all")
        screen = TurtleScreen(self.canvas)
        t = turtle.RawTurtle(screen)
        t.shape("circle")
        t.color("black")
        t.speed(0)
        versatz_x = (len(self.algorithmus.edges[0]))/2
        versatz_y = (len(self.algorithmus.edges))/2
        t.pensize(3)
        t.hideturtle()
        if self.instantZeichnen_VAR.get():
            t._tracer(0)
        t.penup()
        for strich in self.algorithmus.strichliste:
            t.goto(round((strich[0][0]-versatz_x)*self.verhältnis), round((strich[0][1]*(-1)+versatz_y)*self.verhältnis))
            t.pendown()
            for relcord in strich:
                if relcord != strich[0]:
                    turtx,turty=t.pos()
                    t.goto(round(turtx+(relcord[0])*self.verhältnis),round(turty+(relcord[1]*(-1))*self.verhältnis))
                    #t.goto(turtx+(relcord[0]),turty+(relcord[1]*(-1)))
            t.penup()
            t.color("black")
        t.goto(100*len(self.algorithmus.edges[0])*2,100*len(self.algorithmus.edges)*2)


B = Benutzeroberfläche(True)
