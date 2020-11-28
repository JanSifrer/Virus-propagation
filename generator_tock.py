import random
import matplotlib.pyplot as plt
import numpy as np
import sys

### Najprej uvozimo potrebne pakete
### Definiramo funckijo, ki nam nakljucno doloci koordinate tock

def koordinate_tocke():
    x = random.uniform(0, 1)
    y = random.uniform(0, 1)
    status = 0
    ze_prebolela = 0
    return [x,y,status, ze_prebolela]

### Definiramo funckijo, ki nam zgenerira n tock

def generiraj_n_tock(n):
    prva_tocka = koordinate_tocke()
    tocke = {"0": prva_tocka}
    for i in range(1,n):
        koordinate = koordinate_tocke()
        tocke.update({"{}".format(i):koordinate})
    return tocke

### Definiramo funkcijo, ki nam ustvari slovar sosedov, 
### pogledamo najprej ali je kandidat sosed od neke dolocene tocke,
### ce je, dodamo to tocko v seznam sosedov od kandidata.
def ali_je_sosed(kandidat, tocka, tocke, radij, dict_sosedov):
    x_tocke = tocke["{}".format(tocka)][0]
    y_tocke = tocke["{}".format(tocka)][1]
    x_kandidat = tocke["{}".format(kandidat)][0]
    y_kandidat = tocke["{}".format(kandidat)][1]
    if (x_kandidat-x_tocke)**2 + (y_kandidat-y_tocke)**2 < radij**2:
        if tocka in dict_sosedov["{}".format(kandidat)]:
            pass
        else:
            dict_sosedov["{}".format(kandidat)] += [tocka]
    return dict_sosedov

### Dolocimo funckijo, ki nam narise tocke
def za_risanje_tock(n,tocke, dict_sosedov, korak_slike):
    for j in range(0,n):
        x = tocke["{}".format(j)][0]
        y = tocke["{}".format(j)][1]
        if tocke["{}".format(j)][3] == 1:
            plt.plot(x, y, 'o', color="blue")
        else:
            if tocke["{}".format(j)][2] > 0:
                plt.plot(x, y, 'o', color="red")
            else:
                if len(dict_sosedov["{}".format(j)]) > 0:
                    plt.plot(x, y, 'o', color="green")
                else:
                    plt.plot(x, y, 'o', color="black")
    plt.suptitle("slika na {} koraku".format(korak_slike))
    plt.show()
    #c.show()

def narisi_m_okuzenih_tock(n, m, tocke, T, radij):
    ### Najprej dediniram slovar sosedov, in zapisem, da nobena tocka ni sosed od kere okuzene
    dict_sosedov = {}
    for i in range(0,n):
        dict_sosedov.update({"{}".format(i):[]})
    for i in range(0,m):
        ### Izberem neko nakljucno okuzeno tocko, in nastavim da bo kuzna se T-1 dni 
        okuzena_tocka = random.randrange(n)
        tocke["{}".format(okuzena_tocka)][2] = T
        for j in range(0,n):
            ### Za vse tocke preverim, ali so sosedi okuzene tocke
            dict_sosedov = ali_je_sosed(j, okuzena_tocka, tocke, radij, dict_sosedov)
    ### Narisem prvo stanje
    za_risanje_tock(n, tocke, dict_sosedov, 1)
    return tocke, dict_sosedov

def okuzi_sosede(n, koliko_zacetnih_okuzenih, verjetnost, T, max_st_ponovitev, radij, koraki_do_slike):
    tocke = generiraj_n_tock(n)
    tocke, dict_sosedov = narisi_m_okuzenih_tock(n, koliko_zacetnih_okuzenih, tocke, T, radij)
    koraki = 0
    while max_st_ponovitev > 0:
        max_st_ponovitev -= 1
        koraki += 1
        for i in range(0,n):
            if tocke["{}".format(i)][3] < 1:
                if tocke["{}".format(i)][2] < 1:
                    ### Najpprej preverimo, ce je sosed od kaksne okuzene tocke, in ce je, od koliko tock je sosed
                    kolikokart_sosed = len(dict_sosedov["{}".format(i)])
                    if kolikokart_sosed > 0:
                        ### Toliko kolikor ima okuzenih sosedov, tolikokrat je lahko z doloceno verjetnostjo okuzen
                        ali_se_okuzi = np.random.binomial(size=kolikokart_sosed, n=1, p=verjetnost)
                        ali_se_okuzi = max(ali_se_okuzi)
                        if ali_se_okuzi > 0:
                            ### Ce se okuzi, nastavimo cas kuznosti na T+1 (T je cas kuznosti, +1 pa mi v naslednji dveh 
                            ### for zankah omogoca, da popravim sosede od nje...)
                            tocke["{}".format(i)][2] = T+1
        steviloo = 0
        preboleli = 0
        for h in range(0,n):
            ali_je_prebolela = tocke["{}".format(h)][3]
            if ali_je_prebolela < 1:
                ### Za vsako tocko pogledamo koliko dni bo se kuzna, ce ni kuzna, vrne 0
                stevilo = tocke["{}".format(h)][2]
                if stevilo > 0:
                    for j in range(0,n):
                        if stevilo > 1:
                            ### Ce bo tocka okuzena se vec kakor 1 dan, potem za vse druge tocke pogledam,
                            ### ce je soseda od okuzene tocke
                            dict_sosedov = ali_je_sosed(j, h, tocke, radij, dict_sosedov)
                        if stevilo == 1:
                            ### Če je to zadnji dan, ko je oseba se kuzna, popravimo seznam sosedov,
                            ### kajti ta tocka (j) ne bo vec soseda od okuzene tocke (h)
                            try:
                                dict_sosedov["{}".format(j)].remove(h)
                            except:
                                pass
                    if stevilo == 1:
                        tocke["{}".format(h)][3] = 1

                    ### Na koncu se popravimo, koliko dni bo se kuzna.
                    tocke["{}".format(h)][2] -= 1
                if stevilo > 1:
                    steviloo +=1
                if stevilo == 1:
                    preboleli += 1
            else:
                preboleli += 1
        ### Narisemo stanje 
        if koraki % koraki_do_slike == 0:
            print("stevilo okuzenih pri {0} koraku je: {1}, zdravih pa {2}".format(koraki, steviloo, preboleli))
            za_risanje_tock(n, tocke, dict_sosedov, koraki)
        if (steviloo)/n == 1:
            print("stevilo okuzenih pri {0} koraku je: {1}".format(koraki, steviloo))
            print("Delez okuzenih je: {}".format(steviloo/n))
            za_risanje_tock(n, tocke, dict_sosedov, koraki)
            break
        if (steviloo)/n == 0:
            print("stevilo okuzenih pri {0} koraku je: {1}, zdravih pa {2}".format(koraki, steviloo, preboleli))
            za_risanje_tock(n, tocke, dict_sosedov, koraki)
            break
    return tocke
            






#tocke = generiraj_n_tock(200)
### TESTI
#narisi_m_okuzenih_tock(200, 2, tocke, 10, 0.2)
#b = narisi_m_okuzenih_tock(200, 2, tocke, 10, 0.2)
#
#b = okuzi_sosede(2000, 1, 0.01, 14, 1000, 0.05)
countt = 0
#for i in b:
#    if b["{}".format(i)][3] == 0:
#        countt +=1
#        #print(i)
