#Version 1.0
from tkinter import *
from tkinter.ttk import Progressbar, Style
from time import sleep


'''
ERKLÄRUNG LADEBALKEN:
Ein Objekt der Klasse Ladebalken besteht aus einem Fenster mit zwei Ladebalken sowie Beschriftung.
Es besitzt folgende Methoden:
- bar1set(max): setzt den Wert des ersten Balkens (Striche) auf 0 und das Maximum auf max.
- bar2set(max): setzt den Wert des ersten Balkens (Schritte) auf 0 und das Maximum auf max.
- bar1add(wert=1): addiert den eingegebenen Wert auf den Wert des ersten Ladebalkens.
- bar1add(wert=1): addiert den eingegebenen Wert auf den Wert des zweiten Ladebalkens.
- destroy()
- test(): lässt einmal laufen
'''
class Ladebalken:

    def __init__(self) -> None:
        self.fenster=Tk()

        self.bg = "#AAA"
        self.fenster.config(bg=self.bg)
        self.fenster.title("Fortschritt")

        self.style = Style(self.fenster)
        self.style.theme_use("default")
        self.__style = Style(self.__fenster)
        self.__style.theme_use("default")
        self.__style.configure("blue.Horizontal.TProgressbar", background='blue',troughcolor="gray",borderwidth=0)


        self.__bar1wert_VAR = IntVar(self.__fenster)
        self.__bar1max = 100
        self.__bar1text_VAR = StringVar(self.__fenster)
        self.__bar1text_VAR.set("0 von x Strichen abgeschlossen")

        self.__bar1_PGB = Progressbar(self.__fenster,length=300,variable=self.__bar1wert_VAR,style="blue.Horizontal.TProgressbar",maximum=self.__bar1max)
        self.__bar1_PGB.pack(padx=10,pady=10)

        self.__bar1_LBL = Label(self.__fenster,textvariable=self.__bar1text_VAR,bg=self.__bg)
        self.__bar1_LBL.pack(padx=10,pady=10)

        self.__bar2wert_VAR = IntVar(self.__fenster)
        self.__bar2max = 100
        self.__bar2text_VAR = StringVar(self.__fenster)
        self.__bar2text_VAR.set("0 von x Schritten des Strichs abgeschlossen")

        self.__bar2_PGB = Progressbar(self.__fenster,length=300,variable=self.__bar2wert_VAR,style="blue.Horizontal.TProgressbar",maximum=self.__bar2max)
        self.__bar2_PGB.pack(padx=10,pady=10)

        self.__bar2_LBL = Label(self.__fenster,textvariable=self.__bar2text_VAR,bg=self.__bg)
        self.__bar2_LBL.pack(padx=10,pady=10)

        #self.test()
        self.__fenster.mainloop()
    
            
    
    def bar1set(self,max=100):
        self.__bar1max = max
        self.__bar1_PGB.config(maximum=self.__bar1max,value=0)
        self.__bar1wert_VAR.set(0)
        self.__bar1text_VAR.set(f"0 von {self.__bar1max} Strichen abgeschlossen")
        self.__fenster.update()
    

    def bar1add(self,wert=1):
        self.__bar1wert_VAR.set(self.__bar1wert_VAR.get()+wert)
        self.__bar1text_VAR.set(f"{self.__bar1wert_VAR.get()} von {self.__bar1max} Strichen abgeschlossen")
        self.__fenster.update()

    def bar2set(self,max=100):
        self.__bar2max = max
        self.__bar2_PGB.config(maximum=self.__bar2max,value=0)
        self.__bar2wert_VAR.set(0)
        self.__bar2text_VAR.set(f"0 von {self.__bar2max} Schritten des Strichs abgeschlossen")
        self.__fenster.update()
    

    def bar2add(self,wert=1):
        self.__bar2wert_VAR.set(self.__bar2wert_VAR.get()+wert)
        self.__bar2text_VAR.set(f"{self.__bar2wert_VAR.get()} von {self.__bar2max} Schritten des Strichs abgeschlossen")
        self.__fenster.update()
    
    def destroy(self):
        self.__fenster.destroy()
    
    def test(self):
        self.bar1set(1000)
        for i in range(1000):
            self.bar1add()
            self.bar2set(10)
            for i in range(10):
                self.bar2add()
                sleep(0.001)
            sleep(0.001)
        self.destroy()


f=Ladebalken()
