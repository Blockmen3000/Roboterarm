import cv2
import turtle

class EigenerAlgorithmus:
    def __init__(self, img = "", strichlänge=30, wert=80, lückentoleranz = 2):
        self.imgpath = img
        self.wert = wert
        self.min_strichlänge = strichlänge
        self.lückentoleranz = lückentoleranz
    
    
    def erkennen(self):
        self.img = cv2.imread(self.imgpath)
        if format(self.img) == "None":
            print("Error")
            return False
        faktor = 720 / self.img.shape[1]
        self.img = cv2.resize(self.img, (int(self.img.shape[1] * faktor), int(self.img.shape[0] * faktor)), interpolation= cv2.INTER_LINEAR)
        
        #img = cv2.imread("Permission denied..png")
        self.img = cv2.convertScaleAbs(self.img, alpha=1.3, beta=40)
        
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.edges = cv2.Canny(gray, self.wert, 200)

        
        self.auflösung = (len(self.edges[0]), len(self.edges)) #(x,y)
        self.strichliste = []
        for x in range(0, len(self.edges[0])): # alle Pixel durchgehen
            for y in range(0, len(self.edges)):
                if self.edges[y][x] == 255:
                    self.edges[y][x] = 40

                    # Roboter bekommt Liste: strich = [(x,y), (relativx, relativy), (relativx, relativy), ...]
                    
                    strich = [(x,y)] #Liste mit absoluten Startkooredinaten erstellt
                    x_rel = 0
                    y_rel = 0
                    while self.umliegendeErkennen(x + x_rel, y + y_rel) != False:
                        #print("rel",x_rel, y_rel)
                        tupel = self.umliegendeErkennen(x + x_rel, y + y_rel)
                        x_rel += tupel[0]
                        y_rel += tupel[1]
                        self.edges[y + y_rel][x + x_rel] = 40
                        strich.append(tupel) # Einfügen von relativen Koordinaten
                        #print("Strich",strich)
                        
                    self.strichliste.append(strich)
        #cv2.imshow("linesEdges", self.edges)
        return True

    def umliegendeErkennen(self, x, y):
        for i in range (0, self.lückentoleranz+1):
            for x_rel in range(i, -1-i, -1):
                for y_rel in range(i, -1-i, -1): # nahe umliegende Pixel durchgehen (Abstand i)
                    try:
                        if self.edges[y + y_rel][x + x_rel] == 255:
                            return (x_rel, y_rel)
                    except IndexError: #Bildrand
                        pass
        # umliegende Pixel sind nicht weiß --> False zurückgeben
        return False

    def kurzeLinienEntfernen(self):
        for strichindex in range(len(self.strichliste)-1, -1, -1):
            if len(self.strichliste[strichindex]) <= self.min_strichlänge:
                self.strichliste.pop(strichindex)
        print("Und nach dem Löschen von zu kurzen Linien, da warens nur noch "+str(len(self.strichliste)))
                
    def linien_zusammenfügen(self):
        #startundendpunktliste=[[strichindex,punktx,punkty,startpunkt?-->Bool]]  --->      Liste aller Start und Endpunkte, immer abwechselnd erst Startpunkt der Liste, dann Endpunkt der Liste
        besondere_punktliste=[]
        for strich in self.strichliste:
            #Startpunkte hinzufügen
            besondere_punktliste.append([self.strichliste.index(strich),strich[0][0],strich[0][1],True])
            #Endpunkte berechnen
            endpunktx=strich[0][0]
            endpunkty=strich[0][1]
            for schritt in strich[1:]:
                endpunktx+=schritt[0]
                endpunkty+=schritt[1]
            #Endpunkte hinzufügen
            besondere_punktliste.append([self.strichliste.index(strich),endpunktx,endpunkty,False])

        #Punkte vergleichen
        for koordinate in besondere_punktliste:
            if koordinate != None:
                kx=koordinate[1]
                ky=koordinate[2]
                for punkt in besondere_punktliste:
                    if punkt!=None:
                        px=punkt[1]
                        py=punkt[2]
                        #Überprüfen, ob es sich nicht um den gleichen Punkt handelt
                        if koordinate[0] != punkt[0]:
                            
                            if abs(px-kx) < 2 and abs(py-ky) < 2:

                                if koordinate[3] == False and punkt[3] == True:                         #Endpunkt mit Startpunkt verknüpfen
                                    self.strichliste[koordinate[0]].append((px-kx,py-ky))               #Differenz zwischen End- und Startpunkt berechnen
                                    self.strichliste[koordinate[0]] += self.strichliste[punkt[0]][1:]   #Listen zusammenühren
                                    besondere_punktliste[besondere_punktliste.index(punkt)+1][0] = koordinate[0]                            #Strichindex des Endpunkts der Startpunktlinie auf den der Endpunktlinie setzen
                                    besondere_punktliste[besondere_punktliste.index(koordinate)] = besondere_punktliste[besondere_punktliste.index(punkt)+1] 
                                    besondere_punktliste[besondere_punktliste.index(punkt)+1] = None                                        #Entfallene Objekte entfernen
                                    besondere_punktliste[besondere_punktliste.index(punkt)] = None
                                    self.strichliste[punkt[0]] = None
                                    
                                
                                   
                                elif koordinate[3] == True and punkt[3] == False:                       #Endpunkt mit Startpunkt verknüpfen
                                    self.strichliste[punkt[0]].append((kx-px,ky-py))                    #Differenz zwischen End- und Startpunkt berechnen
                                    self.strichliste[punkt[0]] += self.strichliste[koordinate[0]][1:]   #Listen zusammenühren
                                    besondere_punktliste[besondere_punktliste.index(koordinate)+1][0] = punkt[0]                            #Strichindex des Startpunkts der Endpunktlinie auf den der Startpunktlinie setzen
                                    besondere_punktliste[besondere_punktliste.index(punkt)]=besondere_punktliste[besondere_punktliste.index(koordinate)+1]
                                    besondere_punktliste[besondere_punktliste.index(koordinate)+1] = None                                   #Entfallene Objekte entfernen
                                    besondere_punktliste[besondere_punktliste.index(koordinate)] = None
                                    self.strichliste[koordinate[0]] = None
                                    
                                

                                elif koordinate[3] == False and punkt[3] == False:                      #Endpunkt mit Endpunkt verknüpfen
                                    self.strichliste[koordinate[0]].append((px-kx,py-ky))               #Differenz zwischen End- und Endpunkt berechnen
                                    for s in range(len(self.strichliste[punkt[0]])-1,0,-1):             #Liste rückwärts durchgehen
                                        schritt = self.strichliste[punkt[0]][s]
                                        sx = schritt[0]
                                        sy = schritt[1]
                                        self.strichliste[koordinate[0]].append(((-1)*sx,(-1)*sy))       #Koordinaten umkehren und zur Liste hinzufügen
                                    besondere_punktliste[besondere_punktliste.index(punkt)-1][0] = koordinate[0]                            # Strichindex der einen Endpunktlinie auf den der anderen Endpunktlinie setzen
                                    besondere_punktliste[besondere_punktliste.index(punkt)-1][3] = False
                                    besondere_punktliste[besondere_punktliste.index(koordinate)] = besondere_punktliste[besondere_punktliste.index(punkt)-1]
                                    besondere_punktliste[besondere_punktliste.index(punkt)+1] = None
                                    besondere_punktliste[besondere_punktliste.index(punkt)] = None
                                    self.strichliste[punkt[0]] = None
                                    

                                elif koordinate[3] == True and punkt[3] == True:                        #Startpunkt mit Startpunkt verknüpfen
                                    #Liste für Pfeil der Startkoordinate Koordinate gefüllt mit Absoluter Startkoordinate des neuen verknüpften Pfeils
                                    newkoordinate = [(besondere_punktliste[besondere_punktliste.index(koordinate)+1][1], besondere_punktliste[besondere_punktliste.index(koordinate)+1][2])]
                                    for s in range(len(self.strichliste[koordinate[0]])-1,0,-1):
                                        schritt = self.strichliste[koordinate[0]][s]
                                        sx = schritt[0]
                                        sy = schritt[1]
                                        newkoordinate.append((sx*(-1),sy*(-1)))
                                    self.strichliste[koordinate[0]] = newkoordinate
                                    self.strichliste[koordinate[0]].append((px-kx,py-ky))               #Differenz zwischen End- und Startpunkt berechnen
                                    self.strichliste[koordinate[0]] += self.strichliste[punkt[0]][1:]   #Listen zusammenühren
                                    koordinate = besondere_punktliste[besondere_punktliste.index(koordinate)+1]
                                    besondere_punktliste[besondere_punktliste.index(koordinate)-1] = besondere_punktliste[besondere_punktliste.index(koordinate)]               #alter Endpunkt von Koordinater wird neuer Startpunkt
                                    besondere_punktliste[besondere_punktliste.index(punkt)+1][0] = koordinate[0]
                                    besondere_punktliste[besondere_punktliste.index(koordinate)+1] = besondere_punktliste[besondere_punktliste.index(punkt)+1]                  #alter Endpunkt von Punkt wird Endpunkt von Koordinate
                                    besondere_punktliste[besondere_punktliste.index(punkt)+1] = None                                        #Entfallene Objekte entfernen
                                    besondere_punktliste[besondere_punktliste.index(punkt)] = None 
                                    self.strichliste[punkt[0]] = None
                                    

                                else:
                                    print("Diese Meldung ist unmöglich. Du Magier. Oder Hacker!")                      
        for i in range(len(self.strichliste)-1, 0, -1):
            if self.strichliste[i] == None:
                self.strichliste.pop(i)

        print(len(self.strichliste),"Linien durch zusammenfügen!")


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
            for relcord in strich:
                if relcord != strich[0]:
                    turtx,turty=t.pos()
                    t.goto(turtx+relcord[0],turty+relcord[1]*(-1))
            t.penup()
            t.color("black")
        t.goto(1000, 1000)
        turtle.done()

#E = EigenerAlgorithmus("schildkrote-charakter-cartoon-illustration-fyj0g3.jpg")
#E = EigenerAlgorithmus("Schulimpressionen.jpg",strichlänge=40,wert=20)
#cv2.imshow("linesEdges", E.edges)
#E.erkennen()
#print("Aus",len(E.strichliste),"werden")
#E.linien_zusammenfügen()
#E.kurzeLinienEntfernen()
#E.turtle()
#ab hier sinnlos weil turtel.done() ähnlich wie tk.mainloop()
