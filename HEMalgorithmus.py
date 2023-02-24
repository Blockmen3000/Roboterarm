# Version 1.6 (Alpha)
import turtle
import cv2
from time import time
from numpy import zeros


class EigenerAlgorithmus:
    def __init__(self, img = "", strichlänge=30, wert=80, lückentoleranz = 2,resize=False):
        self.imgpath = img
        self.wert = wert
        self.min_strichlänge = strichlänge
        self.lückentoleranz = lückentoleranz
        self.resize = resize
        self.doppungstoleranz = 0
    
    def konvertieren(self,info):
        if self.erkennen()!=True:
            return False

        if info:
            t=time()
            print(f"{len(self.strichliste)} Striche und {self.schritte_zählen()} Schritte erkannt")

        self.kurzeLinienEntfernen()
        if info:
            print(f"noch {len(self.strichliste)} Striche und {self.schritte_zählen()} Schritte nach dem entfenen kurzer Linien")

        self.edgesanpassen()

        self.geradeLinienZusammenfassen()
        if info:
            print(f"noch {self.schritte_zählen()} Schritte nach dem geraden Zusammenfassen")
        
        self.diagonaleLinienZusammenfasssen()
        if info:
            print(f"noch {self.schritte_zählen()} Schritte nach dem diagonalen Zusammenfassen")
            print(f"gesammte Rechendauer: {time()-t} Sekunden")
        
        #self.turtle()
        

        
        
        return True

    def edgesanpassen(self):
        self.edges = zeros([len(self.edges), len(self.edges[0])]) # Edges komplett entleeren
        for strich in self.strichliste:
            x=strich[0][0]
            y=strich[0][1]
            self.edges[y][x] = 255
            for schritt in strich[1:]:
                x+=schritt[0]
                y+=schritt[1]
                self.edges[y][x] = 255


    
    def schritte_zählen(self):
        schritte=0
        for i in self.strichliste:
            schritte+=len(i)
        return schritte
    
    def erkennen(self):
        self.img = cv2.imread(self.imgpath)
        if format(self.img) == "None":
            #raise TypeError("Nicht lesbare Datei")
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

    def kurzeLinienEntfernen(self):
        for strichindex in range(len(self.strichliste)-1, -1, -1):
            if len(self.strichliste[strichindex]) <= self.min_strichlänge:
                self.strichliste.pop(strichindex)
                
    def geradeLinienZusammenfassen(self):
        for strich in self.strichliste:
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
            self.strichliste[self.strichliste.index(strich)]=neustrich
    
    def diagonaleLinienZusammenfasssen(self):
        for strichnr in range(len(self.strichliste)):
            strich=self.strichliste[strichnr]
            neustrich=[strich[0]]
            urschritt=(0,0)
            zähler=1
            jpunkt=[0,0]
            for schritt in strich[1:]:
                if abs(int((jpunkt[0])+int(schritt[0]))-int(urschritt[0]*(zähler+1)))<=self.lückentoleranz and abs(int(jpunkt[1]+schritt[1])-int(urschritt[1]*(zähler+1)))<=self.lückentoleranz:
                    zähler+=1
                    jpunkt[0]+=schritt[0]
                    jpunkt[1]+=schritt[1]
                else:
                    neustrich.append((jpunkt[0],jpunkt[1]))
                    urschritt=schritt
                    zähler=1
                    jpunkt=list(urschritt)
            neustrich.append((jpunkt[0],jpunkt[1]))
            self.strichliste[strichnr]=neustrich



    def turtle(self):
        t = turtle.Pen()
        t.shape("turtle")
        t.color("black")
        t.speed(0.1)
        versatz = 400
        t.pensize(3)
        t._tracer(0)
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

def testen(doc="Manhattan.jpeg"):
    print("moin")
    E = EigenerAlgorithmus(doc,strichlänge=20,wert=80,lückentoleranz=2)

    E.erkennen()

    schritte=0
    for i in E.strichliste:
        schritte+=len(i)

    cv2.imshow("linesEdges", E.edges)

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


#testen("Manhattan.jpeg")
#ab hier sinnlos weil turtel.done() ähnlich wie tk.mainloop()
