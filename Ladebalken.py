from tkinter import *
from tkinter.ttk import Progressbar, Style
import time

class Ladebalken:

    def __init__(self) -> None:
        self.fenster=Tk()

        self.bg = "#AAA"
        self.fenster.config(bg=self.bg)
        self.fenster.title("Fortschritt")
        self.fenster.resizable(False,False)

        self.style = Style(self.fenster)
        self.style.theme_use("default")
        self.style.configure("blue.Horizontal.TProgressbar", background='blue',troughcolor="gray",borderwidth=0)


        self.bar1wert_VAR = IntVar(self.fenster)
        self.bar1max = 100
        self.bar1text_VAR = StringVar(self.fenster)
        self.bar1text_VAR.set("0 von x Strichen abgeschlossen")

        self.bar1_PGB = Progressbar(self.fenster,length=300,variable=self.bar1wert_VAR,style="blue.Horizontal.TProgressbar",maximum=self.bar1max)
        self.bar1_PGB.pack(padx=10,pady=10)

        self.bar1_LBL = Label(self.fenster,textvariable=self.bar1text_VAR,bg=self.bg)
        self.bar1_LBL.pack(padx=10,pady=10)

        self.bar2wert_VAR = IntVar(self.fenster)
        self.bar2max = 100
        self.bar2text_VAR = StringVar(self.fenster)
        self.bar2text_VAR.set("0 von x Schritten abgeschlossen")

        self.bar2_PGB = Progressbar(self.fenster,length=300,variable=self.bar2wert_VAR,style="blue.Horizontal.TProgressbar",maximum=self.bar2max)
        self.bar2_PGB.pack(padx=10,pady=10)

        self.bar2_LBL = Label(self.fenster,textvariable=self.bar2text_VAR,bg=self.bg)
        self.bar2_LBL.pack(padx=10,pady=10)

        self.fenster.mainloop()
    
            
    
    def bar1set(self,max=100):
        self.bar1max = max
        self.bar1_PGB.config(maximum=self.bar1max,value=0)
        self.bar1wert_VAR.set(0)
        self.bar1text_VAR.set(f"0 von {self.bar1max} Strichen abgeschlossen")
        self.fenster.update()
    

    def bar1add(self,wert=1):
        self.bar1wert_VAR.set(self.bar1wert_VAR.get()+wert)
        self.bar1text_VAR.set(f"{self.bar1wert_VAR.get()} von {self.bar1max} Strichen abgeschlossen")

    def bar2set(self,max=100):
        self.bar2max = max
        self.bar2_PGB.config(maximum=self.bar2max,value=0)
        self.bar2wert_VAR.set(0)
        self.bar2text_VAR.set(f"0 von {self.bar2max} Schritten abgeschlossen")
        self.fenster.update()
    

    def bar2add(self,wert=1):
        self.bar2wert_VAR.set(self.bar2wert_VAR.get()+wert)
        self.bar2text_VAR.set(f"{self.bar2wert_VAR.get()} von {self.bar2max} Schritten abgeschlossen")
    
    def destroy(self):
        self.fenster.destroy()

#f=Ladebalken()
