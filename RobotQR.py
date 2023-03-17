import pyqrcode as qr
import cv2
import numpy as np

def erstelle_qr_code(imagesize=10,codesize=None,erocorr="H",link= "https://mypapertown.de/products/"):
    qrcode = qr.QRCode(link,error=erocorr,version=codesize) #Wenn Codesize=None, wird immer die kleinstmögliche genommen,ansonsten int(1-40)
    #qrcode.show()
    inhalt = qrcode.text()
    liste1=inhalt.split("\n")
    liste2 = []
    for reihe in range(0,len(liste1)):
        liste2.append([])
        for nummer in liste1[reihe]:
            liste2[reihe].append(int(nummer))
    liste2.pop(-1)

    #liste2=[["a","b","c","d"],[2,2,0,0],[2,2,2,2],["Öl","Haus","Lampe","Natur"],[2,2,2,1000],]
    #liste2=[[1,0,0,1],[1,0,0,1],[1,1,1,0],[1,1,1,1],[1,1,1,1]]
    #print(liste2)
    #QrCode auf Größe setzen

    #Spalten vervielfachen
    for i in liste2:
        for zahlindex in range(len(i)-1,-1,-1):
            for j in range(0,imagesize-1,1):
                i.insert(zahlindex,i[zahlindex])
    #Reihen vervielfachen
    for i in range(len(liste2)-1,-1,-1):
        for j in range(0,imagesize-1,1):
            liste2.insert(i,liste2[i])
            
    #qrcode.show()
    #1-en weiß machen
    for y in range(len(liste2)):
        for x in range(len(liste2[0])):
            if liste2[y][x] == 1:
                liste2[y][x]=255
                
                
    liste2=np.array(liste2)
    liste2 = np.uint8(liste2)

    #cv2.imshow("QRCOde", liste2)
    return liste2
    

#erstelle_qr_code(imagesize=10,codesize=None)
