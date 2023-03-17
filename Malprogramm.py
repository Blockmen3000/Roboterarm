from tkinter import *
from functools import partial
import json
from tkinter import filedialog as fd

        
class Malprogramm:
    def __init__(self):
        
        self.strichliste = []
        self.stiftgroesse = 2

        self.rückgängigliste = []
        self.strich = []
        
        self.canvasbreite = 1200
        self.canvashöhe = 820
        
    def oberfläche(self): # zeigt Oberfläche an
        # [0] = Background
        # [1] = Text
        # [2] = Canvas
        # [3] = Tabbuttonfarbe
        # [4] = aktuelle Tabfarbe
        # [5] = Standard-ActiveBackground (nicht bei Klaibrieren, Zeichnen oder Toleranz anpassen, weil dort schon rot und grün zum Einsatz kommen)
        # [6] = Standard-ActiveForeground (Textfarbe beim Drücken)

        self.hauptfenster = self.gui.fenster

        #Canvas
        self.malFenster_CNV = Canvas(self.hauptfenster, width=self.canvasbreite, height=self.canvashöhe, bg=self.gui.farben[2], border=-2)
        self.malFenster_CNV.place(x=30, y=50)
        self.gui.objektliste.append(self.malFenster_CNV)

        #Buttons
        self.leeren_BTN = Button(self.hauptfenster, text="alles Löschen",command=self.löschen,bg=self.gui.farben[0], fg=self.gui.farben[1], activebackground = self.gui.farben[5], activeforeground = self.gui.farben[6])
        self.leeren_BTN.place(x=1250,y=85)
        self.gui.objektliste.append(self.leeren_BTN)

        self.rückgängig_BTN = Button(self.hauptfenster, text="rückgängig",command=self.rückgängig,bg=self.gui.farben[0], fg=self.gui.farben[1], activebackground = self.gui.farben[5], activeforeground = self.gui.farben[6])
        self.rückgängig_BTN.place(x=1250,y=50)
        self.gui.objektliste.append(self.rückgängig_BTN)
        self.vorgängig_BTN = Button(self.hauptfenster, text="vorgängig",command=self.vorgängig,bg=self.gui.farben[0], fg=self.gui.farben[1], activebackground = self.gui.farben[5], activeforeground = self.gui.farben[6])
        self.vorgängig_BTN.place(x=1330,y=50)
        self.gui.objektliste.append(self.vorgängig_BTN)

        self.json_BTN = Button(self.hauptfenster, text="als Strili-Datei speichern",command=self.json_speichern,bg=self.gui.farben[0], fg=self.gui.farben[1], activebackground = "#55aa00", activeforeground = self.gui.farben[6])
        self.json_BTN.place(x=1250,y=810)
        self.gui.objektliste.append(self.json_BTN)
        self.malen_BTN = Button(self.hauptfenster, text="jetzt malen",command=self.jetzt_malen,bg=self.gui.farben[0], fg=self.gui.farben[1], activebackground = "#55aa00", activeforeground = self.gui.farben[6])
        self.malen_BTN.place(x=1250,y=845)
        self.gui.objektliste.append(self.malen_BTN)

        #Label
        self.minPunktabst_LBL = Label(self.hauptfenster, text = "minimaler\nPunktabstand", fg = self.gui.farben[1], bg=self.gui.farben[0],justify=LEFT)
        self.minPunktabst_LBL.place(x=1250, y=120)
        self.gui.objektliste.append(self.minPunktabst_LBL)

        #Scale
        self.größe_SCL = Scale(self.hauptfenster, from_=100, to=0, orient=VERTICAL, bg=self.gui.farben[0],fg = self.gui.farben[1], relief=FLAT, length=635, activebackground = self.gui.farben[5],highlightbackground=self.gui.farben[2],troughcolor=self.gui.farben[2], border = 0)
        self.größe_SCL.place(x=1250, y=160)
        self.größe_SCL.set(20)
        self.gui.objektliste.append(self.größe_SCL)

        #Events
        self.malFenster_CNV.bind(sequence="<B1-Motion>",func=self.male)
        self.malFenster_CNV.bind(sequence="<Button-1>",func=self.male)
        self.malFenster_CNV.bind(sequence="<ButtonRelease-1>",func=self.speicher_linie)
        
        self.hauptfenster.bind(sequence="<MouseWheel>", func=self.scroll)
        self.hauptfenster.bind(sequence='<Control-z>', func=self.rückgängig)
        self.hauptfenster.bind(sequence='<Control-y>', func=self.vorgängig)

        self.hauptfenster.bind(sequence='<BackSpace>', func=self.löschen)
        self.hauptfenster.bind(sequence='<Delete>', func=self.löschen)

        if self.strichliste != []:
            self.male_nach_koordinaten(self.strichliste)
            self.buttons_aktualisieren()


    def lerne_GUI_kennen(self, guiklasse):
        self.gui = guiklasse

    def scroll(self, event):
        if event.delta == 120: #hochscrollen
            self.größe_SCL.set(self.größe_SCL.get()+5)
        else: #runterscrollen
            self.größe_SCL.set(self.größe_SCL.get()-5)


    def jsonÖffnen(self):
        filepath = fd.askopenfilename(filetypes = [("Strichliste", ".strili")])

        if filepath != "":
            with open(filepath) as f:
                content = f.read()
                if content:
                    strichliste = json.loads(content)
                else:
                    print("Datei beschädigt")
                    strichliste = []
                f.close()
            self.strichliste = strichliste
            self.rückgängigliste = []

        else:
            print("Error beim Erkennen der Strili-Datei")

    def json_speichern(self):
        liste = self.strichliste # ABSOLUTE KOORDINATEN WERDEN IN STRILIs GESPEICHERT!!!
        name=fd.asksaveasfilename(defaultextension=".strili", filetypes = [("Strichliste", ".strili")])
        if name != "":
            with open(name, 'w', encoding='utf-8') as f:
                json.dump(liste, f, ensure_ascii=False, indent=4)
                f.close()

    def jetzt_malen(self):
        liste = self.wandleabsolutekoordinateninrelativeum()
        fertige_liste = self.gui.algorithmus.diagonaleLinienZusammenfasssen(self.gui.algorithmus.geradeLinienZusammenfassen(liste)) # Unübersichtlich aber super weil weniger Variablen -> EFFIZIENZ (+Mathis nerven macht Spaß)
        self.gui.malen(fertige_liste)

    def löschen(self, event=None): # ["RESET", [Strich1], [Strich2], ...], [Srich], [(x,y), (x,y)], ["RESET", [(x,y),(x,y)],[(x,y),(x,y)], [(x,y),(x,y)]]
        self.malFenster_CNV.delete("all")
        self.resetliste = []
        for i in range(len(self.strichliste)):
            self.resetliste.append(self.strichliste[i])
        
        self.strichliste = ["RESET"]

    def rückgängig(self, event=None):
        if len(self.strichliste) != 0:
            if self.strichliste == ["RESET"]:
                self.strichliste=[]
                for i in self.resetliste:
                    self.strichliste.append(i)
                self.male_nach_koordinaten(self.strichliste)
            else:
                self.rückgängigliste.append(self.strichliste.pop(-1))
                if len(self.rückgängigliste) > 100:
                    self.rückgängigliste.pop(0)

                self.male_nach_koordinaten(self.strichliste)
        self.buttons_aktualisieren()
        

    def vorgängig(self, event=None):
        if len(self.rückgängigliste) != 0:
            self.strichliste.append(self.rückgängigliste.pop(-1))
            
            self.male_nach_koordinaten(self.strichliste)
        self.buttons_aktualisieren()

    def buttons_aktualisieren(self):
        if len(self.rückgängigliste) == 0:
            self.vorgängig_BTN.config(state=DISABLED)
        else:
            self.vorgängig_BTN.config(state=NORMAL)
            
        if len(self.strichliste) == 0:
            self.rückgängig_BTN.config(state=DISABLED)
        else:
            self.rückgängig_BTN.config(state=NORMAL)
            

    def male_nach_koordinaten(self, liste):
        self.malFenster_CNV.delete("all")
        for strichliste in range(len(liste)):
            if liste[strichliste] != "RESET":
                for strich in range(len(liste[strichliste])):
                    for punkt in range(len(liste[strichliste][strich])):
                        x = liste[strichliste][strich][punkt][0] # bei x ohne Differenz und bei y mit, weil Umwandlung von Bild-Koordinatensystem zu mathematischen Koordinatensystem (Quadrant 1)
                        y = self.canvashöhe - liste[strichliste][strich][punkt][1]
                        self.malFenster_CNV.create_oval(x-self.stiftgroesse/2,y-self.stiftgroesse/2,x+self.stiftgroesse/2,y+self.stiftgroesse/2,fill = "black",outline="")
                        if punkt > 0:
                            x_alt = liste[strichliste][strich][punkt-1][0]
                            y_alt = self.canvashöhe - liste[strichliste][strich][punkt-1][1]
                            self.malFenster_CNV.create_line(x, y, x_alt, y_alt, width = self.stiftgroesse)
            
        
    def male(self, event):
        if event.x >= 0 and event.x <= self.canvasbreite and event.y >= 0 and event.y <= self.canvashöhe:
            if len(self.strich) > 0:
                abstand_x = event.x - self.strich[-1][0]
                abstand_y = (self.canvashöhe - event.y) - self.strich[-1][1]
                abstand = ((abstand_x ** 2) + (abstand_y ** 2)) ** 0.5 #Satz des Pythangoras --> Betrag des Vektors zum letzten Punkt
            else:
                abstand = 1000000000000000000000000000000
            
            if abstand > self.größe_SCL.get()+1:
                self.malFenster_CNV.create_oval(event.x-self.stiftgroesse/2,event.y-self.stiftgroesse/2,event.x+self.stiftgroesse/2,event.y+self.stiftgroesse/2,fill="black",outline="")
                if len(self.strich) > 0:
                    self.malFenster_CNV.create_line(event.x, event.y,self.strich[-1][0], self.canvashöhe - self.strich[-1][1], width = self.stiftgroesse)

                self.strich.append([event.x, self.canvashöhe - event.y])



    def speicher_linie(self, event):
        #print(self.strichliste)
        self.strichliste.append([self.strich])
        self.strich = []
        self.buttons_aktualisieren()
            

    def wandleabsolutekoordinateninrelativeum(self):
        rel_strichliste = []
        for strichliste in range(len(self.strichliste)):
            if self.strichliste[strichliste] != "RESET":
                append_strich = []
                for strich in range(len(self.strichliste[strichliste])):
                    for punkt in range(len(self.strichliste[strichliste][strich])):
                        if punkt == 0:
                            x = self.strichliste[strichliste][strich][punkt][0]
                            y = self.canvashöhe - self.strichliste[strichliste][strich][punkt][1]
                            append_strich.append((x,y))
                        else:
                            unterschied_x = self.strichliste[strichliste][strich][punkt][0] - self.strichliste[strichliste][strich][punkt-1][0]
                            unterschied_y = self.strichliste[strichliste][strich][punkt][1] - self.strichliste[strichliste][strich][punkt-1][1]
                            append_strich.append((unterschied_x, unterschied_y*(-1)))
                rel_strichliste.append(append_strich)

        return rel_strichliste





#Hauptprogramm

#fenster=Ui()
