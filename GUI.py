#Version 1.1
import numpy as np
from tkinter import *
from tkinter import filedialog as fd
from PIL import Image as im
from PIL import ImageTk
import HEMalgorithmus as HEM
import time
import test as ROBO
import turtle
from turtle import TurtleScreen, ScrolledCanvas, RawTurtle

class Benutzeroberfläche:
    def __init__(self,info=False):
        self.algorithmus = HEM.EigenerAlgorithmus()
        self.roboter = ROBO.Roboter()
        
        self.fenster=Tk()
        self.fenster.title("Netflix")
        #self.fenster.geometry("1440x900+2000+50")
        self.info=info

        fensterbreite = 1440
        fensterhöhe = 900
        x = (self.fenster.winfo_screenwidth() - fensterbreite) // 2
        y = (self.fenster.winfo_screenheight() - fensterhöhe) // 2
        self.fenster.geometry(f"{fensterbreite}x{fensterhöhe}+{x}+{y}")
        
        self.fensterfarbe="darkgrey"
        self.fenster.configure(background=self.fensterfarbe)

        #Canvas
        self.canvas = Canvas(self.fenster, width = 1280, height= 720, border=-2, bg = "#DDDDDD")
        self.canvas.place(x = 115, y = 50)

        #Buttons
        self.webcam_BTN = Button(self.fenster, text = "Webcam nutzen", activebackground="#777777", bg=self.fensterfarbe, width=13, height=1, command=self.webcam)
        self.webcam_BTN.place(x = 115, y = 15)
        
        self.bildÖffnen_BTN = Button(self.fenster, text = "Bild öffnen", activebackground="#777777", bg=self.fensterfarbe, width=10, height=1, command=self.bildÖffnen)
        self.bildÖffnen_BTN.place(x = 230, y = 15)

        self.toleranzAnpassen_BTN = Button(self.fenster, text = "Toleranz anpassen", activebackground="#FF2223", bg=self.fensterfarbe, width=13, height=1, command=self.toleranzAnpassen)
        self.toleranzAnpassen_BTN.place(x = 1300, y = 790)

        self.kalibrierung_BTN = Button(self.fenster, text = "Kalibrieren", activebackground="#FF2223", bg=self.fensterfarbe, width=13, height=1, command=self.kalibrierungsfensterErstellen)
        self.kalibrierung_BTN.place(x = 1300, y = 15)

        self.MALEN_BTN = Button(self.fenster, text = "MALEN", activebackground="#55aa00", bg=self.fensterfarbe, width=13, height=1, command=self.malen)
        self.MALEN_BTN.place(x = 1300, y = 840)

        #Scales
        self.größe_SCL = Scale(self.fenster, from_=100, to=0, orient=VERTICAL, bg=self.fensterfarbe, relief=FLAT, length=720, border = 0)
        self.größe_SCL.place(x=40, y=48)
        self.größe_SCL.set(100)

        self.toleranz_LBL = Label(self.fenster,text="Kontrast-\ntoleranz:",bg=self.fensterfarbe,justify=LEFT)
        self.toleranz_LBL.place(x=35,y=790)

        self.toleranz_SCL = Scale(self.fenster, from_=0, to=255, orient=HORIZONTAL, bg=self.fensterfarbe, relief=FLAT, length=550, border = 0)
        self.toleranz_SCL.place(x=115, y=790)
        self.toleranz_SCL.set(80)

        self.dotol_LBL = Label(self.fenster,text="Dopplungs-\ntoleranz:",bg=self.fensterfarbe,justify=LEFT) #dotol: Dopplungstoleranz
        self.dotol_LBL.place(x=690,y=790)

        self.dotol_SCL = Scale(self.fenster, from_=0, to=10, orient=HORIZONTAL, bg=self.fensterfarbe, relief=FLAT, length=500, border = 0)
        self.dotol_SCL.place(x=765, y=790)
        self.dotol_SCL.set(0)

        self.minstrl_LBL = Label(self.fenster,text="minimale\nStrichlänge:",bg=self.fensterfarbe,justify=LEFT) #minstrl: minimale Strichlänge
        self.minstrl_LBL.place(x=35,y=840)

        self.minstrl_SCL = Scale(self.fenster, from_=0, to=50, orient=HORIZONTAL, bg=self.fensterfarbe, relief=FLAT, length=550, border = 0)
        self.minstrl_SCL.place(x=115, y=840)
        self.minstrl_SCL.set(20)

        self.luetol_LBL = Label(self.fenster,text="Lücken-\ntoleranz:",bg=self.fensterfarbe,justify=LEFT) #luetol: Lückentoleranz
        self.luetol_LBL.place(x=690,y=840)

        self.luetol_SCL = Scale(self.fenster, from_=0, to=10, orient=HORIZONTAL, bg=self.fensterfarbe, relief=FLAT, length=500, border = 0)
        self.luetol_SCL.place(x=765, y=840)
        self.luetol_SCL.set(5)

        

        self.fenster.mainloop()

    def malen(self):
        try:
            strichliste = self.algorithmus.strichliste
        except NameError:
            print("abbruch")
            return
        bildbreite = len(self.algorithmus.edges[0])
        bildhöhe = len(self.algorithmus.edges)
        
        self.roboter.bildZeichnen(strichliste, (bildbreite, bildhöhe))
        #self.fenster.wait_variable(self.roboter.weiter)

    def kalibrierungsfensterErstellen(self):
        # kafe = Kaliebrierungs-Fenster
        self.roboter.reset(True)
        self.kafe = Toplevel()
        self.kafe.geometry("300x170")
        self.kafe.configure(background=self.fensterfarbe)
        self.eckliste = ["OL", "OR", "UR", "UL"]
        self.akt_ecklisten_index = 0

        self.roboter.gehezuEcke(self.eckliste[self.akt_ecklisten_index]) # zur ersten Ecke gehen

        #Label
        self.anzeige_LBL = Label(self.kafe, text = "aktuelle Ecke: "+self.eckliste[0], bg=self.fensterfarbe)
        self.anzeige_LBL.place(x = 15, y = 10)
        
        self.kafevelo_LBL = Label(self.kafe, text = "Geschwindigkeit der Kalibrierung", bg=self.fensterfarbe)
        self.kafevelo_LBL.place(x = 15, y = 60)

        #Buttons
        self.näher_BTN = Button(self.kafe, text = "näher", activebackground="#777777", bg=self.fensterfarbe, width=13, height=1, command=self.kalibrierungs_NÄHER)
        self.näher_BTN.place(x = 15, y = 30)

        self.ferner_BTN = Button(self.kafe, text = "ferner", activebackground="#777777", bg=self.fensterfarbe, width=13, height=1, command=self.kalibrierungs_FERNER)
        self.ferner_BTN.place(x = 150, y = 30)

        self.nächster_BTN = Button(self.kafe, text = "nächster Kalibrierungsschritt", activebackground="#777777", bg=self.fensterfarbe, width=32, height=1, command=self.kalibrierung_NÄCHSTE)
        self.nächster_BTN.place(x = 15, y = 130)

        #Scales
        self.kalibrierungsgeschwindigkeit_SCL = Scale(self.kafe, from_=1, to=20, orient=HORIZONTAL, bg=self.fensterfarbe, relief=FLAT, length=250, border = 0)
        self.kalibrierungsgeschwindigkeit_SCL.place(x=15, y=80)
        self.kalibrierungsgeschwindigkeit_SCL.set(10)


    def kalibrierungs_NÄHER(self):
        self.roboter.kalibrierung(self.kalibrierungsgeschwindigkeit_SCL.get())

    def kalibrierungs_FERNER(self):
        self.roboter.kalibrierung(-1 * self.kalibrierungsgeschwindigkeit_SCL.get())

    def kalibrierung_NÄCHSTE(self):
        self.roboter.vierPunkteKalibrierung(self.eckliste[self.akt_ecklisten_index]) # aktuelle Position eintragen
        
        if self.akt_ecklisten_index == 3: # Nach allen 4 Ecken kafe schließen
            self.roboter.saveKalibrierungspunkte()
            self.roboter.stift_absetzen()
            self.kafe.destroy()
            self.roboter.reset(True)
            return
        else:
            self.akt_ecklisten_index += 1
        
        self.anzeige_LBL.configure(text = "aktuelle Ecke: "+self.eckliste[self.akt_ecklisten_index])
        self.roboter.gehezuEcke(self.eckliste[self.akt_ecklisten_index]) # zur nächsten Ecke gehen

    def webcam(self):
        pass

    def bildÖffnen(self):
        filepath = fd.askopenfilename()
        self.algorithmus.imgpath = filepath
        if self.algorithmus.konvertieren(self.info) == True:
            #self.bildPlazieren()
            self.turtle()
        else:
            print("Error beim Erkennen des Bildes")

    def toleranzAnpassen(self):
        self.algorithmus.wert = 255-self.toleranz_SCL.get()
        self.algorithmus.min_strichlänge = self.minstrl_SCL.get()
        self.algorithmus.lückentoleranz = self.luetol_SCL.get()
        self.algorithmus.doppungstoleranz = self.dotol_SCL.get()
        if self.algorithmus.konvertieren(self.info) == True:
            #self.bildPlazieren()
            self.turtle()

    def bildPlazieren(self):
        for i in self.canvas.find_withtag("BILD"):
            self.canvas.delete(i)
        self.loades_edges = self.algorithmus.edges
        verhältnis = self.getVerhältnis(self.loades_edges)
        self.resized_edges = self.resizeEdges(self.loades_edges, verhältnis[0], verhältnis[1])
        data = im.fromarray(self.resized_edges)
        self.img = ImageTk.PhotoImage(data)
        
        place_x = ((1280-verhältnis[0])/2)
        place_y = ((720-verhältnis[1])/2)
        
        self.canvas.create_image(place_x, place_y, anchor = NW, image = self.img, tag = "BILD")

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

    def resizeEdges(self, edges, newWidth, newHeight):
        oldWidth = len(edges[0])
        oldHeight = len(edges)
        newEdges = np.zeros([newHeight, newWidth]) # neues Array nur mit 0-en in der richtigen Größe erstellt

        # Hier wird entschieden wie verfahren wird. Bei herunterskalieren (also viele werden zu wenigen Pixeln) wird das alte Bild mit den vielen Pixeln durchgegangen.
        # Bei Hochskalierung wird das neue Bild durchgegangen und da wird an den Koordinaten des alten Bilds überprüft, welcher Wert da steht.
        if newWidth < oldWidth:
            for x in range(oldWidth):
                for y in range(oldHeight): #geht jeden Pixel durch
                    xNew = int(x*(newWidth/oldWidth))
                    yNew = int(y*(newHeight/oldHeight)) # bildet Verhältnis zwischen alter und neuer Pixelposition
                    wert = edges[y][x]
                    if wert == 40:
                        wert = 255
                    newEdges[yNew][xNew] = abs(wert-255) # Pixel invertieren
        else:
            for x in range(newWidth):
                for y in range(newHeight): #geht jeden Pixel durch
                    xOld = int(x*(oldWidth/newWidth))
                    yOld = int(y*(oldHeight/newHeight)) # bildet Verhältnis zwischen alter und neuer Pixelposition
                    wert = edges[yOld][xOld]
                    if wert == 40:
                        wert = 255
                    newEdges[y][x] = abs(wert-255) # Pixel invertieren
        return newEdges

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
        t.hideturtle()
        t.goto(len(self.algorithmus.edges[0])*2,len(self.algorithmus.edges)*2)


B = Benutzeroberfläche(True)
