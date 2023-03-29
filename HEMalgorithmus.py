# Version 1.8 (Alpha)
import turtle
import cv2
from time import time
from numpy import zeros
from copy import deepcopy


class EigenerAlgorithmus:
    def __init__(self, img = "", strichlänge=10, wert=85, lückentoleranz = 3,resize=False):
        self.imgpath = img
        self.wert = wert
        self.min_strichlänge = strichlänge
        self.lückentoleranz = lückentoleranz
        self.resize = resize
        self.doppungstoleranz = 0

        self.zeit = 0 # vorraussichtliche Zeit, die für das Malen benötigt wird
    
    def konvertieren(self,info):
        self.zeit = 0
        if self.erkennen()!=True:
            return False

        self.zeit = 10 # 5s für Bewegen zur Startposition + 5s für Bewegen von Endposition

        if info:
            t=time()
            print(f"{len(self.strichliste)} Striche und {self.schritte_zählen()} Schritte erkannt")

        self.kurzeLinienEntfernen()
        
        self.anzahl_schritte_anfang = self.schritte_zählen()
        
        if info:
            print(f"noch {len(self.strichliste)} Striche und {self.schritte_zählen()} Schritte nach dem entfenen kurzer Linien")

        #self.edgesanpassen()

        self.strichliste = self.geradeLinienZusammenfassen(deepcopy(self.strichliste))
        if info:
            print(f"noch {self.schritte_zählen()} Schritte nach dem geraden Zusammenfassen")
        
        self.strichliste = self.diagonaleLinienZusammenfasssen(deepcopy(self.strichliste))
        if info:
            print(f"noch {self.schritte_zählen()} Schritte nach dem diagonalen Zusammenfassen")
            print(f"gesammte Rechendauer: {time()-t} Sekunden")

        self.zeit_berechnen()
        
        return True

    def zeit_berechnen(self):
        schritte = self.schritte_zählen()
        zeit_echte_schritte = schritte * 0.18 #Zeit pro Schritt
        self.zeit += zeit_echte_schritte

        zeit_entfernte_schritte = self.anzahl_schritte_anfang * 0.001 #Zeit pro entfernten Schritt
        self.zeit += zeit_entfernte_schritte

        zeit_anzahl_striche = len(self.strichliste) * 2 #Zeit pro Strich
        self.zeit += zeit_anzahl_striche
    
    def mache_qrcode__yey(self,link,imagesize,errorcor,codesize=None):
        qrcode=RobotQR.erstelle_qr_code(imagesize,codesize,errorcor,link)
        self.qr_array = qrcode
        self.male_qr_code()
        self.geradeLinienZusammenfassen(self.qr_array)
    
    def schritte_zählen(self):
        schritte=0
        for i in self.strichliste:
            schritte+=len(i)
        return schritte
    
    def canny_durchfuehren(self):
        self.img = cv2.imread(self.imgpath)
        if format(self.img) == "None":
            return
        #faktor = 720 / self.img.shape[1]
        #if self.resize == True:
        #    self.img = cv2.resize(self.img, (int(self.img.shape[1] * faktor), int(self.img.shape[0] * faktor)), interpolation= cv2.INTER_LINEAR)
        
        #img = cv2.imread("Permission denied..png")
        self.img = cv2.convertScaleAbs(self.img, alpha=1.3, beta=40)
        
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.edges = cv2.Canny(gray, self.wert, 200)
        #print(self.edges)
        #cv2.imshow("linesEdges", self.edges)
        
    def erkennen(self,bild = True):
        if bild == True:
            self.canny_durchfuehren()
        if format(self.img) == "None":
            return False
