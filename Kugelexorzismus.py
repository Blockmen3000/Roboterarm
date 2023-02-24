#Version 1.2

class Kugeldings:
    def __init__(self, ebene, boden, radius = 700 ):   #Ebene:[stützvekor,richtungsvektor1,richtungsvektor2]
        self.stützvektor = ebene[0]
        self.richtungsvektor1 = ebene[1]
        self.richtungsvektor2 = ebene[2]
        self.boden = boden
        self.radius = radius                        # Kugel = r^2 = x^2 + y^2 + z^2
        s1,s2,s3 = self.stützvektor
        r1,r2,r3 = self.richtungsvektor1
        rp,rq,rr = self.richtungsvektor2
        y = 0
        z = self.boden
        x = ((r1*rr-r3*rp)*z-(r1*rq-r2*rp)*y+r1*(rq*s3-rr*s2)-r2*(rp*s3-rr*s1)+r3*(rp*s2-rq*s1))/(r2*rr-r3*rq)
        self.ursprung = [x,y,z]                     # x = ebene,  y = 0, z = boden
        self.kugelmitte = (0,0,112)
    
    #eckenAusrechnen(verhältnis: float) --> (OL: (y,z) ,OR: (y,z) ,UL: (y,z) ,UR: (y,z))
    def eckenAusrechnen(self,verhältnis):           #Verhältnis: Breite/Höhe

        y = verhältnis/2
        z = 1
        s1,s2,s3 = self.stützvektor
        r1,r2,r3 = self.richtungsvektor1
        rp,rq,rr = self.richtungsvektor2
        x = ((r1*rr-r3*rp)*z-(r1*rq-r2*rp)*y+r1*(rq*s3-rr*s2)-r2*(rp*s3-rr*s1)+r3*(rp*s2-rq*s1))/(r2*rr-r3*rq) - self.ursprung[0]
        gx,gy,gz = x,y,z                            #g: Richtungsvektor Gerade
        sx,sy,sz = self.ursprung                    #s: Stützvektor


        stelle = -1
        t1 = 0
        while stelle <= 3:
            tt = t1 + (1/(10**stelle))

            y1 = sy + t1 * gy
            z1 = sz + t1 * gz
            x1 = ((r1*rr-r3*rp)*z1-(r1*rq-r2*rp)*y1+r1*(rq*s3-rr*s2)-r2*(rp*s3-rr*s1)+r3*(rp*s2-rq*s1))/(r2*rr-r3*rq) - self.ursprung[0]

            if (x1 - self.kugelmitte[0])**2 + (y1 - self.kugelmitte[1])**2 + (z1 - self.kugelmitte[2])**2 <= self.radius**2:
                t1 = tt
            else:
                stelle +=1
        
        t2 = 0
        stelle = -1
        while stelle <= 3:
            tt = t2 + (1/(10**stelle))

            y2 = sy + t2 * gy * (-1)
            z2 = sz + t2 * gz
            x2 = ((r1*rr-r3*rp)*z2-(r1*rq-r2*rp)*y2+r1*(rq*s3-rr*s2)-r2*(rp*s3-rr*s1)+r3*(rp*s2-rq*s1))/(r2*rr-r3*rq) - self.ursprung[0]

            if (x2 - self.kugelmitte[0])**2 + (y2 - self.kugelmitte[1])**2 + (z2-self.kugelmitte[2])**2 <= self.radius**2:
                t2 = tt
            else:
                stelle +=1
        
        if t1 < t2:
            x,y,z = x1,y1,z1
        else:
            x,y,z = x2,y2,z2
        
        return ((y,z),(-y,z),(y,self.boden),(-y,self.boden))

        





        

    

#K=Kugeldings([[100,100,0],[0,100,0],[10,0,100]],10)
#print(K.eckenAusrechnen(21/9))
#print(K.ursprung) 