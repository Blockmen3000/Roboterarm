import numpy as np
from tkinter import *
from tkinter import filedialog as fd
from PIL import Image as im
from PIL import ImageTk
import HEMalgorithmus as HEM

class Benutzeroberfläche:
    def __init__(self):
        self.algorithmus = HEM.EigenerAlgorithmus()
        
        self.fenster=Tk()
        self.fenster.title("Netflix")
        #self.fenster.geometry("1440x900+2000+50")

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

        #Scales
        self.größe_SCL = Scale(self.fenster, from_=100, to=0, orient=VERTICAL, bg=self.fensterfarbe, relief=FLAT, length=720, border = 0)
        self.größe_SCL.place(x=40, y=48)
        self.größe_SCL.set(100)

        self.toleranz_SCL = Scale(self.fenster, from_=0, to=255, orient=HORIZONTAL, bg=self.fensterfarbe, relief=FLAT, length=720, border = 0)
        self.toleranz_SCL.place(x=115, y=790)
        self.toleranz_SCL.set(80)

       
        self.fenster.mainloop()

    def webcam(self):
        pass

    def bildÖffnen(self):
        filepath = fd.askopenfilename()
        self.algorithmus.imgpath = filepath
        if self.algorithmus.erkennen() == True:
            self.bildPlazieren()

    def toleranzAnpassen(self):
        self.algorithmus.wert = self.toleranz_SCL.get()
        if self.algorithmus.erkennen() == True:
            self.bildPlazieren()

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
            return tupel1
        else:
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


B = Benutzeroberfläche()
