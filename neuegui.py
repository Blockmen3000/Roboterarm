import json
import numpy as np
from tkinter import *
from tkinter import filedialog as fd
from PIL import Image as im
from PIL import ImageTk
from functools import partial
import HEMalgorithmus as HEM
import Malprogramm as draw
import customtkinter
#import QR_GUI_QR as qrgui

try:
    import roboter as ROBO
except:
    print("kein Roboter verfügbar")
import turtle
from turtle import TurtleScreen, ScrolledCanvas, RawTurtle

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class Tabs(customtkinter.CTkTabview):
    def __init__(self, master, info=False, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Home")
        self.add("Bild zeichnen")
        self.add("QR")

        self.info=info
        
        self.algorithmus = HEM.EigenerAlgorithmus()
        self.malfenster = draw.Malprogramm()
        self.malfenster.lerne_GUI_kennen(self)
        #self.qrgui= qrgui.QRGUI()
        #self.qrgui.lerne_GUI_kennen(self)
        try:
            self.roboter = ROBO.Roboter()
        except:
            pass

        self.canvas = Canvas(master=self.tab("Home"), width = 1280, height= 720, border=-2, bg = "white")
        self.canvas.place(x = 100, y = 10)

        self.toleranzAnpassen_BTN = customtkinter.CTkButton(master=self.tab("Home"), text = "Toleranz anpassen", corner_radius=8, command=self.toleranzAnpassen)
        self.toleranzAnpassen_BTN.place(x = 1400, y = 80)

        self.kalibrierung_BTN = customtkinter.CTkButton(master=self.tab("Home"), text = "Kalibrieren", corner_radius=8, command=self.kalibrierungsfensterErstellen)
        self.kalibrierung_BTN.place(x = 1400, y = 10)

        self.MALEN_BTN = customtkinter.CTkButton(master=self.tab("Home"), text = "MALEN", corner_radius=8, command=self.malen)
        self.MALEN_BTN.place(x = 1400, y = 150)

        #Scales
        self.größe_SCL = customtkinter.CTkSlider(master=self.tab("Home"), from_=100, to=0, orientation="vertical", height=600)
        self.größe_SCL.place(x=40, y=48)
        self.größe_SCL.set(100)

        labelinhalt = (("Kontrast-\ntoleranz:", "Dopplungs-\ntoleranz:"),("minimale\nStrichlänge:", "Lücken-\ntoleranz:"))
        scale_to = ((255,10),(50,10))
        setwerte = ((170,0),(10,3))


        for i in range(0,2):
            for j in range(0,2):
                label = customtkinter.CTkLabel(master=self.tab("Home"),text=labelinhalt[i][j],justify=LEFT)
                label.place(x = ((j*650)+115)-80, y = ((i*50)+750))

                scale = customtkinter.CTkSlider(master=self.tab("Home"), from_=0, to=scale_to[i][j], width=500)
                scale.place(x = ((j*650)+115), y= ((i*50)+750))
                scale.set(setwerte[i][j])

        #Checkbutton
        self.instantZeichnen_VAR = BooleanVar(self.tab("Home"),False)
        
        self.instantZeichnen_CHB = customtkinter.CTkCheckBox(master=self.tab("Home"), text = "sofort Zeichnen",variable = self.instantZeichnen_VAR)
        self.instantZeichnen_CHB.place(x = 1300, y = 815)
        self.instantZeichnen_CHB.select()
        
        if self.algorithmus.konvertieren(self.info) == True:
            self.turtle()        
        
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
            if tabwechsel == False:
                self.turtle()
        else:
            print("Error beim Erkennen des Bildes")


    def toleranzAnpassen(self): #self.scaleliste = [Kontrast, Dopplung, minStrich, Lücken]
        self.algorithmus.wert = 255-self.scaleliste[0].get()
        self.algorithmus.min_strichlänge = self.scaleliste[2].get()
        self.algorithmus.doppungstoleranz = self.scaleliste[1].get()
        self.algorithmus.lückentoleranz = self.scaleliste[3].get()+1

        for i in range(len(self.scaleliste)):
            print(self.scaleliste[i].get(), self.labelliste[i].configure(text=i))

        if self.algorithmus.konvertieren(self.info) == True:
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
            print(canvasbreite/bildbreite)
            print(canvashöhe/bildhöhe)
            self.verhältnis = canvasbreite/bildbreite
            return tupel1
        else:
            print(canvasbreite/bildbreite)
            print(canvashöhe/bildhöhe)
            self.verhältnis = canvashöhe/bildhöhe
            return tupel2


    def turtle(self):
        verhältnis = self.getVerhältnis(self.algorithmus.edges)
        print(verhältnis)
        self.canvas.delete("all")
        screen = TurtleScreen(self.canvas)
        t = turtle.RawTurtle(screen)
        t.shape("circle")
        t.color("black")
        t.speed(0)
        versatz_x = (len(self.algorithmus.edges[0]))/2
        versatz_y = (len(self.algorithmus.edges))/2
        t.pensize(3)
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


class App():
    def __init__(self,info=False):
        super().__init__()

        self.info=info
        
        #self.algorithmus = HEM.EigenerAlgorithmus()
        #self.malfenster = draw.Malprogramm()
        #self.malfenster.lerne_GUI_kennen(self)
        #self.qrgui= qrgui.QRGUI()
        #self.qrgui.lerne_GUI_kennen(self)
        try:
            self.roboter = ROBO.Roboter()
        except:
            pass

        self.fenster=customtkinter.CTk()
        self.fenster.title("Netflix")
        #self.fenster.geometry("1440x2950")


        fensterbreite = 1700
        fensterhöhe = 950
        x = (self.fenster.winfo_screenwidth() - fensterbreite) // 2
        y = (self.fenster.winfo_screenheight() - fensterhöhe) // 2
        self.fenster.geometry(f"{fensterbreite}x{fensterhöhe}+{x}+{y}")
        

        self.tab_view = Tabs(master=self.fenster,height=fensterhöhe-50,width=fensterbreite-50)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)


app = App()
app.fenster.mainloop()
