from tkinter import *
import turtle
from turtle import TurtleScreen, ScrolledCanvas, RawTurtle

class QRGUI:
    def __init__(self):
        pass
    def oberfläche(self):
        # [0] = Background
        # [1] = Text
        # [2] = Canvas
        # [3] = Tabbuttonfarbe
        # [4] = aktuelle Tabfarbe
        # [5] = Standard-ActiveBackground (nicht bei Klaibrieren, Zeichnen oder Toleranz anpassen, weil dort schon rot und grün zum Einsatz kommen)
        # [6] = Standard-ActiveForeground (Textfarbe beim Drücken)

        self.hauptfenster = self.gui.fenster

        self.linkeingabe_ENT = Entry(self.hauptfenster,font=("TkDefaultFont",30),width=44,fg="#0140A0")
        self.linkeingabe_ENT.place(x=29,y=69)
        self.gui.objektliste.append(self.linkeingabe_ENT)

        self.eingabebutton = Button(self.hauptfenster,font=("TkDefaultFont",19),text = "Bestaeätigen",command=self.ready)
        self.eingabebutton.place(x=1029,y=69)
        self.gui.objektliste.append(self.eingabebutton)

        self.vorschau_CNV = Canvas(self.hauptfenster,width = 666,height=666)
        self.vorschau_CNV.place(x=29,y=150)
        self.gui.objektliste.append(self.vorschau_CNV)

        self.anzahl_striche_SCL = Scale(self.hauptfenster)
        
    def lerne_GUI_kennen(self, guiklasse):
        self.gui = guiklasse

    def ready(self):
        print("Der Button wurde geddrueckt!!!! OMG. Was passiert jetzt nur? \n Was sollen wir jetzt tun?")
        text = self.linkeingabe_ENT.get()
        qrcodegroesse = 15
        strichliste = self.gui.algorithmus.mache_qrcode__yey(text,qrcodegroesse,"H")
        max_koordinatzen=self.suche_max_koordinaten(strichliste)
        self.turtle(max_koordinatzen,strichliste)
        self.gui.malen(strichliste)

    def suche_max_koordinaten(self,strichliste):
        x_max=0
        y_max=0
        
        for strich in strichliste:
            start_x,start_y = strich[0]
            if strich[0][0] > x_max:
                x_max=strich[0][0]
            if strich[0][1] > y_max:
                y_max=strich[0][1]
            for punkt in strich[1:]:
                start_x+= punkt[0]
                start_y+= punkt[1]
                if start_x > x_max:
                    x_max = start_x
                if start_y > y_max:
                    y_max = start_y
        return (x_max,y_max)
                    

    def turtle(self,bildbreite,strichliste):
        canvasbreite=670
        verhältnis = canvasbreite/bildbreite[0]
        print(verhältnis)
        self.vorschau_CNV.delete("all")
        screen = TurtleScreen(self.vorschau_CNV)
        t = turtle.RawTurtle(screen)
        t.shape("circle")
        t.color("black")
        t.speed(0)
        versatz_x =(strichliste[0][0][0]*verhältnis)+canvasbreite/2
        versatz_y =(strichliste[0][0][1]*verhältnis)+canvasbreite/2
        t.pensize(3)
        t.hideturtle()
        t._tracer(0)
        t.penup()
        for strich in strichliste:
            t.goto((strich[0][0]*verhältnis-versatz_x),(strich[0][1]*(-1)*verhältnis+versatz_y))
            t.pendown()
            for relcord in strich[1:]:
                if relcord != strich[0]:
                    turtx,turty=t.pos()
                    t.goto(turtx+(relcord[0])*verhältnis,turty+(relcord[1]*(-1))*verhältnis)
                    #t.goto(turtx+(relcord[0]),turty+(relcord[1]*(-1)))
            t.penup()
            t.color("black")
        t.goto(100*bildbreite[0]*2,100*bildbreite[1]*2)


#Großer QRCode mit soooo viel Text, dass selbst das Entry Widget nicht lang genug ist, um alles auf ein Mal anzuzeigen.
