#!/usr/bin/env python3
#eine einheit entspricht 1mm
#Standartkoordinaten: 207, 0.0, 112

#Bei unverständlichen Errors -> kurze Sleep-Time dazwischen setzen, weil wait=True nicht immer richtig funktioniert

# Input: strichliste = [strich1, strich2, strich3, strich4, ...]
#        strich = [(absoultx, absoluty), (rel_x, rel_y), (rel_x, rel_y), (rel_x, rel_y), ...]

from xarm.wrapper import XArmAPI
import os
import sys
import time
import math
#import HEMalgorithmus as HEM
import Ladebalken as load

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

class Roboter:
    def __init__(self):           
        self.arm = XArmAPI('192.168.1.223')
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(state=0)

        self.load = load.Ladebalken()

        self.schreibEbene = 300
        self.absetzEbene = self.schreibEbene - 50

        self.verhältnis = 1 # Das Verhätnis, womit man Pixel in mm umwandelt. Also: PIXEL * VERHÄLTNIS = MM
        # ((x_max,y_max), (x_min,y_min)) - Gibt Punkte an, die die Größe und Position des Bilds festlegen

        self.größe = ((270, 650), (-270, 280)) #(links_x, oben_y),(rechts_x, unten_y)

        try:
            textdatei = open("Kalibrierung.txt","r")
            print("Kalibrierungsdaten gefunden")
        except:
            textdatei = None
            print("keine Kalibrierungsdaten gefunden")
                
        if textdatei != None:
            liste = textdatei.readlines()
            for i in range(len(liste)):
                liste[i] = float(liste[i][:-1])
            self.kalibrierungspunkte = [liste[:3], liste[3:6], liste[6:9], liste[9:]]
        else:
            self.kalibrierungspunkte = [] # [OL, UL, OR, UR]
            self.kalibrierungspunkte.append([self.absetzEbene, self.größe[0][1], self.größe[0][0]]) #OL
            self.kalibrierungspunkte.append([self.absetzEbene, self.größe[1][1], self.größe[0][0]]) #UL
            self.kalibrierungspunkte.append([self.absetzEbene, self.größe[0][1], self.größe[1][0]]) #OR
            self.kalibrierungspunkte.append([self.absetzEbene, self.größe[1][1], self.größe[1][0]]) #UR
        print("\nKalibrierungspunkte:",self.kalibrierungspunkte,"\n")

        self.reset()

    def setVerhältnis(self, bildgröße): # Größe des zu malenden Bildes als Tupel: (x, y)
        bildbreite = bildgröße[0]
        bildhöhe = bildgröße[1]
        bildverhältnis1 = (bildbreite) / (bildhöhe)
        bildverhältnis2 = (bildhöhe) / (bildbreite)

        
        
        #Beide Möglichkeiten durchgehen, erst Bild an malbreite anpassen, dann an malhöhe und gucken was besser ist
        malbreite = self.größe[0][0] - self.größe[1][0] #in mm
        malhöhe = self.größe[0][1] - self.größe[1][1] #in mm
        x = int(malbreite)
        y = int(malbreite * bildverhältnis2)
        if x > malhöhe:
            y=0
        tupel1 = (x,y)
        
        x = int(malhöhe * bildverhältnis1)
        y = int(malhöhe)
        if y > malbreite:
            x=0
        tupel2 = (x,y)

        if (tupel1[0] * tupel1[1]) > (tupel2[0] * tupel2[1]): # besseres Format mithilfe vom Flächeninhalt herausfinden
            self.verhältnis = tupel1[0] / bildgröße[0]
        else:
            self.verhältnis = tupel2[0] / bildgröße[0] # bestimmt Verhältnis mithilfe von (zu malender Bildgröße) / (Input-Bildgröße)


    def bildZeichnen(self, strichliste, bildgröße):
        self.reset()
        self.setVerhältnis(bildgröße)

        position = self.arm.get_position()[1] # geht auf kleinste Höhe
        self.arm.set_position(position[0], position[1], self.größe[1][1], wait = True, velo = 1)
        time.sleep(0.00001)
        
        #self.stift_absetzen() # auf richtige Ebene ungefähr bewegen

        
        self.load.fenster_erstellen()
        self.load.bar1set(len(strichliste)) # Ladebalken Anzahl Striche festlegen
        for strich in strichliste:
            self.load.bar2set(len(strich))  # Ladebalken Anzahl Schritte festlegen
            if self.strichZeichnen(strich) == False:
                break
            self.load.bar1add()             # Ladebalken Strich fertiggestellt
        self.stift_absetzen()
        self.reset(True)
        self.load.destroy()                 # Ladebalken wird VERNICHTET!!!

    def strichZeichnen(self, strich):
        start = strich[0]
        ebene_x = (self.größe[0][0] - (start[0] * self.verhältnis))
        ebene_y = abs(self.größe[0][1] - (start[1] * self.verhältnis)) #Maximale y-Koordinate minus y-Koordinate des Striches

        self.abs_koord = [ebene_x, ebene_y]
        
        #UPDATE FÜR KALIBRIERUNG
        self.updateEbenen(self.abs_koord[0], self.abs_koord[1])
        
        self.arm.set_position(self.absetzEbene, ebene_x , ebene_y , wait = True) #Gehe zur Startposition
        self.stift_aufsetzen()

        self.load.bar2add()             # Ladebalken erster Schritt fertiggestellt

        for i in range(len(strich)-1):
            if self.load.läuftnoch() == True:
                self.relativeKoordinateZeichnen(strich[i+1])
                self.load.bar2add()             # Ladebalken nächster Schritt fertiggestellt
            else:
                return False# Returnt False, wenn abgebrochen werden soll

        self.stift_absetzen()

    def relativeKoordinateZeichnen(self, tupel):
        ebene_x = tupel[0] * self.verhältnis
        ebene_y = tupel[1] * self.verhältnis

        self.abs_koord[0] -= ebene_x
        self.abs_koord[1] -= ebene_y

        #UPDATE FÜR KALIBRIERUNG
        self.updateEbenen(self.abs_koord[0], self.abs_koord[1])
        
        self.arm.set_position(self.schreibEbene, self.abs_koord[0], self.abs_koord[1], wait = True, velo = 1)
        
        
    def stift_absetzen(self):
        position = self.arm.get_position()[1]
        print("\nABSETZEN:\nGehe von", position[0], "zu", self.absetzEbene)
        
        #UPDATE FÜR KALIBRIERUNG
        self.updateEbenen(position[1], position[2])
        position[0] = self.absetzEbene
        
        self.arm.set_position(position[0], position[1], position[2], wait = True)
        time.sleep(0.00001)

    def stift_aufsetzen(self):
        position = self.arm.get_position()[1]
        print("\nAUFSETZEN:\nGehe von", position[0], "zu", self.schreibEbene)
        
        #UPDATE FÜR KALIBRIERUNG
        self.updateEbenen(position[1], position[2])
        position[0] = self.schreibEbene
        
        self.arm.set_position(position[0], position[1], position[2], wait = True)
        time.sleep(0.00001)

    def updateEbenen(self, y, z):
        stützvektor = (self.kalibrierungspunkte[0])
        richtungsvektor1 = [None,None,None]
        richtungsvektor2 = [None,None,None]
        for i in range(0,3):
            richtungsvektor1[i] = self.kalibrierungspunkte[1][i] - stützvektor[i]
        for i in range(0,3):
            richtungsvektor2[i] = self.kalibrierungspunkte[2][i] - stützvektor[i]
    
        #Punkt auf Ebene berechnen
        s1,s2,s3 = stützvektor[0],stützvektor[1],stützvektor[2]
        r1,r2,r3 = richtungsvektor1
        rp,rq,rr = richtungsvektor2
        x = ((r1*rr-r3*rp)*y-(r1*rq-r2*rp)*z+r1*(rq*s3-rr*s2)-r2*(rp*s3-rr*s1)+r3*(rp*s2-rq*s1))/(r2*rr-r3*rq) #Das funktioniert, wenn es einen Fehler gibt, liegt das nicht an dieser Zeile
        #punkt_auf_ebene = stützvektor + r * richtungsvektor1 + s * richtungsvektor2

        self.schreibEbene = x
        self.absetzEbene = self.schreibEbene - 50

        print(f"UPDATE DER EBENEN: \nSchreibebene:{self.schreibEbene}\nAbsetzebene: {self.absetzEbene}\nY: {y}\nZ: {z}")

    def EbenenALT(self, z, y):
        bildbreite = self.größe[0][0] - self.größe[1][0] #in mm
        bildhöhe = self.größe[0][1] - self.größe[1][1] #in mm

        anteil_z = z / bildbreite # Anteil an der Bildbreite
        anteil_y = y / bildhöhe # Anteil an der Bildhöhe


        differenz_kz = (((self.kalibrierungspunkte[0] - self.kalibrierungspunkte[2])+(self.kalibrierungspunkte[1] - self.kalibrierungspunkte[3]))/2) #berechnet den Durchschnitt von der Verschiebung auf der z-Achse
        differenz_ky = (((self.kalibrierungspunkte[0] - self.kalibrierungspunkte[1])+(self.kalibrierungspunkte[2] - self.kalibrierungspunkte[3]))/2) #berechnet den Durchschnitt von der Verschiebung auf der y-Achse
        # self.kalibrierungspunkte = [OL, UL, OR, UR]


        verschiebung_z = anteil_z * differenz_kz # Verschiebung nach z-Berechnung
        verschiebung_y = anteil_y * differenz_ky # Verschiebung nach y-Berechnung

        verschiebung = verschiebung_z + verschiebung_y
        
        self.schreibEbene = verschiebung
        self.absetzEbene = self.schreibEbene - 50


    def gehezuEcke(self, ecke):
        position = self.arm.get_position()[1] #Startkoordinaten: 207, 0.0, 112
        position[0] = 207
        self.arm.set_position(position[0], position[1], position[2], wait = True)
        # ecke ist ein String mit "OL" für oben links und "UR" für unten rechts
        if ecke.__contains__("U") == True:
            y = self.größe[1][1]
        elif ecke.__contains__("O") == True:
            y = self.größe[0][1]
        else:
            return "Error"

        if ecke.__contains__("L") == True:
            z = self.größe[0][0]
        elif ecke.__contains__("R") == True:
            z = self.größe[1][0]
        else:
            return "Error"

        self.arm.set_position(position[0], z, y, wait = True)
        time.sleep(0.00001)
        
    def vierPunkteKalibrierung(self, ecke): # Liest aktuelle x-Werte aus und speichert sie in self.kalibrierungspunkte
        verschiebung = (self.arm.get_position()[1][0],self.arm.get_position()[1][1],self.arm.get_position()[1][2])

        if ecke == "OL":
            self.kalibrierungspunkte[0] = verschiebung
        elif ecke == "UL":
            self.kalibrierungspunkte[1] = verschiebung
        elif ecke == "OR":
            self.kalibrierungspunkte[2] = verschiebung
        elif ecke == "UR":
            self.kalibrierungspunkte[3] = verschiebung
        else:
            return "Error"

        if verschiebung[0] < self.absetzEbene + 20:
            self.absetzEbene = round(verschiebung[0] - 20)
            #Abesetzebene zur Sicherheit falls notwendig hinter den hintersten Kalibrierungspunkt legen
            
    def saveKalibrierungspunkte(self):
        print("SAVED",self.kalibrierungspunkte,"\n")
        textdatei = open("Kalibrierung.txt","w")
        for i in self.kalibrierungspunkte:
            for y in i:
                textdatei.write(str(y)+"\n")
        textdatei.close()

    def kalibrierung(self, wert = 1):
        position = self.arm.get_position()[1]
        #if position[0] + wert > 207:
        position[0] += wert
        #else:
        #    print("ERROR E$(§)") # geht hinter seine Startpostion -> soll nicht
        self.arm.set_position(position[0], position[1], position[2], wait = True)
        time.sleep(0.00001)



    def reset(self, fullreset = False):
        if fullreset == True:
            position = self.arm.get_position()[1] #Startkoordinaten: 207, 0.0, 112
            position[0] = 207
            position[1] = 0
            self.arm.set_position(position[0], position[1], position[2], wait = True)
            position[2] = 112
            self.arm.set_position(position[0], position[1], position[2], wait = True)
            time.sleep(0.5)

        self.arm.reset(wait=True)
        time.sleep(0.5)