#        else:
#            self.edges = self.imgpath
#            pass #Es wurde ein QRCode gegeben
        
        self.auflösung = (len(self.edges[0]), len(self.edges)) #(x,y)
        self.strichliste = []
        for x in range(0, len(self.edges[0])): # alle Pixel durchgehen
            for y in range(0, len(self.edges)):
                if self.edges[y][x] == 255:
                    self.edges[y][x] = 40

                    # Roboter bekommt Liste: strich = [(x,y), (relativx, relativy), (relativx, relativy), ...]
                    
                    nachstrich = [] #Liste mit absoluten Startkooredinaten erstellt
                    x_rel = 0
                    y_rel = 0
                    x_clr = x
                    y_clr = y
                    x_ges = 0
                    y_ges = 0
                    zähler = 0
                    while self.umliegendeErkennen(x + x_rel, y + y_rel) != False:
                        #print("rel",x_rel, y_rel)
                        tupel = self.umliegendeErkennen(x + x_rel, y + y_rel)
                        x_rel += tupel[0]
                        y_rel += tupel[1]
                        self.edges[y + y_rel][x + x_rel] = 40
                        nachstrich.append(tupel) # Einfügen von relativen Koordinaten
                        #print("Strich",strich)
                        if self.doppungstoleranz>0:
                            if len(nachstrich)>2*self.doppungstoleranz: # um striche herum aufräumen
                                for x1 in range(x_clr-self.doppungstoleranz,x_clr+self.doppungstoleranz):
                                    for y1 in range(y_clr-self.doppungstoleranz,y_clr+self.doppungstoleranz):
                                        if x1 >= 0 and y1 >= 0 and x1<len(self.edges[0]) and y1<len(self.edges):
                                            if self.edges[y1][x1] == 255:
                                                self.edges[y1][x1] = 40
                                x_clr += nachstrich[zähler+1][0]
                                y_clr += nachstrich[zähler+1][1]
                                zähler += 1
                    if self.doppungstoleranz>0:
                        for i in range(zähler+1,len(nachstrich)-1):
                            for x1 in range(x_clr-self.doppungstoleranz,x_clr+self.doppungstoleranz):
                                for y1 in range(y_clr-self.doppungstoleranz,y_clr+self.doppungstoleranz):
                                    if x1 >= 0 and y1 >= 0 and x1<len(self.edges[0]) and y1<len(self.edges):
                                        if self.edges[y1][x1] == 255:
                                            self.edges[y1][x1] = 40
                                x_clr += nachstrich[i][0]
                                y_clr += nachstrich[i][1]

                            
                    vorstrich=[]
                    x_ges += x_rel
                    y_ges += y_rel
                    x_rel = 0
                    y_rel = 0
                    x_clr = x
                    y_clr = y
                    zähler = 0
                    while self.umliegendeErkennen(x + x_rel, y + y_rel) != False:
                        #print("rel",x_rel, y_rel)
                        tupel = self.umliegendeErkennen(x + x_rel, y + y_rel)
                        x_rel += tupel[0]
                        y_rel += tupel[1]
                        self.edges[y + y_rel][x + x_rel] = 40
                        vorstrich.append(tupel) # Einfügen von relativen Koordinaten
                        #print("Strich",strich)
                        if self.doppungstoleranz>0:
                            if len(vorstrich)>2*self.doppungstoleranz: # um striche herum aufräumen
                                for x1 in range(x_clr-self.doppungstoleranz,x_clr+self.doppungstoleranz):
                                    for y1 in range(y_clr-self.doppungstoleranz,y_clr+self.doppungstoleranz):
                                        if x1 >= 0 and y1 >= 0 and x1<len(self.edges[0]) and y1<len(self.edges):
                                            if self.edges[y1][x1] == 255:
                                                self.edges[y1][x1] = 40
                                x_clr += vorstrich[zähler+1][0]
                                y_clr += vorstrich[zähler+1][1]
                                zähler += 1
                    if self.doppungstoleranz>0:
                        for i in range(zähler+1,len(vorstrich)-1):
                            for x1 in range(x_clr-self.doppungstoleranz,x_clr+self.doppungstoleranz):
                                for y1 in range(y_clr-self.doppungstoleranz,y_clr+self.doppungstoleranz):
                                    if x1 >= 0 and y1 >= 0 and x1<len(self.edges[0]) and y1<len(self.edges):
                                        if self.edges[y1][x1] == 255:
                                            self.edges[y1][x1] = 40
                                x_clr += vorstrich[i][0]
                                y_clr += vorstrich[i][1]

                    strich=[(x+x_rel,y+y_rel)]
                    
                    for schritt in range(len(vorstrich)-1,-1,-1):
                        strich.append((vorstrich[schritt][0]*(-1),vorstrich[schritt][1]*(-1)))

                    strich+=nachstrich

                    x_ges -= x_rel
                    y_ges -= y_rel
                    if abs(x_ges) <= self.lückentoleranz and abs(y_ges) <= self.lückentoleranz:
                        strich.append((-x_ges,-y_ges))

                    self.strichliste.append(strich)

                    #print(("HAAAAALLLLLLOOOOOO",x_ges,y_ges))
        
        return True

    def umliegendeErkennen(self, x, y):
        for i in range (0, self.lückentoleranz+1):
            for x_rel in range(i, -1-i, -1):
                for y_rel in range(i, -1-i, -1): # nahe umliegende Pixel durchgehen (Abstand i)
                    try:
                        if self.edges[y + y_rel][x + x_rel] == 255:
                            if x >= self.lückentoleranz or x_rel >= 0:
                                return (x_rel, y_rel)
                    except IndexError: #Bildrand
                        pass
        # umliegende Pixel sind nicht weiß --> False zurückgeben
        return False
    
    def male_qr_code(self):
        #self.qr_array = self.imgpath
        self.strichliste=[]
        yzähler = 0
        for reihe_y in self.qr_array:
            xzähler = 0
            for zeichen_x in reihe_y:
                if zeichen_x == 255:
                    self.start_linie(xzähler,yzähler)
                    #print(self.strichliste)
                xzähler += 1
            yzähler += 1
        #self.geradeLinienZusammenfassen()
        return self.strichliste


    def start_linie(self,x,y):
        self.strichliste.append([(x,y)]) #Startkoordinaten
        self.qr_array[y][x] = 34
        while True: #Reihe nach unten
            while self.qr_array[y][x+1] == 255: #oberste Reihe
                if x+1 <= len(self.qr_array[0])-1:
                    self.strichliste[-1].append((1,0))
                    self.qr_array[y][x+1] = 34
                    x+=1
                else:
                    break
            if self.qr_array[y+1][x] == 255:
                self.strichliste[-1].append((0,1))
                self.qr_array[y+1][x] = 34
                y += 1
            else:
                break
            while self.qr_array[y][x-1] == 255: #nächste Reihe (jetzt nach links)
                if x-1 >= 0:
                    self.strichliste[-1].append((-1,0))
                    self.qr_array[y][x-1] = 34
                    x -= 1
                else:
                    break
            if self.qr_array[y+1][x] == 255:
                self.strichliste[-1].append((0,1))
                self.qr_array[y+1][x] = 34
                y += 1
            else:
                break
            
    def kurzeLinienEntfernen(self):
        for strichindex in range(len(self.strichliste)-1, -1, -1):
            if len(self.strichliste[strichindex]) <= self.min_strichlänge:
                self.strichliste.pop(strichindex)
                
    def geradeLinienZusammenfassen(self, strichliste):
        for strich in strichliste:
            neustrich=[strich[0]]
            letzte=(0,0)            #Letzter Schritt
            zähler=1                #Anzahl der bisherigen Wiederholungen
            for schritt in strich[1:]:
                if letzte == schritt:
                    zähler+=1
                else:
                    neustrich.append((zähler*letzte[0],zähler*letzte[1]))
                    letzte=schritt
                    zähler=1
            neustrich.append((zähler*letzte[0],zähler*letzte[1]))
            strichliste[strichliste.index(strich)]=neustrich
        return strichliste
    
    def diagonaleLinienZusammenfasssen(self, strichliste):
        for strichnr in range(len(strichliste)):
            strich=strichliste[strichnr]
            neustrich=[strich[0]]
            urschritt=(0,0)
            zähler=1
            jpunkt=[0,0]
            for schritt in strich[1:]:
                if abs(int((jpunkt[0])+int(schritt[0]))-int(urschritt[0]*(zähler+1)))<=(self.lückentoleranz*2) and abs(int(jpunkt[1]+schritt[1])-int(urschritt[1]*(zähler+1)))<=(self.lückentoleranz*2):
                    zähler+=1
                    jpunkt[0]+=schritt[0]
                    jpunkt[1]+=schritt[1]
                else:
                    neustrich.append((jpunkt[0],jpunkt[1]))
                    urschritt=schritt
                    zähler=1
                    jpunkt=list(urschritt)
            neustrich.append((jpunkt[0],jpunkt[1]))
            strichliste[strichnr]=neustrich
        return strichliste



    def turtle(self):
        t = turtle.Pen()
        t.shape("turtle")
        t.color("black")
        t.speed(4)
        versatz = 400
        t.pensize(3)
        #t._tracer(0)
        t.penup()
        for strich in self.strichliste:
            t.goto((strich[0][0])-versatz, (strich[0][1]*(-1))+versatz) # zur absoluten Startposition teleportieren#
            t.pendown()
            for relcord in strich[1:]:
                turtx,turty=t.pos()
                t.goto(turtx+relcord[0],turty+relcord[1]*(-1))
            t.penup()
            t.color("black")
        t.goto(1000, 1000)
        turtle.hideturtle()

