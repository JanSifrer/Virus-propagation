import random
import matplotlib.pyplot as plt

### Najprej uvozimo potrebne pakete
### Definiramo funckijo, ki nam naključno določi koordinate točk

def koordinate_tocke():
    x = random.uniform(0, 1)
    y = random.uniform(0, 1)
    status = 0
    return [x,y,status]

### Definiramo funkcijo, ki nariše točke

def narisi_tocke(n,tocke,list):
    okuzene_tocke = list
    for j in range(0,n):
        x = tocke["{}".format(j)][0]
        y = tocke["{}".format(j)][1]
        if j in okuzene_tocke:
            plt.plot(x, y, 'o', color="red")
        else:
            plt.plot(x, y, 'o', color="black")
    return plt.show()

### Definiramo funckijo, ki nam zgenerira n točk, in jih nariše

def generiraj_n_tock(n):
    prva_tocka = koordinate_tocke()
    tocke = {"0": prva_tocka}
    for i in range(1,n):
        koordinate = koordinate_tocke()
        tocke.update({"{}".format(i):koordinate})
    
    okuzena_tocka = random.randrange(n)
    tocke["{}".format(okuzena_tocka)][2] = 1
    okuzena_tocka = [okuzena_tocka]
    narisi_tocke(n, tocke, okuzena_tocka)
    return tocke

### TESTI
#a = koordinate_tocke()
b = generiraj_n_tock(200)

# pogledamo katera točka je okužena
xcx = 0
for i in range(0,len(b)):
    tocka = b["{}".format(i)][2]
    if tocka == 1:
        print(i, b["{}".format(i)])
