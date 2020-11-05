import random
import matplotlib.pyplot as plt
import numpy as np

### Najprej uvozimo potrebne pakete
### Definiramo funckijo, ki nam naključno določi koordinate točk

def koordinate_tocke():
    x = random.uniform(0, 1)
    y = random.uniform(0, 1)
    status = 0
    kolikokarat_sosed = 0
    return [x,y,status,kolikokarat_sosed]

### Definiramo funckijo, ki nam zgenerira n točk

def generiraj_n_tock(n):
    prva_tocka = koordinate_tocke()
    tocke = {"0": prva_tocka}
    for i in range(1,n):
        koordinate = koordinate_tocke()
        tocke.update({"{}".format(i):koordinate})
    return tocke

### Definiramo funkcijo, ki nariše točke
def cas_kuznosti(tocka_ki_nas_zanima, tocke):
    cas = tocke["{}".format(int(tocka_ki_nas_zanima))][2]
    return cas



def ali_je_sosed(kandidat, tocka, tocke, radij, dict_sosedov):
    x_tocke = tocke["{}".format(tocka)][0]
    y_tocke = tocke["{}".format(tocka)][1]
    x_kandidat = tocke["{}".format(kandidat)][0]
    y_kandidat = tocke["{}".format(kandidat)][1]
    if (x_kandidat-x_tocke)**2 + (y_kandidat-y_tocke)**2 < radij**2:
        tocke["{}".format(kandidat)][3] += 1
        if tocka in dict_sosedov["{}".format(kandidat)]:
            pass
        else:
            dict_sosedov["{}".format(kandidat)] += [tocka]
    return tocke, dict_sosedov


def za_risanje_tock(n,tocke, radij, dict_sosedov):
    #figure, axes = plt.subplots()
    for j in range(0,n):
        x = tocke["{}".format(j)][0]
        y = tocke["{}".format(j)][1]
        if tocke["{}".format(j)][2] > 0:
            #krog = plt.Circle((x, y), radij, color='r', fill=False)
            plt.plot(x, y, 'o', color="red")
            #axes.add_artist(krog)
        else:
            #for i in kuzne_tocke:
            #tocke = ali_je_sosed(j, i ,tocke, radij)
            if len(dict_sosedov["{}".format(j)]) > 0:
                plt.plot(x, y, 'o', color="green")
            else:
                plt.plot(x, y, 'o', color="black")
    #axes.add_artist(krog)
    plt.show()

def dodaj_okuzeno_tocko(novo_okuzena_tocka, tocke, koliko_dni_bo_kuzna):
    tocke["{}".format(novo_okuzena_tocka)][2] = koliko_dni_bo_kuzna
    return tocke

def narisi_m_okuzenih_tock(n, m, tocke, T, radij):
    dict_sosedov = {}
    for i in range(0,n):
        dict_sosedov.update({"{}".format(i):[]})
    for i in range(0,m):
        okuzena_tocka = random.randrange(n)
        tocke = dodaj_okuzeno_tocko(okuzena_tocka, tocke, T)
        for j in range(0,n):
            tocke, dict_sosedov = ali_je_sosed(j, okuzena_tocka, tocke, radij, dict_sosedov)
    za_risanje_tock(n, tocke, radij, dict_sosedov)
    return tocke, dict_sosedov

def okuzi_sosede(n, koliko_zacetnih_okuzenih, verjetnost, T, max_st_ponovitev, radij):
    tocke = generiraj_n_tock(n)
    tocke, dict_sosedov = narisi_m_okuzenih_tock(n, koliko_zacetnih_okuzenih, tocke, T, radij)
    koraki = 0
    while max_st_ponovitev > 0:
        max_st_ponovitev -= 1
        koraki += 1
        print(koraki)
        for i in range(0,n):
            kolikokart_sosed = len(dict_sosedov["{}".format(i)])
            if kolikokart_sosed > 0:
                ali_se_okuzi = np.random.binomial(size=kolikokart_sosed, n=1, p=verjetnost)
                ali_se_okuzi = max(ali_se_okuzi)
                if ali_se_okuzi > 0:
                    tocke = dodaj_okuzeno_tocko(i, tocke, T)
        for h in range(0,n):
            stevilo = tocke["{}".format(h)][2]
            if stevilo > 0:
                for j in range(0,n):
                    tocke, dict_sosedov = ali_je_sosed(j, h, tocke, radij, dict_sosedov)
                    if stevilo == 1:
                        try:
                            dict_sosedov["{}".format(j)].remove(h)
                        except:
                            pass
                tocke["{}".format(h)][2] -= 1
        za_risanje_tock(n, tocke, radij, dict_sosedov)
    return tocke
            






#tocke = generiraj_n_tock(200)
### TESTI
#narisi_m_okuzenih_tock(200, 2, tocke, 10, 0.2)
#b = narisi_m_okuzenih_tock(200, 2, tocke, 10, 0.2)
#c=b[1]
##a = b[2]
#b=b[0]
#
b = okuzi_sosede(200, 1, 0.1, 3, 8,0.2)
#
## pogledamo katera točka je okužena
#xcx = 0
#for i in range(0,len(b)):
#    tocka = b["{}".format(i)][2]
#    if tocka > 0:
#        print(i, b["{}".format(i)])