def testen(doc=None,qrcode=None):
    print("moin")
    if doc != None:
        E = EigenerAlgorithmus(doc,strichlänge=20,wert=80,lückentoleranz=2)
        E.erkennen()
    else:
        print("Ja")
        E = EigenerAlgorithmus(qrcode,strichlänge=20,wert=80,lückentoleranz=2)
        E.male_qr_code()

    schritte=0
    for i in E.strichliste:
        schritte+=len(i)

    cv2.imshow("linesEdges", E.qr_array)

    print(f"Aus {len(E.strichliste)} Strichen und {schritte} Schritten werden")
    
    E.kurzeLinienEntfernen()

    print(len(E.strichliste)," Striche nach dem Aussortieren")

    schritte=0
    for i in E.strichliste:
        schritte+=len(i)
    
    print(f"Und aus {schritte} Schritten")
    
    E.geradeLinienZusammenfassen()

    schritte=0
    for i in E.strichliste:
        schritte+=len(i)

    print(f"werden {schritte} nach linearem Zusammenfassen")

    E.diagonaleLinienZusammenfasssen()

    schritte=0
    for i in E.strichliste:
        schritte+=len(i)
    
    print("werden",schritte,"nach diagonalem Zusammenfassen")

    E.turtle()

#testen()

#testen(qrcode=RobotQR.erstelle_qr_code())
#ab hier sinnlos weil turtel.done() ähnlich wie tk.mainloop()
