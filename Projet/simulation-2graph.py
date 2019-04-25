import math as m
import numpy as np
import matplotlib.pyplot as plt



'''constante :  m = masse
                g = 9.81
                k = elsticité
                mu = coéfficient de friction
                N = normale 

E_tot = mv^2/2 + mgh + kx^2/2 + Iw^2/2
E_tot(d) = mv^2/2(d) + mgh(d) + kx^2/2 + Iw^2/2(d) - mu*cos(alpha)*mg*d'''


"Ces 3 valeurs peuvent etre changées au dernier moment"
"longueur du saut"
L= 0.3
"hauteur de la bosse"
hbosse= 0.1
"hauteur de la pente ajoutée"
hpente= 0.8
lpente= 0.88
"Angle du tremplin 10<ALPHA<20"
alphatremplin=15
"Energie supp au debut"
energie_supp= 15


"Ce sont les longueurs qui ne peuvent pas etre modifiées le jour du jury"
hpiste=0.02

d1=lpente
d2=0.744 
d3=0.600
d4=0.300



diago_de_tremplin= 0.305
htremplin= m.sin( np.deg2rad(alphatremplin) ) * diago_de_tremplin
d5= m.cos( np.deg2rad(alphatremplin) ) * diago_de_tremplin

print(d5,htremplin)


"Variables pour énergies"
masse = 0.8
mu=0.03
k=0                                   # k de l'élastique
dressort=0
kdefrot=0.3
couple= (0.8)**(1/2)        
mvol=0.2
Rroue=0.5
Rvol=1
rapport= couple**2 * (mvol*Rvol)  / (masse*Rroue)        # rapport entre energie volant d'inertie et cinétiue de translation ( rapport * Ec = Evol)


step = 0.02  # pas de simulation [m]
end = d1+d2+d3+d4+d5 + step

x = np.arange(0, end, step)           # distance parcourue [m]
l = np.zeros(len(x))                  # position x [m]
y = np.zeros(len(x))
y[0]= hpente + hpiste
l[0]=0
x[0]=0



f = np.zeros(len(x))
p = np.zeros(len(x))
ctot = np.zeros(len(x))
c = np.zeros(len(x))
evol = np.zeros(len(x)) 
elas = np.zeros(len(x))
E = np.zeros(len(x))
vx = np.zeros(len(x))
vy = np.zeros(len(x))

f[0]=0
p[0]=masse*9.81* (hpente + hpiste)
ctot[0]=0
c[0]=0
evol[0]=0
elas[0]=0
E[0]= p[0] + energie_supp



def pente1(x,y,l,lpente,hpente,hpiste):
    y[i] = -(hpente/lpente)*x[i] + hpente + hpiste
    l[i] = l[i-1] + m.sqrt((x[i]-x[i-1])**2+(y[i]-y[i-1])**2)
    return (y[i],l[i])

def plat(y,l,i,step,hpiste):
    y[i] = hpiste
    l[i] = l[i-1] + step
    return (y[i],l[i])
    
def bosse(x,y,l,i,debut,lbosse,hbosse,hpiste,step):
    y[i] = (hbosse/2) * (m.cos( (2*m.pi* (x[i] -debut+lbosse/2) ) /d3) + 1 ) + hpiste
    l[i] = l[i-1] + m.sqrt((x[i]-x[i-1])**2+(y[i]-y[i-1])**2)
    return (y[i],l[i])

def tremplin(x,y,l,i,debut,ltremplin,htremplin):
    y[i]= (htremplin/ltremplin)*(x[i]-debut) + hpiste
    l[i] = l[i-1] + m.sqrt((x[i]-x[i-1])**2+(y[i]-y[i-1])**2)
    return (y[i],l[i])


for i in range(len(x)):
    if 0 < x[i] < d1:
        y[i] = pente1(x,y,l,d1,hpente,hpiste)[0]
        l[i] = pente1(x,y,l,d1,hpente,hpiste)[1]
    elif d1 <= x[i] < d1+d2:
        y[i] = plat(y,l,i,step,hpiste)[0]
        l[i] = plat(y,l,i,step,hpiste)[1]
    elif d1+d2 <= x[i] < d1+d2+d3:
        debut= d1+d2
        y[i]= bosse(x,y,l,i,debut,d3,hbosse,hpiste,step)[0]
        l[i]= bosse(x,y,l,i,debut,d3,hbosse,hpiste,step)[1]  
    elif d1+d2+d3 <= x[i] < d1+d2+d3+d4:
        y[i] = plat(y,l,i,step,hpiste)[0]
        l[i] = plat(y,l,i,step,hpiste)[1]
    elif d1+d2+d3+d4 <= x[i] <= d1+d2+d3+d4+d5+step:
        debut= d4+d3+d2+d1
        y[i] = tremplin(x,y,l,i,debut,d5,htremplin)[0]
        l[i] = tremplin(x,y,l,i,debut,d5,htremplin)[1] 



print("x= ", x[101],"\ny= ", y[101],"\nl= ", l[101]) 




"""
LES ENERGIES
"""



def alpha(x,y,i):
    return m.atan( (y[i]-y[i-1]) / (x[i]-x[i-1]) )
    
def fric(f,x,y,l,i,mu,masse):
    f[i]= mu * m.cos(alpha(x,y,i))*masse*9.81 * (l[i])
    return f[i]

def pot(p,y,i,masse):
    p[i]= masse*9.81*y[i]
    return p[i]

def elast(elas,x,y,l,i,k,dressort):
    elas[i] = k* (dressort**2)/2
    return elas[i]

def potint(petitpoids,h):
    potint= petitpoids*h*9.81
    return potint

def cintot(ctot,x,y,l,i):
    ctot[i] = E[i-1] - (p[i] + elas[i])
    return ctot[i]

def cin(c,ctot,x,y,l,i,rapport):
    if x[i] < d1+d2+d3+d4+d5:
        c[i]= ctot[i] / (1 + rapport)                        
    else:
        c[i]= ( vx[i]**2 + vy[i]**2 ) *masse/2
    return c[i]

def vol(evol,x,y,l,i,rapport):    
    evol[i]= c[i] * rapport                 
    return evol[i]

def etot(E,x,y,l,f,p,c,elas,evol):
    if x[i] < d1+d2+d3+d4+d5:
        E[i]= p[i] + ctot[i] + elas[i] - (f[i]-f[i-1])
    else:
        E[i]= p[i] + c[i] - frotx[i]+ froty[i]
    return E[i]

def long(x,y,l,i):
    l[i]= m.sqrt( (x[i]-x[i-1])**2 + (y[i]-y[i-1])**2 )
    return l[i]

def vitx(angle,i,c):
    v= (c[i]*2/masse)**(1/2)
    vx[i]= ( m.cos(angle) * v )
    return vx[i]

def vity(angle,i,c):
    v= (c[i]*2/masse)**(1/2)
    vy[i]= ( m.sin(angle) * v )
    return vy[i]


for i in range(len(x)):
    if 0 < x[i] < d1+d2+d3+d4+d5:
        f[i]= fric(f,x,y,l,i,mu,masse)
        p[i]= pot(p,y,i,masse)
        elas[i]= elast(elas,x,y,l,i,k,dressort)            # Circuit
        ctot[i]= cintot(ctot,x,y,l,i)
        c[i]= cin(c,ctot,x,y,l,i,rapport)
        evol[i]= vol(evol,x,y,l,i,rapport)
        E[i]= etot(E,x,y,l,f,p,c,elas,evol)
        vx[i]= vitx(alpha(x,y,i),i,c)
        vy[i]= vity(alpha(x,y,i),i,c)


"""
LE SAUT
"""


vx0=vx[-2]
vy0=vy[-2]
y0= htremplin
x0= 0


step= 0.001
max= 0.5
tsaut = np.arange(0, max, step)           
xsaut = np.zeros(len(tsaut))             
ysaut = np.zeros(len(tsaut))
ysaut[0]= y0
tsaut[0]= 0
xsaut[0]= 0
#print("\nvx0=",vx0,"vy0=",vy0,"x0=",x0,"y0=",y0)

def saut(i):
    g= 9.81
    D= 8  #ou 10
    t= tsaut[i]
    Ca1 = -(vx0*masse)/D
    Ca2 = - Ca1
    Cb1 = -(vy0 * masse)/ D 
    Cb2 = y0 - Cb1
    
    xsaut[i]= ( Ca1* m.exp((-D)*t/masse) + Ca2 )
    ysaut[i]= ( Cb2 + Cb1*m.exp(-D*t/masse) - masse*g*t/D )

for i in range(1,len(tsaut)):
    saut(i)
    if ysaut[i] < 0:
        break
    
for i in range(1,len(tsaut)):
    if xsaut[i] == 0:
        xsaut[i]=xsaut[i-1]



#print(x,"\n",y,"\n",l,"\n",dl) 
#print(x,"\n",p,"\n",f,"\n",c,"\n",evol,"\n",elas,"\n",fric,"\n",E)
#print("l=",l,"\n","x=",x,"\n","y=",y,"\n","vx=",vx,"\n","vy=",vy,"\n","c=",c)
#print("tsaut=",tsaut,"xsaut=",xsaut,"ysaut=",ysaut)
print("Longueur du saut = ",xsaut[-1])


plt.subplot(411)   # grille 4x1, 1er graphique
plt.plot(x, y,"red", label="traj du parcours")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()


'''plt.subplot(411)   # grille 4x1, 1er graphique
plt.plot(xsaut, ysaut,"green", label="traj du saut")
plt.xlabel("xsaut")
plt.ylabel("ysaut")
plt.legend()'''

plt.subplot(412)  # grille 2x1, 2e graphique
plt.plot(tsaut, xsaut, 'red', label="xsaut")
plt.plot(tsaut, ysaut, 'green', label="ysaut")
plt.xlabel("tsaut")
plt.ylabel("x et y saut")
plt.legend()

plt.subplot(212)   # grille 4x1, 2e graphique
plt.plot(x, f, "blue",label="travail de la friction")
plt.plot(x, p, "green",label="potentielle")
plt.plot(x, c, "red",label="cinétique")
plt.plot(x, evol, "cyan",label="volant d'inertie")
plt.plot(x, elas, "magenta",label="elastique")

plt.plot(x, E, "black",label="energie totale")
plt.ylabel("Energies")
plt.legend()

#help(plt.plot)
plt.show()
